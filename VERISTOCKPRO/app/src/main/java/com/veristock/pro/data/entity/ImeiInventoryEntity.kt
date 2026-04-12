package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

/**
 * Tracks individual unique items (Smartphones, Laptops) by IMEI/Serial.
 */
@Entity(
    tableName = "imei_inventory",
    foreignKeys = [
        ForeignKey(
            entity = ProductEntity::class,
            parentColumns = ["id"],
            childColumns = ["product_id"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = SaleEntity::class,
            parentColumns = ["id"],
            childColumns = ["sale_id"],
            onDelete = ForeignKey.SET_NULL
        ),
        ForeignKey(
            entity = SaleItemEntity::class,
            parentColumns = ["id"],
            childColumns = ["sale_item_id"],
            onDelete = ForeignKey.SET_NULL
        ),
        ForeignKey(
            entity = CustomerEntity::class,
            parentColumns = ["id"],
            childColumns = ["sold_to_customer_id"],
            onDelete = ForeignKey.SET_NULL
        )
    ],
    indices = [
        Index(value = ["imei_number"], unique = true),
        Index(value = ["product_id"]),
        Index(value = ["status"]),
        Index(value = ["sale_id"]),
        Index(value = ["sale_item_id"]),       // Added Index
        Index(value = ["sold_to_customer_id"]) // Added Index
    ]
)
data class ImeiInventoryEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    @ColumnInfo(name = "product_id")
    val productId: Int,

    // Identifiers
    @ColumnInfo(name = "imei_number")
    val imeiNumber: String,
    @ColumnInfo(name = "serial_number")
    val serialNumber: String?,

    // Status
    @ColumnInfo(defaultValue = "IN_STOCK")
    val status: String = "IN_STOCK", // IN_STOCK, SOLD, RETURNED

    // Acquisition
    @ColumnInfo(name = "acquired_date")
    val acquiredDate: Long,
    @ColumnInfo(name = "acquisition_source", defaultValue = "PURCHASE")
    val acquisitionSource: String = "PURCHASE",
    @ColumnInfo(name = "purchase_price")
    val purchasePrice: Double?,

    // Sale Info
    @ColumnInfo(name = "sale_id")
    val saleId: Int?,
    @ColumnInfo(name = "sale_item_id")
    val saleItemId: Int?,
    @ColumnInfo(name = "sale_date")
    val saleDate: Long?,
    @ColumnInfo(name = "sale_price")
    val salePrice: Double?,
    @ColumnInfo(name = "sold_to_customer_id")
    val soldToCustomerId: Int?,

    // Warranty
    @ColumnInfo(name = "warranty_start_date")
    val warrantyStartDate: Long?,
    @ColumnInfo(name = "warranty_end_date")
    val warrantyEndDate: Long?,
    @ColumnInfo(name = "warranty_card_number")
    val warrantyCardNumber: String?,

    // Condition
    @ColumnInfo(name = "condition_on_receipt", defaultValue = "NEW")
    val conditionOnReceipt: String = "NEW",
    @ColumnInfo(name = "current_condition", defaultValue = "GOOD")
    val currentCondition: String = "GOOD",

    val notes: String?,

    @ColumnInfo(name = "created_at")
    val createdAt: Long,
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long
)