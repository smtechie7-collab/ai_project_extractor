package com.veristock.pro.feature.batchgeneration

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.domain.model.Sale
import java.text.SimpleDateFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BatchGenerationScreen(viewModel: BatchGenerationViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsState()
    var showStartDatePicker by remember { mutableStateOf(false) }
    var showEndDatePicker by remember { mutableStateOf(false) }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Batch Invoice Generation") }) }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Date Range
            Text("Date Range", style = MaterialTheme.typography.titleMedium)
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedButton(onClick = { showStartDatePicker = true }) {
                    Text("From: ${SimpleDateFormat("dd/MM/yy", Locale.US).format(state.startDate)}")
                }
                OutlinedButton(onClick = { showEndDatePicker = true }) {
                    Text("To: ${SimpleDateFormat("dd/MM/yy", Locale.US).format(state.endDate)}")
                }
            }

            // Output Format
            Text("Output Format", style = MaterialTheme.typography.titleMedium)
            Row(verticalAlignment = Alignment.CenterVertically) {
                RadioButton(
                    selected = state.outputFormat == BatchOutputFormat.ZIP_FILE,
                    onClick = { viewModel.onOutputFormatChanged(BatchOutputFormat.ZIP_FILE) }
                )
                Text("Separate PDF files (in ZIP)")
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                RadioButton(
                    selected = state.outputFormat == BatchOutputFormat.SINGLE_PDF,
                    onClick = { viewModel.onOutputFormatChanged(BatchOutputFormat.SINGLE_PDF) }
                )
                Text("Single combined PDF")
            }

            HorizontalDivider()

            // Matching Invoices
            Text("${state.matchingSales.size} invoices match filters", style = MaterialTheme.typography.titleMedium)
            if (state.isFetchingSales) {
                CircularProgressIndicator()
            } else {
                LazyColumn(modifier = Modifier.weight(1f)) {
                    items(state.matchingSales) { sale ->
                        SaleListItem(sale)
                    }
                }
            }

            Button(
                onClick = { viewModel.startBatchGeneration() },
                enabled = state.matchingSales.isNotEmpty() && state.workId == null,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(if (state.workId != null) "Processing..." else "Generate All")
            }
        }
    }

    if (showStartDatePicker) {
        val datePickerState = rememberDatePickerState(initialSelectedDateMillis = state.startDate)
        DatePickerDialog(
            onDismissRequest = { showStartDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    datePickerState.selectedDateMillis?.let {
                        viewModel.onDateRangeChanged(startDate = it, endDate = state.endDate)
                    }
                    showStartDatePicker = false
                }) { Text("OK") }
            },
            dismissButton = {
                 TextButton(onClick = { showStartDatePicker = false }) { Text("Cancel") }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }

    if (showEndDatePicker) {
        val datePickerState = rememberDatePickerState(initialSelectedDateMillis = state.endDate)
        DatePickerDialog(
            onDismissRequest = { showEndDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    datePickerState.selectedDateMillis?.let {
                        viewModel.onDateRangeChanged(startDate = state.startDate, endDate = it)
                    }
                    showEndDatePicker = false
                }) { Text("OK") }
            },
            dismissButton = {
                 TextButton(onClick = { showEndDatePicker = false }) { Text("Cancel") }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }
}

@Composable
fun SaleListItem(sale: Sale) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(sale.invoiceNumber, style = MaterialTheme.typography.bodyLarge)
                Text(sale.customerName, style = MaterialTheme.typography.bodySmall)
            }
            Text("₹${String.format(Locale.US, "%.2f", sale.grandTotal)}", style = MaterialTheme.typography.bodyLarge)
        }
    }
}
