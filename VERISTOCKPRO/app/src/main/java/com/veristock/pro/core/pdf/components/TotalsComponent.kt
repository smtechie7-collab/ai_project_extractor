package com.veristock.pro.core.pdf.components

import android.graphics.Canvas
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.utils.IndianCurrencyFormatter
import com.veristock.pro.core.pdf.utils.PdfCanvasHelper

class TotalsComponent(
    private val canvas: Canvas,
    private val invoiceData: InvoiceData,
    private val layout: InvoiceLayout,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>,
    private val startY: Float
) {

    fun draw() {
        val bodyPaint = paints["body"] ?: TextPaint()
        val rightAlignX = layout.pageWidth - layout.margin
        val valueColumnWidth = 150f // A fixed width for the currency values
        val labelX = rightAlignX - valueColumnWidth
        var currentY = startY + 40f

        // Subtotal
        drawTotalLine("Subtotal:", invoiceData.totals.subtotal, labelX, rightAlignX, currentY, bodyPaint)
        currentY += 30f

        // GST Details
        if (invoiceData.totals.igst > 0) {
            drawTotalLine("IGST:", invoiceData.totals.igst, labelX, rightAlignX, currentY, bodyPaint)
            currentY += 30f
        } else {
            drawTotalLine("CGST:", invoiceData.totals.cgst, labelX, rightAlignX, currentY, bodyPaint)
            currentY += 30f
            drawTotalLine("SGST:", invoiceData.totals.sgst, labelX, rightAlignX, currentY, bodyPaint)
            currentY += 30f
        }
        
        PdfCanvasHelper.drawHorizontalLine(canvas, labelX, rightAlignX, currentY, paints["border"] ?: TextPaint())
        currentY += 30f

        // Grand Total
        val totalPaint = paints["header"] ?: TextPaint()
        drawTotalLine("Total:", invoiceData.totals.grandTotal, labelX, rightAlignX, currentY, totalPaint)
        currentY += 50f

        // Amount in Words
        if (template.type != com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL) {
            val amountInWordsLayout = createStaticLayout(invoiceData.totals.amountInWords, (layout.pageWidth - layout.margin * 2).toInt(), totalPaint)
            canvas.save()
            canvas.translate(layout.margin, currentY)
            amountInWordsLayout.draw(canvas)
            canvas.restore()
        }
    }

    private fun drawTotalLine(label: String, value: Double, labelX: Float, valueX: Float, y: Float, paint: TextPaint) {
        val formattedValue = IndianCurrencyFormatter.format(value)
        canvas.drawText(label, labelX, y, paint)
        PdfCanvasHelper.drawTextRight(canvas, formattedValue, valueX, y, paint)
    }

    companion object {
        fun measureHeight(invoiceData: InvoiceData, template: InvoiceTemplate, paints: Map<String, TextPaint>, width: Float): Float {
            var height = 40f // top padding
            height += 30f // subtotal
            height += if (invoiceData.totals.igst > 0) 30f else 60f // tax lines
            height += 30f // separator
            height += 30f // total
            height += 50f // padding

            if (template.type != com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL) {
                val totalPaint = paints["header"] ?: TextPaint()
                val amountInWordsLayout = createStaticLayout(invoiceData.totals.amountInWords, (width - 80f).toInt(), totalPaint)
                height += amountInWordsLayout.height
            }
            return height + 20f // bottom padding
        }

        private fun createStaticLayout(text: String, width: Int, paint: TextPaint): StaticLayout {
             return StaticLayout.Builder
                .obtain(text, 0, text.length, paint, width)
                .setAlignment(Layout.Alignment.ALIGN_NORMAL)
                .build()
        }
    }
}
