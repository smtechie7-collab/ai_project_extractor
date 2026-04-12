package com.veristock.pro.feature.batch

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.feature.batch.components.DateRangeSelector

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BatchGenerationScreen(
    onBackClick: () -> Unit,
    viewModel: BatchGenerationViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Batch Invoice Generation") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                }
            )
        }
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(it)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            DateRangeSelector(state.startDate, state.endDate, viewModel::setDateRange)

            Text("Found ${state.matchingInvoiceCount} invoices in the selected range.")

            Spacer(modifier = Modifier.height(16.dp))

            OutputFormatSelector(state.outputFormat, viewModel::setOutputFormat)

            Spacer(modifier = Modifier.weight(1f))

            Button(
                onClick = viewModel::startGeneration,
                modifier = Modifier.fillMaxWidth().height(56.dp),
                enabled = state.matchingInvoiceCount > 0 && !state.isGenerating
            ) {
                if (state.isGenerating) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp))
                } else {
                    Text("Generate ${state.matchingInvoiceCount} Invoices")
                }
            }
        }
    }
}

@Composable
fun OutputFormatSelector(selectedFormat: OutputFormat, onFormatSelected: (OutputFormat) -> Unit) {
    Column {
        Text("Output Format", style = MaterialTheme.typography.titleMedium)
        Row(verticalAlignment = Alignment.CenterVertically) {
            RadioButton(
                selected = selectedFormat == OutputFormat.ZIP_FILE,
                onClick = { onFormatSelected(OutputFormat.ZIP_FILE) }
            )
            Text("Separate PDF files (in ZIP)")
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            RadioButton(
                selected = selectedFormat == OutputFormat.SINGLE_PDF,
                onClick = { onFormatSelected(OutputFormat.SINGLE_PDF) }
            )
            Text("Single Combined PDF")
        }
    }
}
