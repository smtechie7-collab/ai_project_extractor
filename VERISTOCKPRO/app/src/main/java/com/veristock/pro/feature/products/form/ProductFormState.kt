
package com.veristock.pro.feature.products.form

/**
 * Represents the state of the Product Form UI.
 * Uses String for all input fields to accommodate TextField state
 * and allow for intermediate invalid user input.
 */
data class ProductFormState(
    // Product Data
    val id: Long = 0,
    val name: String = "",
    val category: String = "",
    val brand: String = "",
    val model: String = "",
    val hsnCode: String = "",
    val barcode: String = "",
    val mrp: String = "",
    val sellingPrice: String = "",
    val purchasePrice: String = "",
    val gstRate: String = "18", // Default GST
    val currentStock: String = "",
    val minStockLevel: String = "",
    val unit: String = "Piece",
    val hasImei: Boolean = false,
    val hasSerial: Boolean = false,
    val warrantyMonths: String = "",

    // Validation Errors
    val nameError: String? = null,
    val categoryError: String? = null,
    val mrpError: String? = null,
    val sellingPriceError: String? = null,
    val gstRateError: String? = null,
    val stockError: String? = null,
    val minStockError: String? = null,

    // UI Control State
    val isLoading: Boolean = false,
    val isSaved: Boolean = false,
    val errorMessage: String? = null
)
