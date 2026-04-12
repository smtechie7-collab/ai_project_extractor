package com.veristock.pro.domain.model

enum class Orientation {
    PORTRAIT,   // Vertical
    LANDSCAPE   // Horizontal
}

data class Margins(
    val top: Float,
    val right: Float,
    val bottom: Float,
    val left: Float
) {
    companion object {
        val DEFAULT = Margins(30f, 30f, 30f, 30f)
        val NARROW = Margins(20f, 20f, 20f, 20f)
        val THERMAL = Margins(10f, 5f, 10f, 5f)  // Tight margins for thermal
    }
}

data class PaperSettings(
    val paperSize: PaperSize,
    val customWidth: Float? = null,    // For CUSTOM size
    val customHeight: Float? = null,   // For CUSTOM size
    val orientation: Orientation = Orientation.PORTRAIT,
    val margins: Margins = Margins.DEFAULT
)
