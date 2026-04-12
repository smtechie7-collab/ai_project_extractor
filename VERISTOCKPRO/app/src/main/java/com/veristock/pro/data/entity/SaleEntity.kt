
package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "sales",
    foreignKeys = [
        ForeignKey(
            entity = CustomerEntity::class,
            parentColumns = ["id"],
            childColumns = ["customer_id"],
            onDelete = ForeignKey.RESTRICT
        )
    ],
    indices = [
        Index(value = ["invoice_number"], unique = true),
        Index(value = ["invoice_date"]), // Often accessed for sorting
        Index(value = ["customer_id"]),
        Index(value = ["payment_status"])
    ]
)
data class SaleEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    @ColumnInfo(name = "invoice_number")
    val invoiceNumber: String,
    @ColumnInfo(name = "invoice_date")
    val invoiceDate: Long,

    @ColumnInfo(name = "customer_id")
    val customerId: Int?,
    @ColumnInfo(name = "customer_name")
    val customerName: String,
    @ColumnInfo(name = "customer_mobile")
    val customerMobile: String?,
    @ColumnInfo(name = "customer_gstin")
    val customerGstin: String?,
    @ColumnInfo(name = "customer_address")
    val customerAddress: String?,
    @ColumnInfo(name = "customer_state")
    val customerState: String?,

    // Financial fields are now stored as String to maintain precision.
    // A TypeConverter will handle the BigDecimal <-> String conversion.
    val subtotal: String,

    @ColumnInfo(name = "discount_type", defaultValue = "NONE")
    val discountType: String = "NONE",
    @ColumnInfo(name = "discount_percent", defaultValue = "0")
    val discountPercent: String = "0.0",
    @ColumnInfo(name = "discount_amount", defaultValue = "0")
    val discountAmount: String = "0.0",

    @ColumnInfo(name = "taxable_amount")
    val taxableAmount: String,
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
    @ColumnInfo(name = "round_off", defaultValue = "0")
    val roundOff: String = "0.0",
    @ColumnInfo(name = "grand_total")
    val grandTotal: String,

    @ColumnInfo(name = "payment_mode")
    val paymentMode: String,
    @ColumnInfo(name = "payment_status", defaultValue = "PAID")
    val paymentStatus: String = "PAID",
    @ColumnInfo(name = "paid_amount", defaultValue = "0")
    val paidAmount: String = "0.0",

    @ColumnInfo(name = "payment_reference")
    val paymentReference: String?,
    @ColumnInfo(name = "payment_details_json")
    val paymentDetailsJson: String?,

    @ColumnInfo(name = "sale_type", defaultValue = "B2C")
    val saleType: String = "B2C",
    @ColumnInfo(name = "invoice_type", defaultValue = "RETAIL")
    val invoiceType: String = "RETAIL",

    @ColumnInfo(name = "print_count", defaultValue = "0")
    val printCount: Int = 0,
    @ColumnInfo(name = "last_print_time")
    val lastPrintTime: Long?,
    @ColumnInfo(name = "is_shared", defaultValue = "0")
    val isShared: Boolean = false,
    @ColumnInfo(name = "shared_at")
    val sharedAt: Long?,

    val notes: String?,
    @ColumnInfo(name = "internal_notes")
    val internalNotes: String?,

    @ColumnInfo(name = "created_by", defaultValue = "OWNER")
    val createdBy: String = "OWNER",

    @ColumnInfo(name = "created_at")
    val createdAt: Long,
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long
)
