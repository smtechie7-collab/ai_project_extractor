package com.veristock.pro.feature.reports

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.domain.model.reports.SalesReportRow
import com.veristock.pro.feature.reports.components.DateRangeSelector
import com.veristock.pro.feature.reports.components.SalesLineChart

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DateRangeReportScreen(
    onBackClick: () -> Unit,
    viewModel: DateRangeReportViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Date Range Sales Report") },
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
                .padding(16.dp)
        ) {
            DateRangeSelector(
                selectedRange = state.filters.dateRange,
                startDate = state.filters.startDate ?: 0,
                endDate = state.filters.endDate ?: 0,
                onRangeSelected = viewModel::onFiltersChanged
            )

            Spacer(Modifier.height(16.dp))

            if (state.isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (state.errorMessage != null) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "Error: ${state.errorMessage}",
                        color = MaterialTheme.colorScheme.error,
                        textAlign = TextAlign.Center
                    )
                }
            } else if (state.reportResult != null) {
                val report = state.reportResult!!
                
                // Summary Cards
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) {
                    StatCard("Total Sales", "₹${report.summary.totalAmount}")
                    StatCard("Transactions", "${report.summary.totalCount}")
                    StatCard("Avg. Sale", "₹${report.summary.averageAmount}")
                }

                Spacer(Modifier.height(16.dp))

                // Chart
                val chartData = report.data.mapIndexed { index, row -> Pair(index.toFloat(), row.grandTotal.toFloat()) }
                SalesLineChart(
                    data = chartData,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(250.dp)
                )

                Spacer(Modifier.height(16.dp))

                // Data Table
                LazyColumn {
                    item {
                         Row(Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                            TableCell(text = "Invoice", weight = .3f, title = true)
                            TableCell(text = "Customer", weight = .4f, title = true)
                            TableCell(text = "Amount", weight = .3f, title = true, alignment = TextAlign.End)
                        }
                        HorizontalDivider()
                    }
                    items(report.data) { row ->
                        Row(Modifier.fillMaxWidth()) {
                            TableCell(text = row.invoiceNumber, weight = .3f)
                            TableCell(text = row.customerName, weight = .4f)
                            TableCell(text = "₹${row.grandTotal}", weight = .3f, alignment = TextAlign.End)
                        }
                    }
                }
            } else {
                 Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("No data available for the selected period.")
                }
            }
        }
    }
}

@Composable
fun RowScope.TableCell(text: String, weight: Float, alignment: TextAlign = TextAlign.Start, title: Boolean = false) {
    Text(
        text = text,
        modifier = Modifier
            .weight(weight)
            .padding(8.dp),
        fontWeight = if (title) FontWeight.Bold else FontWeight.Normal,
        textAlign = alignment
    )
}
