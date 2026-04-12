package com.veristock.pro.domain.model

import androidx.compose.ui.graphics.Color

data class CopySettings(
    val copyType: InvoiceCopyType,
    val headerText: String,           // "ORIGINAL FOR RECIPIE"NT"
    val watermarkText: String?,       // Optional watermark
    val watermarkOpacity: Float,      // 0.0 to 1.0
    val showInFooter: Boolean,        // Show copy type in footer
    val colorIndicator: Color?        // Different color per copy
)
