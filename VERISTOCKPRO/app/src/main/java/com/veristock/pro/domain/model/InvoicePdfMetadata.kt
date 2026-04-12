package com.veristock.pro.domain.model

import com.veristock.pro.core.pdf.models.InvoiceTemplateType

data class InvoicePdfMetadata(
    val id: Long = 0,
    val saleId: Long,
    val generatedAt: Long = System.currentTimeMillis(),
    val templateType: String,
    val paperSize: String,
    val copyTypes: String, // Comma-separated list of copy types
    val fileSize: Long, // in bytes
    val filePath: String,
    val regenerationCount: Int = 0
)
