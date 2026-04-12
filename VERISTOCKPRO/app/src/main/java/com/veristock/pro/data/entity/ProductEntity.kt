
package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "products",
    indices = [
        Index(value = ["category"]),
        Index(value = ["brand"]),
        Index(value = ["barcode"], unique = true),
        Index(value = ["is_active"]),
        Index(value = ["sku"], unique = true)
    ]
)
data class ProductEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    val name: String,
    val description: String?,

    val category: String,
    val brand: String?,
    val model: String?,

    val sku: String?,
    @ColumnInfo(name = "hsn_code", defaultValue = "8517")
    val hsnCode: String = "8517",
    val barcode: String?,

    // Financial fields now stored as String for precision
    val mrp: String,
    @ColumnInfo(name = "selling_price")
    val sellingPrice: String,
    @ColumnInfo(name = "purchase_price")
    val purchasePrice: String?,

    @ColumnInfo(name = "gst_rate", defaultValue = "18.0")
    val gstRate: String = "18.0",

    @ColumnInfo(name = "current_stock", defaultValue = "0")
    val currentStock: Int = 0,
    @ColumnInfo(name = "min_stock_level", defaultValue = "5")
    val minStockLevel: Int = 5,
    @ColumnInfo(name = "max_stock_level", defaultValue = "100")
    val maxStockLevel: Int = 100,

    @ColumnInfo(defaultValue = "Piece")
    val unit: String = "Piece",

    @ColumnInfo(name = "has_imei", defaultValue = "0")
    val hasImei: Boolean = false,
    @ColumnInfo(name = "has_serial", defaultValue = "0")
    val hasSerial: Boolean = false,
    @ColumnInfo(name = "warranty_months", defaultValue = "0")
    val warrantyMonths: Int = 0,

    @ColumnInfo(name = "is_active", defaultValue = "1")
    val isActive: Boolean = true,
    @ColumnInfo(name = "is_featured", defaultValue = "0")
    val isFeatured: Boolean = false,

    @ColumnInfo(name = "image_path")
    val imagePath: String?,

    val notes: String?,
    @ColumnInfo(name = "created_at")
    val createdAt: Long,
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long
)
