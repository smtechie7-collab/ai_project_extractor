
package com.veristock.pro.feature.saledetail

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.Print
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.core.print.model.PrintJobStatus
import com.veristock.pro.data.entity.PrintJobEntity
import com.veristock.pro.domain.model.InvoicePdfMetadata
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale // Added import

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SaleDetailScreen(viewModel: SaleDetailViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsState()
    val printJob by viewModel.printJobState.collectAsState()

    // Show the status dialog whenever there's an active print job
    printJob?.let {
        PrintStatusDialog(
            job = it,
            onDismiss = { viewModel.clearPrintJobState() }
        )
    }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Sale Details") }) }
    ) { padding ->
        if (state.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (state.error != null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("Error: ${state.error}")
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    Text("Invoice: ${state.sale?.invoiceNumber}", style = MaterialTheme.typography.headlineSmall)
                    Text("Customer: ${state.customer?.name}", style = MaterialTheme.typography.bodyLarge)
                    Text("Total: ₹${state.sale?.grandTotal}", style = MaterialTheme.typography.bodyLarge)
                }

                item {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = { viewModel.printSale() }) {
                            Icon(Icons.Default.Print, contentDescription = "Print Icon", modifier = Modifier.size(ButtonDefaults.IconSize))
                            Spacer(modifier = Modifier.size(ButtonDefaults.IconSpacing))
                            Text("Print Receipt")
                        }
                    }
                }

                item {
                    Text("PDF Generation History", style = MaterialTheme.typography.titleMedium)
                }

                if (state.history.isEmpty()) {
                    item {
                        Text("No PDF generation history found.")
                    }
                } else {
                    items(state.history) { metadata ->
                        HistoryListItem(metadata)
                    }
                }
            }
        }
    }
}

@Composable
fun PrintStatusDialog(job: PrintJobEntity, onDismiss: () -> Unit) {
    val dialogTitle: String
    val dialogContent: @Composable () -> Unit

    when (job.status) {
        PrintJobStatus.QUEUED, PrintJobStatus.PREPARING, PrintJobStatus.PRINTING -> {
            dialogTitle = "Printing..."
            dialogContent = {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    CircularProgressIndicator(modifier = Modifier.padding(16.dp))
                    Text(text = "Status: ${job.status.name}", textAlign = TextAlign.Center)
                }
            }
        }
        PrintJobStatus.SUCCESS -> {
            dialogTitle = "Success"
            dialogContent = {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.ThumbUp, contentDescription = "Success", tint = Color(0xFF00C853), modifier = Modifier.size(48.dp).padding(bottom = 8.dp))
                    Text("Printed successfully!")
                }
            }
        }
        PrintJobStatus.FAILED -> {
            dialogTitle = "Print Failed"
            dialogContent = {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Error, contentDescription = "Error", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(48.dp).padding(bottom = 8.dp))
                    Text("Error: ${job.lastError ?: "Unknown error"}", textAlign = TextAlign.Center)
                }
            }
        }
        else -> {
            // For CANCELLED or other states
            dialogTitle = "Print Status"
            dialogContent = { Text("Job status: ${job.status.name}") }
        }
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(dialogTitle) },
        text = dialogContent,
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Dismiss")
            }
        }
    )
}

@Composable
fun HistoryListItem(metadata: InvoicePdfMetadata) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Generated at: ${SimpleDateFormat("dd/MM/yy hh:mm a", Locale.getDefault()).format(Date(metadata.generatedAt))}", style = MaterialTheme.typography.bodyMedium)
            Text("Template: ${metadata.templateType}", style = MaterialTheme.typography.bodySmall)
            Text("Paper: ${metadata.paperSize}", style = MaterialTheme.typography.bodySmall)
            Text("File Size: ${metadata.fileSize / 1024} KB", style = MaterialTheme.typography.bodySmall)
        }
    }
}
