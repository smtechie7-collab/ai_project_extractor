package com.veristock.pro.feature.settings.invoices

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.core.pdf.models.InvoiceTemplateType
import com.veristock.pro.domain.model.PaperSize
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InvoiceSettingsScreen(viewModel: InvoiceSettingsViewModel = hiltViewModel()) {
    val template by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Invoice Settings") })
        }
    ) { padding ->
        if (template == null) {
            // Show a loading indicator while settings are loaded
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(24.dp)
            ) {
                // Template Type Selector
                item {
                    Text("Invoice Template", style = MaterialTheme.typography.titleMedium)
                    Spacer(modifier = Modifier.height(8.dp))
                    SingleChoiceSegmentedButtonRow(modifier = Modifier.fillMaxWidth()) {
                        InvoiceTemplateType.values().forEachIndexed { index, type ->
                            SegmentedButton(
                                shape = SegmentedButtonDefaults.itemShape(index = index, count = InvoiceTemplateType.values().size),
                                onClick = { viewModel.onTemplateTypeChange(type) },
                                selected = template!!.type == type
                            ) {
                                Text(type.name.replace("_", " ").myCapitalize())
                            }
                        }
                    }
                }

                // Page Size Selector
                item {
                    Text("Paper Size", style = MaterialTheme.typography.titleMedium)
                    Spacer(modifier = Modifier.height(8.dp))
                    SingleChoiceSegmentedButtonRow(modifier = Modifier.fillMaxWidth()) {
                        PaperSize.values().forEachIndexed { index, size ->
                            SegmentedButton(
                                shape = SegmentedButtonDefaults.itemShape(index = index, count = PaperSize.values().size),
                                onClick = { viewModel.onPageSizeChange(size) },
                                selected = template!!.pageSize == size
                            ) {
                                Text(size.displayName)
                            }
                        }
                    }
                }
            }
        }
    }
}

// Helper to fix capitalization for SegmentedButton text
private fun String.myCapitalize(): String {
    return this.lowercase(Locale.getDefault()).replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() }
}
