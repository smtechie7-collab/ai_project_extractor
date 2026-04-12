package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

/**
 * Audit trail for all stock changes.
 */
@Entity(
    tableName = "stock_movements",
    foreignKeys = [
        ForeignKey(
            entity = ProductEntity::class,
            parentColumns = ["id"],
            childColumns = ["product_id"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = ImeiInventoryEntity::class,
            parentColumns = ["id"],
            childColumns = ["imei_id"],
            onDelete = ForeignKey.SET_NULL
        )
    ],
    indices = [
        Index(value = ["product_id"]),
        Index(value = ["movement_date"]), // For history sorting
        Index(value = ["movement_type"]),
        Index(value = ["imei_id"])        // Added Index
    ]
)
data class StockMovementEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    @ColumnInfo(name = "product_id")
    val productId: Int,

    // Movement Details
    @ColumnInfo(name = "movement_type")
    val movementType: String, // SALE, PURCHASE, RETURN, ADJUSTMENT
    @ColumnInfo(name = "reference_type")
    val referenceType: String?,
    @ColumnInfo(name = "reference_id")
    val referenceId: Int?,
    @ColumnInfo(name = "reference_number")
    val referenceNumber: String?,

    // Quantity
    @ColumnInfo(name = "quantity_change")
    val quantityChange: Int, // + for IN, - for OUT
    @ColumnInfo(name = "stock_before")
    val stockBefore: Int,
    @ColumnInfo(name = "stock_after")
    val stockAfter: Int,

    // IMEI Reference
    @ColumnInfo(name = "imei_id")
    val imeiId: Int?,
    @ColumnInfo(name = "imei_number")
    val imeiNumber: String?,

    // Details
    @ColumnInfo(name = "movement_date")
    val movementDate: Long,
    val remarks: String?,

    @ColumnInfo(name = "created_by", defaultValue = "OWNER")
    val createdBy: String = "OWNER",

    @ColumnInfo(name = "created_at")
    val createdAt: Long
)