
package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "sale_items",
    foreignKeys = [
        ForeignKey(
            entity = SaleEntity::class,
            parentColumns = ["id"],
            childColumns = ["sale_id"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = ProductEntity::class,
            parentColumns = ["id"],
            childColumns = ["product_id"],
            onDelete = ForeignKey.RESTRICT
        )
    ],
    indices = [
        Index(value = ["sale_id"]),
        Index(value = ["product_id"])
    ]
)
data class SaleItemEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    @ColumnInfo(name = "sale_id")
    val saleId: Int,
    @ColumnInfo(name = "product_id")
    val productId: Int,

    @ColumnInfo(name = "product_name")
    val productName: String,
    @ColumnInfo(name = "product_hsn")
    val productHsn: String?,
    @ColumnInfo(name = "product_category")
    val productCategory: String?,

    val quantity: Int,
    @ColumnInfo(defaultValue = "Piece")
    val unit: String = "Piece",

    // Financial fields are now stored as String to maintain precision.
    val mrp: String?,
    @ColumnInfo(name = "unit_price")
    val unitPrice: String,

    @ColumnInfo(name = "discount_percent", defaultValue = "0")
    val discountPercent: String = "0.0",
    @ColumnInfo(name = "discount_amount", defaultValue = "0")
    val discountAmount: String = "0.0",

    @ColumnInfo(name = "taxable_value")
    val taxableValue: String,

    @ColumnInfo(name = "gst_rate")
    val gstRate: String,
    @ColumnInfo(name = "cgst_percent", defaultValue = "0")
    val cgstPercent: String = "0.0",
    @ColumnInfo(name = "sgst_percent", defaultValue = "0")
    val sgstPercent: String = "0.0",
    @ColumnInfo(name = "igst_percent", defaultValue = "0")
    val igstPercent: String = "0.0",

    @ColumnInfo(name = "cgst_amount", defaultValue = "0")
    val cgstAmount: String = "0.0",
    @ColumnInfo(name = "sgst_amount", defaultValue = "0")
    val sgstAmount: String = "0.0",
    @ColumnInfo(name = "igst_amount", defaultValue = "0")
    val igstAmount: String = "0.0",

    @ColumnInfo(name = "total_tax")
    val totalTax: String,

    @ColumnInfo(name = "total_amount")
    val totalAmount: String,

    @ColumnInfo(name = "imei_numbers")
    val imeiNumbers: String?,
    @ColumnInfo(name = "serial_numbers")
    val serialNumbers: String?,

    @ColumnInfo(name = "created_at")
    val createdAt: Long
)
