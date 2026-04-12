package com.veristock.pro.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "invoice_pdf_metadata")
data class InvoicePdfMetadataEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val saleId: Long,
    val generatedAt: Long,
    val templateType: String,
    val paperSize: String,
    val copyTypes: String,
    val fileSize: Long,
    val filePath: String,
    val regenerationCount: Int
)
