
package com.veristock.pro.data.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey
import com.veristock.pro.core.print.model.PaperWidth

/**
 * Represents a saved printer profile in the Room database.
 * The deviceAddress is unique to prevent duplicate profiles for the same printer.
 */
@Entity(
    tableName = "printer_profiles",
    indices = [Index(value = ["deviceAddress"], unique = true)]
)
data class PrinterProfileEntity(
    @PrimaryKey
    val id: String,
    val name: String,
    val deviceAddress: String,
    val deviceName: String,
    val paperWidth: PaperWidth,
    val isDefault: Boolean
)
