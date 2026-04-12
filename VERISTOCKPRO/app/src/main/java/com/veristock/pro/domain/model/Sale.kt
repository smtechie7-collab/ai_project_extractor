
package com.veristock.pro.domain.model

import java.math.BigDecimal

data class Sale(
    val id: Long = 0,
    val invoiceNumber: String,
    val invoiceDate: Long,

    val customerId: Long? = null,
    val customerName: String,
    val customerMobile: String? = null,
    val customerGstin: String? = null,
    val customerAddress: String? = null,
    val customerState: String? = null,

    val items: List<SaleItem> = emptyList(),

    // Financial fields now use BigDecimal for precision
    val subtotal: BigDecimal,
    val discountType: String = "NONE",
    val discountPercent: BigDecimal = BigDecimal.ZERO,
    val discountAmount: BigDecimal = BigDecimal.ZERO,
    val taxableAmount: BigDecimal,

    val cgstAmount: BigDecimal = BigDecimal.ZERO,
    val sgstAmount: BigDecimal = BigDecimal.ZERO,
    val igstAmount: BigDecimal = BigDecimal.ZERO,
    val totalTax: BigDecimal,

    val totalAmount: BigDecimal,
    val roundOff: BigDecimal = BigDecimal.ZERO,
    val grandTotal: BigDecimal,

    val paymentMode: String,
    val paymentStatus: String = "PAID",
    val paidAmount: BigDecimal = BigDecimal.ZERO,
    val paymentReference: String? = null,
    val paymentDetailsJson: String? = null,

    val saleType: String = "B2C",
    val invoiceType: String = "RETAIL",
    val printCount: Int = 0,
    val lastPrintTime: Long? = null,
    val isShared: Boolean = false,
    val sharedAt: Long? = null,
    val notes: String? = null,
    val internalNotes: String? = null,
    val createdBy: String = "OWNER",
    val createdAt: Long? = null,
    val updatedAt: Long? = null
) {
    val isPaid: Boolean
        get() = paymentStatus == "PAID"

    val balance: BigDecimal
        get() = grandTotal.subtract(paidAmount)
}
