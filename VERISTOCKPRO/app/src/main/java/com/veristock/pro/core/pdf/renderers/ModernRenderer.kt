package com.veristock.pro.core.pdf.renderers

import android.graphics.Canvas
import android.graphics.Paint
import android.text.TextPaint
import com.veristock.pro.core.pdf.components.*
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate

class ModernRenderer : BaseRenderer {

    override fun render(
        canvas: Canvas,
        invoiceData: InvoiceData,
        layout: InvoiceLayout,
        template: InvoiceTemplate,
        paints: Map<String, TextPaint>
    ) {
        // Draw components in order, passing the calculated start Y positions
        HeaderComponent(canvas, invoiceData, layout, template, paints, layout.headerStartY).draw()
        CustomerInfoComponent(canvas, invoiceData, layout, template, paints, layout.customerInfoStartY).draw()
        TableComponent(canvas, invoiceData, layout, template, paints).draw()
        TotalsComponent(canvas, invoiceData, layout, template, paints, layout.totalsStartY).draw()
        FooterComponent(canvas, invoiceData, layout, template, paints, layout.footerStartY).draw()
        DecorationsComponent(canvas, layout, template, paints.mapValues { it.value as Paint }).draw()
    }
}
