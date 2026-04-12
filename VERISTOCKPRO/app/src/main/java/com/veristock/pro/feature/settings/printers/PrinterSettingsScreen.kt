
package com.veristock.pro.feature.settings.printers

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Done
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.data.entity.PrinterProfileEntity

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PrinterSettingsScreen(
    viewModel: PrinterViewModel = hiltViewModel(),
    onNavigateToDiscovery: () -> Unit
) {
    val savedProfiles by viewModel.savedProfiles.collectAsState()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Printer Settings") }) },
        floatingActionButton = {
            FloatingActionButton(onClick = onNavigateToDiscovery) {
                Icon(Icons.Default.Add, contentDescription = "Add Printer")
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (savedProfiles.isEmpty()) {
                item {
                    Text(
                        text = "No printers saved. Tap the '+' button to find and add a new printer.",
                        modifier = Modifier.padding(16.dp),
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            } else {
                items(savedProfiles, key = { it.id }) {
                    PrinterProfileCard(profile = it, viewModel = viewModel)
                }
            }
        }
    }
}

@Composable
fun PrinterProfileCard(
    profile: PrinterProfileEntity,
    viewModel: PrinterViewModel
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = profile.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f)
                )
                if (profile.isDefault) {
                    Icon(
                        Icons.Default.Done,
                        contentDescription = "Default Printer",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(start = 8.dp)
                    )
                }
            }
            Text("Address: ${profile.deviceAddress}", style = MaterialTheme.typography.bodySmall)
            Text("Paper: ${profile.paperWidth.name}", style = MaterialTheme.typography.bodySmall)

            Spacer(Modifier.height(16.dp))

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                if (!profile.isDefault) {
                    Button(onClick = { viewModel.setAsDefault(profile) }) {
                        Text("Set as Default")
                    }
                }
                OutlinedButton(onClick = { /* TODO: Implement Test Print */ }) {
                    Text("Test Print")
                }
                IconButton(onClick = { viewModel.deleteProfile(profile) }) {
                    Icon(Icons.Default.Delete, contentDescription = "Delete Profile", tint = MaterialTheme.colorScheme.error)
                }
            }
        }
    }
}
