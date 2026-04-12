
package com.veristock.pro.ui.navigation

import androidx.compose.animation.core.tween
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.IntOffset
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.veristock.pro.feature.billing.BillingScreen
import com.veristock.pro.feature.customers.CustomerListScreen
import com.veristock.pro.feature.home.HomeScreen
import com.veristock.pro.feature.products.form.ProductFormScreen
import com.veristock.pro.feature.products.list.ProductListScreen
import com.veristock.pro.feature.reports.DateRangeReportScreen
import com.veristock.pro.feature.reports.ReportsDashboardScreen
import com.veristock.pro.feature.saledetail.SaleDetailScreen
import com.veristock.pro.feature.settings.SettingsDashboardScreen
import com.veristock.pro.feature.settings.invoices.InvoiceSettingsScreen
import com.veristock.pro.feature.settings.printers.PrinterDiscoveryScreen
import com.veristock.pro.feature.settings.printers.PrinterSettingsScreen
import com.veristock.pro.feature.setup.SetupScreen

@Composable
fun AppNavigation(startDestination: String) {

    val navController = rememberNavController()
    val animationSpec = tween<IntOffset>(300)

    NavHost(
        navController = navController,
        startDestination = startDestination,
        enterTransition = { slideInHorizontally(initialOffsetX = { 1000 }, animationSpec = animationSpec) },
        exitTransition = { slideOutHorizontally(targetOffsetX = { -1000 }, animationSpec = animationSpec) },
        popEnterTransition = { slideInHorizontally(initialOffsetX = { -1000 }, animationSpec = animationSpec) },
        popExitTransition = { slideOutHorizontally(targetOffsetX = { 1000 }, animationSpec = animationSpec) }
    ) {

        composable(Screen.Setup.route) {
            SetupScreen(
                onSetupComplete = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Setup.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Home.route) {
            HomeScreen(
                onNewSaleClick = { navController.navigate(Screen.Billing.route) },
                onProductsClick = { navController.navigate(Screen.ProductList.route) },
                onCustomersClick = { navController.navigate(Screen.CustomerList.route) },
                onReportsClick = { navController.navigate(Screen.ReportsDashboard.route) },
                onSettingsClick = { navController.navigate(Screen.SettingsDashboard.route) }
            )
        }

        composable(Screen.SettingsDashboard.route) {
            SettingsDashboardScreen(
                onNavigateToInvoiceSettings = { navController.navigate(Screen.InvoiceSettings.route) },
                onNavigateToPrinterSettings = { navController.navigate(Screen.PrinterSettings.route) }
            )
        }
        composable(Screen.InvoiceSettings.route) {
             InvoiceSettingsScreen()
        }
        composable(Screen.PrinterSettings.route) {
             PrinterSettingsScreen(
                 onNavigateToDiscovery = { navController.navigate(Screen.PrinterDiscovery.route) }
             )
        }
        composable(Screen.PrinterDiscovery.route) {
             PrinterDiscoveryScreen()
        }

        composable(Screen.ReportsDashboard.route) {
            ReportsDashboardScreen(
                onNavigateToDateRangeReport = { navController.navigate(Screen.DateRangeReport.route) }
            )
        }

        composable(Screen.DateRangeReport.route) {
            DateRangeReportScreen(onBackClick = { navController.navigateUp() })
        }

        composable(Screen.ProductList.route) {
            ProductListScreen(
                onAddClick = { navController.navigate(Screen.ProductForm.createRoute(0)) },
                onEditClick = { productId -> navController.navigate(Screen.ProductForm.createRoute(productId)) },
                onBackClick = { navController.navigateUp() }
            )
        }

        composable(
            route = Screen.ProductForm.route,
            arguments = listOf(
                navArgument("productId") {
                    type = NavType.LongType
                    defaultValue = 0L
                }
            )
        ) {
            ProductFormScreen(
                onSaveComplete = { navController.navigateUp() },
                onBackClick = { navController.navigateUp() }
            )
        }

        composable(Screen.CustomerList.route) {
            CustomerListScreen(
                onBackClick = { navController.navigateUp() },
                onCustomerClick = { /* future */ }
            )
        }

        composable(Screen.Billing.route) {
            BillingScreen(
                onBackClick = { navController.navigateUp() },
                onViewInvoice = { saleId ->
                    navController.navigate(Screen.SaleDetail.createRoute(saleId))
                }
            )
        }

        composable(
            route = Screen.SaleDetail.route,
            arguments = listOf(
                navArgument("saleId") { type = NavType.LongType }
            )
        ) {
            SaleDetailScreen()
        }

        composable(Screen.SalesList.route) {
            PlaceholderScreen("Sales (Coming Soon)")
        }
    }
}

@Composable
fun PlaceholderScreen(text: String) {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(text)
    }
}
