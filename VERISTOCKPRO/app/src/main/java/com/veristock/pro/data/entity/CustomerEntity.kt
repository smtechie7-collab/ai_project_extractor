
package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "customers",
    indices = [
        Index(value = ["mobile"], unique = true),
        Index(value = ["gstin"])
    ]
)
data class CustomerEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    val name: String,
    val mobile: String,
    @ColumnInfo(name = "alternate_mobile")
    val alternateMobile: String?,
    val email: String?,

    val gstin: String?,
    @ColumnInfo(name = "business_name")
    val businessName: String?,

    @ColumnInfo(name = "address_line1")
    val addressLine1: String?,
    @ColumnInfo(name = "address_line2")
    val addressLine2: String?,
    val city: String?,
    val state: String?,
    val pincode: String?,

    // Financial fields now use String for precision
    @ColumnInfo(name = "credit_limit", defaultValue = "0")
    val creditLimit: String = "0.0",
    @ColumnInfo(name = "outstanding_balance", defaultValue = "0")
    val outstandingBalance: String = "0.0",

    @ColumnInfo(name = "total_purchases", defaultValue = "0")
    val totalPurchases: String = "0.0",

    @ColumnInfo(name = "total_orders", defaultValue = "0")
    val totalOrders: Int = 0,
    @ColumnInfo(name = "last_purchase_date")
    val lastPurchaseDate: Long?,

    val notes: String?,
    @ColumnInfo(name = "is_active", defaultValue = "1")
    val isActive: Boolean = true,
    @ColumnInfo(name = "created_at")
    val createdAt: Long,
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long
)
