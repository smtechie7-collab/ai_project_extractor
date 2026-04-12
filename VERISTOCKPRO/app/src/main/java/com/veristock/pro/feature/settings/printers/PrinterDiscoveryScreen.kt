
package com.veristock.pro.feature.settings.printers

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.core.print.model.PaperWidth

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PrinterDiscoveryScreen(
    viewModel: PrinterViewModel = hiltViewModel()
) {
    val scannedDevices by viewModel.scannedDevices.collectAsState()
    val pairedDevices by viewModel.pairedDevices.collectAsState()
    var showSaveDialog by remember { mutableStateOf<BluetoothDevice?>(null) }

    val permissionsToRequest = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.BLUETOOTH_ADMIN, Manifest.permission.BLUETOOTH)
    }

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions(),
        onResult = { permissions ->
            if (permissions.values.all { it }) {
                viewModel.startDiscovery()
            } else {
                // You can show a snackbar here to inform the user that permissions are needed
            }
        }
    )

    LaunchedEffect(key1 = true) {
        permissionLauncher.launch(permissionsToRequest)
    }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Find Printers") }) }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            item {
                Button(onClick = { viewModel.startDiscovery() }, modifier = Modifier.fillMaxWidth()) {
                    Text("Start Scan")
                }
            }

            item {
                Text("Paired Printers", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp))
            }
            items(pairedDevices, key = { it.address }) {
                DeviceListItem(device = it) { device -> showSaveDialog = device }
            }

            item {
                Text("Available Printers", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp))
            }
            items(scannedDevices, key = { it.address }) {
                DeviceListItem(device = it) { device -> showSaveDialog = device }
            }
        }
    }

    showSaveDialog?.let { device ->
        SavePrinterDialog(
            device = device,
            onDismiss = { showSaveDialog = null },
            onSave = { name, paperWidth ->
                viewModel.saveOrUpdatePrinterProfile(device, name, paperWidth)
                showSaveDialog = null
            }
        )
    }
}

@SuppressLint("MissingPermission")
@Composable
fun DeviceListItem(device: BluetoothDevice, onClick: (BluetoothDevice) -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick(device) },
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(text = device.name ?: "Unknown Device", fontWeight = FontWeight.Bold)
            Text(text = device.address, style = MaterialTheme.typography.bodySmall)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@SuppressLint("MissingPermission")
@Composable
fun SavePrinterDialog(
    device: BluetoothDevice,
    onDismiss: () -> Unit,
    onSave: (String, PaperWidth) -> Unit
) {
    var name by remember { mutableStateOf(device.name ?: "") }
    var paperWidth by remember { mutableStateOf(PaperWidth.MM_58) }
    var expanded by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Save Printer") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Profile Name") }
                )

                ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
                    OutlinedTextField(
                        value = paperWidth.name,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Paper Width") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                        modifier = Modifier.menuAnchor()
                    )
                    ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false }
                    ) {
                        PaperWidth.entries.forEach { width ->
                            DropdownMenuItem(
                                text = { Text("${width.name} (${width.charsPerLine} chars)") },
                                onClick = {
                                    paperWidth = width
                                    expanded = false
                                }
                            )
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(onClick = { onSave(name, paperWidth) }) {
                Text("Save")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
