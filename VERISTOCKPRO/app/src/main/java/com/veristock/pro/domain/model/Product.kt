
package com.veristock.pro.domain.model

import java.math.BigDecimal
import java.math.RoundingMode

data class Product(
    val id: Int = 0,
    val name: String,
    val description: String? = null,

    val category: String,
    val brand: String? = null,
    val model: String? = null,

    val sku: String? = null,
    val hsnCode: String = "8517",
    val barcode: String? = null,

    // Financial fields now use BigDecimal
    val mrp: BigDecimal,
    val sellingPrice: BigDecimal,
    val purchasePrice: BigDecimal? = null,
    val gstRate: BigDecimal = BigDecimal("18.0"),

    val currentStock: Int = 0,
    val minStockLevel: Int = 5,
    val maxStockLevel: Int = 100,
    val unit: String = "Piece",

    val hasImei: Boolean = false,
    val hasSerial: Boolean = false,
    val warrantyMonths: Int = 0,

    val isActive: Boolean = true,
    val isFeatured: Boolean = false,

    val imagePath: String? = null,

    val notes: String? = null,
    val createdAt: Long? = null,
    val updatedAt: Long? = null
) {
    val isLowStock: Boolean
        get() = currentStock <= minStockLevel

    val isOutOfStock: Boolean
        get() = currentStock <= 0

    val profitMargin: BigDecimal?
        get() = purchasePrice?.let {
            if (it > BigDecimal.ZERO) {
                sellingPrice.subtract(it).divide(it, 4, RoundingMode.HALF_UP).multiply(BigDecimal(100))
            } else {
                BigDecimal.ZERO
            }
        }

    val hasWarranty: Boolean
        get() = warrantyMonths > 0
}
