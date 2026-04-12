
package com.veristock.pro.domain.model

import java.math.BigDecimal

data class SaleItem(
    val id: Long = 0,
    val saleId: Long = 0,
    val productId: Long,

    val productName: String,
    val productHsn: String? = null,
    val productCategory: String? = null,

    val quantity: Int,
    val unit: String = "Piece",

    // Financial fields now use BigDecimal for precision
    val mrp: BigDecimal?,
    val unitPrice: BigDecimal,
    val discountPercent: BigDecimal = BigDecimal.ZERO,
    val discountAmount: BigDecimal = BigDecimal.ZERO,
    val taxableValue: BigDecimal,

    val gstRate: BigDecimal,
    val cgstPercent: BigDecimal = BigDecimal.ZERO,
    val sgstPercent: BigDecimal = BigDecimal.ZERO,
    val igstPercent: BigDecimal = BigDecimal.ZERO,
    val cgstAmount: BigDecimal = BigDecimal.ZERO,
    val sgstAmount: BigDecimal = BigDecimal.ZERO,
    val igstAmount: BigDecimal = BigDecimal.ZERO,
    val totalTax: BigDecimal,

    val totalAmount: BigDecimal,

    val imeiNumbers: String? = null,
    val serialNumbers: String? = null,

    val createdAt: Long? = null
) {
    val imeiList: List<String>
        get() = imeiNumbers?.split(",")?.map { it.trim() } ?: emptyList()
}
