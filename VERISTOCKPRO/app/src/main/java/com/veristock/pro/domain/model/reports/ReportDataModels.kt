package com.veristock.pro.domain.model.reports

// --- Sales Report Data ---

data class SalesReportRow(
    val date: Long,
    val invoiceNumber: String,
    val customerName: String,
    val itemCount: Int,
    val subtotal: Double,
    val taxAmount: Double,
    val grandTotal: Double,
    val paymentMode: String,
    val paymentStatus: String
)

data class SalesSummaryByDay(
    val date: String, // Changed to String to avoid API 26 issues with Room
    val totalSales: Double,
    val transactionCount: Int,
    val averageTicketSize: Double,
    val cashSales: Double,
    val digitalSales: Double
)

// --- Product Report Data ---

data class ProductSalesRow(
    val productId: Long,
    val productName: String,
    val category: String,
    val brand: String?,
    val quantitySold: Int,
    val revenue: Double,
    val costOfGoods: Double,
    val profit: Double,
    val profitMargin: Double,  // percentage
    val currentStock: Int
)

data class TopProduct(
    val productId: Long,
    val productName: String,
    val value: Double,  // Revenue or Quantity or Profit
    val rank: Int,
    val percentageOfTotal: Double
)

// --- GST Report Data ---

data class GstSummary(
    val cgstTotal: Double,
    val sgstTotal: Double,
    val igstTotal: Double,
    val totalTaxCollected: Double,
    val breakdownByRate: List<TaxRateBreakdown>
)

data class TaxRateBreakdown(
    val gstRate: Double,
    val taxableAmount: Double,
    val cgst: Double,
    val sgst: Double,
    val igst: Double,
    val totalTax: Double,
    val invoiceCount: Int
)

data class Gstr1Row(
    val invoiceNumber: String,
    val invoiceDate: Long,
    val customerGstin: String?,
    val customerName: String,
    val customerState: String,
    val invoiceType: String,  // B2B, B2C_LARGE, B2C_SMALL
    val taxableValue: Double,
    val cgst: Double,
    val sgst: Double,
    val igst: Double,
    val invoiceValue: Double
)

// --- Customer Report Data ---

data class CustomerPurchaseRow(
    val customerId: Long,
    val customerName: String,
    val customerMobile: String,
    val totalPurchases: Double,
    val purchaseCount: Int,
    val averageOrderValue: Double,
    val firstPurchaseDate: Long,
    val lastPurchaseDate: Long,
    val outstandingBalance: Double
)

data class CustomerSegment(
    val segmentName: String,
    val customerCount: Int,
    val totalRevenue: Double,
    val percentageOfRevenue: Double,
    val averageLifetimeValue: Double
)
