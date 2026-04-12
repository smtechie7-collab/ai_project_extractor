package com.veristock.pro.core.pdf.components

import android.graphics.Canvas
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.utils.BitmapHelper
import com.veristock.pro.core.pdf.utils.PdfCanvasHelper

class FooterComponent(
    private val canvas: Canvas,
    private val invoiceData: InvoiceData,
    private val layout: InvoiceLayout,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>,
    private val startY: Float
) {

    fun draw() {
        when (template.type) {
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> drawTraditionalFooter()
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> drawModernFooter()
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> drawGstFormalFooter()
        }
    }

    private fun drawTraditionalFooter() {
        val bodyPaint = paints["body"] ?: TextPaint()
        val centerX = layout.pageWidth / 2f
        var currentY = startY

        canvas.drawText("Payment: ${invoiceData.payment.method}", layout.margin, currentY, bodyPaint)
        PdfCanvasHelper.drawTextRight(canvas, "Status: ${invoiceData.payment.status}", layout.pageWidth - layout.margin, currentY, bodyPaint)
        currentY += 40f

        PdfCanvasHelper.drawDashedLine(canvas, layout.margin, layout.pageWidth - layout.margin, currentY, paints["border"] ?: TextPaint())
        currentY += 40f

        PdfCanvasHelper.drawTextCentered(canvas, template.footerMessage, centerX, currentY, bodyPaint)
        currentY += 25f
        PdfCanvasHelper.drawTextCentered(canvas, invoiceData.legal.termsAndConditions, centerX, currentY, bodyPaint)
    }

    private fun drawModernFooter() {
        // ... implementation ...
    }

    private fun drawGstFormalFooter() {
        // ... implementation ...
    }

    companion object {
        fun measureHeight(invoiceData: InvoiceData, template: InvoiceTemplate, paints: Map<String, TextPaint>): Float {
            var height = 0f
            when (template.type) {
                com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> {
                    height += 40f // payment
                    height += 40f // line
                    height += 25f // footer msg
                    height += 25f // terms
                    height += 20f // bottom padding
                }
                com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> {
                    height += 25f + 25f + 25f // payment info
                    val qrCodeHeight = if(invoiceData.payment.qrCode != null) 150f else 0f
                    val termsHeight = 80f
                    height += maxOf(qrCodeHeight, termsHeight) + 40f
                }
                com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> {
                    if (invoiceData.payment.bankDetails != null) height += 120f
                    if (invoiceData.legal.declaration != null) height += 60f
                    height += 80f // Signatures
                    height += 20f
                }
            }
            return height
        }
    }
}
