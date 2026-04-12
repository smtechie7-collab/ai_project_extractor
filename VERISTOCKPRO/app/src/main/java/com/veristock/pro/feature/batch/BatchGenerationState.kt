package com.veristock.pro.feature.batch

import com.veristock.pro.domain.model.Sale

enum class OutputFormat {
    SINGLE_PDF,
    ZIP_FILE
}

data class BatchGenerationState(
    val startDate: Long = System.currentTimeMillis(),
    val endDate: Long = System.currentTimeMillis(),
    val selectedCustomerId: Int? = null,
    val outputFormat: OutputFormat = OutputFormat.ZIP_FILE,
    val matchingInvoiceCount: Int = 0,
    val isGenerating: Boolean = false,
    val progress: Float = 0f,
    val errorMessage: String? = null,
    val foundSales: List<Sale> = emptyList()
)
