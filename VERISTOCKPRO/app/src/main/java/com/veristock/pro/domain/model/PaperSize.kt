package com.veristock.pro.domain.model

enum class PaperSize(
    val widthPoints: Float,
    val heightPoints: Float,
    val displayName: String
) {
    A4(595f, 842f, "A4 (210×297mm)"),
    A5(420f, 595f, "A5 (148×210mm)"),
    THERMAL_80MM(226f, Float.MAX_VALUE, "Thermal 80mm"),
    THERMAL_58MM(164f, Float.MAX_VALUE, "Thermal 58mm"),
    CUSTOM(0f, 0f, "Custom Size")
}
