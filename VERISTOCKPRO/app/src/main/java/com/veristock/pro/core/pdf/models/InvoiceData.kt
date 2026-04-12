package com.veristock.pro.core.pdf.models

import java.io.File

data class InvoiceData(
    val business: BusinessHeaderData,
    val customer: CustomerData,
    val sale: SaleData,
    val items: List<SaleItemData>,
    val totals: TotalsData,
    val payment: PaymentData,
    val legal: LegalData
)

data class BusinessHeaderData(
    val businessName: String,
    val tagline: String?,
    val address: String,
    val mobile: String,
    val email: String?,
    val gstin: String?,
    val logo: File?,
    val cin: String?, // For GST Formal
    val pan: String? // For GST Formal
)

data class CustomerData(
    val name: String,
    val mobile: String?,
    val email: String?,
    val billingAddress: String,
    val shippingAddress: String,
    val gstin: String?
)

data class SaleData(
    val invoiceNumber: String,
    val date: String,
    val placeOfSupply: String?,
    val reverseCharge: Boolean = false
)

data class SaleItemData(
    val serialNumber: Int,
    val description: String,
    val hsn: String?,
    val imei: String?,
    val quantity: Double,
    val rate: Double,
    val gstRate: Double, // Combined GST rate
    val amount: Double
)

data class TotalsData(
    val subtotal: Double,
    val cgst: Double,
    val sgst: Double,
    val igst: Double,
    val totalTax: Double,
    val grandTotal: Double,
    val amountInWords: String,
    val taxAmountInWords: String
)

data class PaymentData(
    val method: String,
    val transactionId: String?,
    val status: String, // e.g., PAID, DUE
    val qrCode: File?,
    val bankDetails: BankDetails?
)

data class BankDetails(
    val bankName: String,
    val accountNumber: String,
    val ifscCode: String,
    val branch: String
)

data class LegalData(
    val termsAndConditions: String,
    val declaration: String?
)
