
package com.veristock.pro.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.veristock.pro.core.print.model.PrintJobStatus
import com.veristock.pro.core.print.model.PrintJobType

/**
 * Represents a print job stored in the local Room database.
 */
@Entity(tableName = "print_jobs")
data class PrintJobEntity(
    @PrimaryKey
    val id: String,
    val type: PrintJobType,
    /**
     * A string reference to the data, e.g., the invoice ID or sale ID.
     * The PrintJobManager will use this to query the actual data object.
     */
    val dataIdentifier: String,
    val printerAddress: String,
    var status: PrintJobStatus,
    val createdAt: Long,
    var attempts: Int,
    var lastError: String?
)
