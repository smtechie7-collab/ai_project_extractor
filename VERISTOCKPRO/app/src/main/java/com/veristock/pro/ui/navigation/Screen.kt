
package com.veristock.pro.ui.navigation

sealed class Screen(val route: String) {
    object Setup : Screen("setup")
    object Home : Screen("home")
    object ProductList : Screen("product_list")
    object ProductForm : Screen("product_form/{productId}") {
        fun createRoute(productId: Long = 0) = "product_form/$productId"
    }
    object CustomerList : Screen("customer_list")
    object Billing : Screen("billing")
    object SalesList : Screen("sales_list")
    object SaleDetail : Screen("sale_detail/{saleId}") {
        fun createRoute(saleId: Long) = "sale_detail/$saleId"
    }
    object ReportsDashboard : Screen("reports_dashboard")
    object DateRangeReport : Screen("date_range_report")

    // Updated Settings Section
    object SettingsDashboard : Screen("settings_dashboard")
    object InvoiceSettings : Screen("invoice_settings")
    object PrinterSettings : Screen("printer_settings")
    object PrinterDiscovery : Screen("printer_discovery")
}