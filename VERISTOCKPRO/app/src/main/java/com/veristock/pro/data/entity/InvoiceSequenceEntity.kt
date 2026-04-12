package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Persistence for invoice numbering to prevent duplicates/gaps during crashes.
 */
@Entity(tableName = "invoice_sequences")
data class InvoiceSequenceEntity(
    @PrimaryKey
    val id: Int = 1, // Only one row

    @ColumnInfo(name = "last_invoice_number")
    val lastInvoiceNumber: String?,

    @ColumnInfo(name = "last_invoice_counter", defaultValue = "0")
    val lastInvoiceCounter: Int = 0,

    @ColumnInfo(name = "last_generated_at")
    val lastGeneratedAt: Long?
)