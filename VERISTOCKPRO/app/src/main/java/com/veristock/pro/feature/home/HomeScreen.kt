package com.veristock.pro.feature.home

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ReceiptLong
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.ui.shared.shimmerBrush
import kotlinx.coroutines.launch
import java.math.BigDecimal
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNewSaleClick: () -> Unit,
    onProductsClick: () -> Unit,
    onCustomersClick: () -> Unit,
    onReportsClick: () -> Unit,
    onSettingsClick: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    LaunchedEffect(uiState.errorMessage) {
        uiState.errorMessage?.let {
            scope.launch { snackbarHostState.showSnackbar(it) }
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            TopAppBar(
                title = { Text("VERISTOCK PRO", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    actionIconContentColor = MaterialTheme.colorScheme.onPrimary
                ),
                actions = {
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }
            )
        }
    ) { padding ->
        PullToRefreshBox(
            isRefreshing = uiState.isRefreshing,
            onRefresh = viewModel::refreshDashboard,
            modifier = Modifier.fillMaxSize().padding(padding)
        ) {
            Column(
                modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState())
            ) {
                if (uiState.isLoading) {
                    ShimmerDashboard()
                } else {
                    DashboardContent(
                        stats = uiState.stats,
                        onNewSaleClick = onNewSaleClick,
                        onProductsClick = onProductsClick,
                        onCustomersClick = onCustomersClick,
                        onReportsClick = onReportsClick
                    )
                }
            }
        }
    }
}

@Composable
private fun DashboardContent(
    stats: DashboardStats,
    onNewSaleClick: () -> Unit,
    onProductsClick: () -> Unit,
    onCustomersClick: () -> Unit,
    onReportsClick: () -> Unit
) {
    Column(modifier = Modifier.padding(16.dp)) {
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxWidth().height(280.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            userScrollEnabled = false
        ) {
            item { StatCard("Today's Sales", formatCurrency(stats.todaySales), Icons.Default.MonetizationOn, MaterialTheme.colorScheme.primary) }
            item { StatCard("Transactions", stats.todayTransactions.toString(), Icons.AutoMirrored.Filled.ReceiptLong, MaterialTheme.colorScheme.secondary) }
            item { StatCard("Low Stock", stats.lowStockCount.toString(), Icons.Default.Warning, MaterialTheme.colorScheme.error) }
            item { StatCard("Total Products", stats.totalProducts.toString(), Icons.Default.Inventory, MaterialTheme.colorScheme.tertiary) }
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text("Quick Actions", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))

        LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp), contentPadding = PaddingValues(horizontal = 4.dp)) {
            item { ActionButton("New Sale", Icons.Default.AddShoppingCart, onNewSaleClick, isPrimary = true) }
            item { ActionButton("Products", Icons.Default.Inventory, onProductsClick) }
            item { ActionButton("Customers", Icons.Default.Group, onCustomersClick) }
            item { ActionButton("Reports", Icons.Default.Assessment, onReportsClick) }
        }
    }
}

@Composable
private fun StatCard(title: String, value: String, icon: ImageVector, color: Color) {
    Card(modifier = Modifier.fillMaxSize(), elevation = CardDefaults.cardElevation(4.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.SpaceBetween, horizontalAlignment = Alignment.Start) {
            Icon(imageVector = icon, contentDescription = title, modifier = Modifier.size(32.dp), tint = color)
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = value, fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
            Text(text = title, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun ActionButton(text: String, icon: ImageVector, onClick: () -> Unit, isPrimary: Boolean = false) {
    val containerColor = if (isPrimary) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
    val contentColor = if (isPrimary) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant

    Card(modifier = Modifier.size(100.dp).clip(RoundedCornerShape(12.dp)).clickable(onClick = onClick), shape = RoundedCornerShape(12.dp), colors = CardDefaults.cardColors(containerColor = containerColor)) {
        Column(modifier = Modifier.fillMaxSize(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
            Icon(imageVector = icon, contentDescription = text, tint = contentColor)
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = text, color = contentColor, fontSize = 12.sp, textAlign = TextAlign.Center)
        }
    }
}

@Composable
private fun ShimmerDashboard() {
    Column(modifier = Modifier.padding(16.dp)) {
        LazyVerticalGrid(columns = GridCells.Fixed(2), modifier = Modifier.fillMaxWidth().height(280.dp), verticalArrangement = Arrangement.spacedBy(16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), userScrollEnabled = false) {
            items(4) {
                Box(modifier = Modifier.aspectRatio(1f).background(shimmerBrush(), shape = RoundedCornerShape(16.dp)))
            }
        }
    }
}

private fun formatCurrency(amount: BigDecimal): String {
    val format = NumberFormat.getCurrencyInstance(Locale("en", "IN"))
    return format.format(amount)
}
