
package com.veristock.pro.core.print

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothSocket
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.content.ContextCompat
import com.veristock.pro.core.print.model.BluetoothPrinterState
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import java.io.IOException
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class BluetoothPrinterManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val bluetoothManager = context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
    private val bluetoothAdapter: BluetoothAdapter? = bluetoothManager.adapter

    private val sppUuid: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

    private var bluetoothSocket: BluetoothSocket? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private val connectionMutex = Mutex()

    private val _printerState = MutableStateFlow<BluetoothPrinterState>(BluetoothPrinterState.DISCONNECTED)
    val printerState: StateFlow<BluetoothPrinterState> = _printerState.asStateFlow()

    private val _scannedDevices = MutableStateFlow<List<BluetoothDevice>>(emptyList())
    val scannedDevices: StateFlow<List<BluetoothDevice>> = _scannedDevices.asStateFlow()

    private val _pairedDevices = MutableStateFlow<List<BluetoothDevice>>(emptyList())
    val pairedDevices: StateFlow<List<BluetoothDevice>> = _pairedDevices.asStateFlow()

    private val discoveryReceiver = object : BroadcastReceiver() {
        @SuppressLint("MissingPermission")
        override fun onReceive(context: Context, intent: Intent) {
            if (intent.action == BluetoothDevice.ACTION_FOUND) {
                val device: BluetoothDevice? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE, BluetoothDevice::class.java)
                } else {
                    @Suppress("DEPRECATION")
                    intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
                }
                device?.let { foundDevice ->
                    if (isPrinter(foundDevice) && !_scannedDevices.value.any { it.address == foundDevice.address }) {
                        _scannedDevices.value = _scannedDevices.value + foundDevice
                    }
                }
            }
        }
    }

    fun hasBluetoothPermissions(): Boolean {
        val requiredPermissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            listOf(Manifest.permission.BLUETOOTH_CONNECT, Manifest.permission.BLUETOOTH_SCAN)
        } else {
            listOf(Manifest.permission.BLUETOOTH, Manifest.permission.BLUETOOTH_ADMIN, Manifest.permission.ACCESS_FINE_LOCATION)
        }
        return requiredPermissions.all {
            ContextCompat.checkSelfPermission(context, it) == PackageManager.PERMISSION_GRANTED
        }
    }

    @SuppressLint("MissingPermission")
    fun getDeviceByAddress(address: String): BluetoothDevice? {
        if (!hasBluetoothPermissions()) return null
        return try {
            bluetoothAdapter?.getRemoteDevice(address)
        } catch (e: IllegalArgumentException) {
            null
        }
    }

    @SuppressLint("MissingPermission")
    fun startDiscovery() {
        if (!hasBluetoothPermissions()) return
        if (bluetoothAdapter?.isDiscovering == true) {
            return
        }
        _scannedDevices.value = emptyList()
        val filter = IntentFilter(BluetoothDevice.ACTION_FOUND)
        context.registerReceiver(discoveryReceiver, filter)
        bluetoothAdapter?.startDiscovery()
    }

    @SuppressLint("MissingPermission")
    fun stopDiscovery() {
        if (!hasBluetoothPermissions() || bluetoothAdapter?.isDiscovering == false) return
        try {
            context.unregisterReceiver(discoveryReceiver)
            bluetoothAdapter?.cancelDiscovery()
        } catch (e: IllegalArgumentException) {
            // Receiver not registered, ignore
        }
    }

    @SuppressLint("MissingPermission")
    fun fetchPairedDevices() {
        if (!hasBluetoothPermissions()) return
        _pairedDevices.value = bluetoothAdapter?.bondedDevices?.filter { isPrinter(it) } ?: emptyList()
    }

    fun connect(device: BluetoothDevice) {
        coroutineScope.launch {
            connectionMutex.withLock {
                if (_printerState.value == BluetoothPrinterState.CONNECTED && bluetoothSocket?.remoteDevice?.address == device.address) {
                    return@withLock
                }
                if (bluetoothAdapter?.isDiscovering == true) {
                    stopDiscovery()
                }
                _printerState.value = BluetoothPrinterState.CONNECTING
                try {
                    @SuppressLint("MissingPermission")
                    val socket: BluetoothSocket? = device.createRfcommSocketToServiceRecord(sppUuid)
                    socket?.connect() // Blocking call
                    bluetoothSocket = socket
                    _printerState.value = BluetoothPrinterState.CONNECTED
                } catch (e: IOException) {
                    handleConnectionError()
                } catch (e: SecurityException) {
                    handleConnectionError()
                }
            }
        }
    }

    fun disconnect() {
        coroutineScope.launch {
            connectionMutex.withLock {
                handleConnectionError()
            }
        }
    }

    private fun handleConnectionError() {
        try {
            bluetoothSocket?.close()
        } catch (e: IOException) {
            // Ignore error on close
        } finally {
            bluetoothSocket = null
            _printerState.value = BluetoothPrinterState.DISCONNECTED
        }
    }

    suspend fun writeData(data: ByteArray) = withContext(Dispatchers.IO) {
        if (_printerState.value != BluetoothPrinterState.CONNECTED) {
            _printerState.value = BluetoothPrinterState.ERROR
            throw IOException("Printer is not connected.")
        }
        try {
            _printerState.value = BluetoothPrinterState.PRINTING
            bluetoothSocket?.outputStream?.write(data)
            bluetoothSocket?.outputStream?.flush()
            _printerState.value = BluetoothPrinterState.CONNECTED
        } catch (e: IOException) {
            _printerState.value = BluetoothPrinterState.ERROR
            disconnect()
            throw e
        }
    }

    @SuppressLint("MissingPermission")
    private fun isPrinter(device: BluetoothDevice): Boolean {
        if (!hasBluetoothPermissions()) return false
        val deviceClass = device.bluetoothClass?.majorDeviceClass
        val deviceName = device.name?.lowercase() ?: ""
        if (deviceClass == android.bluetooth.BluetoothClass.Device.Major.IMAGING) {
            return true
        }
        val printerKeywords = listOf("printer", "pos", "rp", "tvs", "epson", "imin", "mpt")
        return printerKeywords.any { keyword -> deviceName.contains(keyword) }
    }
}
