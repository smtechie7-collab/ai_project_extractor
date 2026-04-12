package com.veristock.pro.core.pdf.models

import com.veristock.pro.domain.model.PaperSize

enum class InvoiceTemplateType {
    TRADITIONAL,    // Style 1: Kirana style
    MODERN,         // Style 2: Professional
    GST_FORMAL      // Style 3: Government format
}

data class InvoiceTemplate(
    val type: InvoiceTemplateType,
    val pageSize: PaperSize = PaperSize.A4,
    val showLogo: Boolean,
    val tagline: String?,
    val borderStyle: BorderStyle,
    val fontSize: FontSize,
    val colorScheme: ColorScheme,
    val footerMessage: String,
    val showDecorations: Boolean,
    val useRegionalLanguage: Boolean,
    val regionalLanguage: String? // "hi", "mr", "ta" etc.
)

enum class BorderStyle {
    NONE,           // No borders
    SIMPLE,         // Single line borders
    DOUBLE_LINE,    // Double line borders
    DECORATIVE      // Dotted/dashed decorative
}

enum class FontSize {
    SMALL,    // Compact for thermal
    MEDIUM,   // Standard A4
    LARGE     // Easy reading
}

enum class ColorScheme {
    BLACK_WHITE,     // Pure B&W
    GRAYSCALE,       // Shades of gray
    BRAND_COLORS     // Use business brand colors
}
