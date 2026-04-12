
package com.veristock.pro.feature.settings.printers

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.core.print.BluetoothPrinterManager
import com.veristock.pro.core.print.model.PaperWidth
import com.veristock.pro.data.dao.PrinterProfileDao
import com.veristock.pro.data.entity.PrinterProfileEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.util.UUID
import javax.inject.Inject

@HiltViewModel
@SuppressLint("MissingPermission") // Permissions are handled by the UI before calling these functions
class PrinterViewModel @Inject constructor(
    private val bluetoothManager: BluetoothPrinterManager,
    private val printerProfileDao: PrinterProfileDao
) : ViewModel() {

    val scannedDevices = bluetoothManager.scannedDevices
    val pairedDevices = bluetoothManager.pairedDevices
    val printerState = bluetoothManager.printerState

    val savedProfiles = printerProfileDao.getAllProfiles()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    init {
        // Load already paired devices as soon as the ViewModel is created
        bluetoothManager.fetchPairedDevices()
    }

    fun startDiscovery() {
        bluetoothManager.startDiscovery()
    }

    fun stopDiscovery() {
        bluetoothManager.stopDiscovery()
    }

    fun saveOrUpdatePrinterProfile(device: BluetoothDevice, name: String, paperWidth: PaperWidth) {
        viewModelScope.launch {
            val existingProfile = printerProfileDao.getProfileByAddress(device.address)
            val profile = PrinterProfileEntity(
                id = existingProfile?.id ?: UUID.randomUUID().toString(),
                name = name,
                deviceAddress = device.address,
                deviceName = device.name ?: "Bluetooth Printer",
                paperWidth = paperWidth,
                isDefault = existingProfile?.isDefault ?: (savedProfiles.value.isEmpty())
            )
            printerProfileDao.insert(profile)
        }
    }

    fun setAsDefault(profile: PrinterProfileEntity) {
        viewModelScope.launch {
            // Clear the default status from all other profiles first
            printerProfileDao.clearAllDefaults()
            // Set the new default
            printerProfileDao.update(profile.copy(isDefault = true))
        }
    }

    fun deleteProfile(profile: PrinterProfileEntity) {
        viewModelScope.launch {
            printerProfileDao.delete(profile)
        }
    }

    fun connectToDevice(profile: PrinterProfileEntity) {
        bluetoothManager.getDeviceByAddress(profile.deviceAddress)?.let {
            bluetoothManager.connect(it)
        }
    }

    override fun onCleared() {
        super.onCleared()
        // Ensure discovery is stopped to prevent context leaks
        stopDiscovery()
    }
}
