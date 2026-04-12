package com.veristock.pro.core.pdf.renderers

import android.graphics.Canvas
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate

interface BaseRenderer {
    fun render(
        canvas: Canvas,
        invoiceData: InvoiceData,
        layout: InvoiceLayout,
        template: InvoiceTemplate,
        paints: Map<String, TextPaint>
    )
}
