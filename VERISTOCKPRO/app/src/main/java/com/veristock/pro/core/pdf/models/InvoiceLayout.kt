package com.veristock.pro.core.pdf.models

import android.graphics.RectF

data class InvoiceLayout(
    // Page dimensions
    val pageHeight: Float,
    val pageWidth: Float,
    val margin: Float,

    // Section Y positions (where each section should START drawing)
    val headerStartY: Float,
    val customerInfoStartY: Float,
    val tableStartY: Float,
    val totalsStartY: Float,
    val footerStartY: Float,

    // Detailed table layout
    val tableLayout: TableLayout
)

data class TableLayout(
    val columnWidths: List<Float>,
    val columnXPositions: List<Float>,
    val headerHeight: Float,
    val rowHeights: List<Float>,
    val totalHeight: Float,
    val rowYPositions: List<Float>,
    val tableHeaderY: Float,
    val tableBodyY: Float
)

// A helper class to hold the dimensions of a single cell
data class CellRect(val rect: RectF, val text: String)
