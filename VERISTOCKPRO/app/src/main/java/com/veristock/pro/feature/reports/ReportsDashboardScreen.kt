package com.veristock.pro.feature.reports

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReportsDashboardScreen(
    onNavigateToDateRangeReport: () -> Unit,
    viewModel: ReportsDashboardViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Reports & Analytics") }
            )
        }
    ) {
        if (state.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (state.errorMessage != null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Warning, contentDescription = "Error")
                    Text(text = state.errorMessage ?: "An unknown error occurred.")
                }
            }
        } else {
            Column(
                modifier = Modifier
                    .padding(it)
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Quick Stats Dashboard
                Text("Today's Performance", style = MaterialTheme.typography.titleLarge)
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) {
                    StatCard("Today's Sales", "₹${state.todayStats?.totalSales ?: 0.0}")
                    StatCard("Transactions", "${state.todayStats?.transactionCount ?: 0}")
                    StatCard("Avg. Sale", "₹${state.todayStats?.averageTicketSize ?: 0.0}")
                }

                HorizontalDivider()

                // Report Categories
                Text("Report Categories", style = MaterialTheme.typography.titleLarge)
                ReportCategoryItem("Sales Reports", "Daily, weekly, and monthly sales trends", Icons.AutoMirrored.Filled.ArrowForward, onClick = onNavigateToDateRangeReport)
                ReportCategoryItem("GST Reports", "GSTR-1 summaries and tax breakdowns", Icons.AutoMirrored.Filled.ArrowForward) { /* TODO */ }
                ReportCategoryItem("Product Reports", "Analyze product performance and stock", Icons.AutoMirrored.Filled.ArrowForward) { /* TODO */ }
                ReportCategoryItem("Customer Reports", "Identify top customers and purchase history", Icons.AutoMirrored.Filled.ArrowForward) { /* TODO */ }
            }
        }
    }
}

@Composable
fun StatCard(title: String, value: String) {
    Card {
        Column(modifier = Modifier.padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = title, style = MaterialTheme.typography.labelMedium)
            Text(text = value, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReportCategoryItem(title: String, description: String, icon: ImageVector, onClick: () -> Unit) {
    ListItem(
        headlineContent = { Text(title) },
        supportingContent = { Text(description) },
        trailingContent = { Icon(icon, contentDescription = null) },
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
    )
}
