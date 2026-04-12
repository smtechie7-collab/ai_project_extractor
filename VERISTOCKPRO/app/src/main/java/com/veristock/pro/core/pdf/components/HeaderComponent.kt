package com.veristock.pro.core.pdf.components

import android.graphics.Canvas
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.utils.BitmapHelper
import com.veristock.pro.core.pdf.utils.PdfCanvasHelper
import com.veristock.pro.core.pdf.utils.TextMeasurement

class HeaderComponent(
    private val canvas: Canvas,
    private val invoiceData: InvoiceData,
    private val layout: InvoiceLayout,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>,
    private val startY: Float
) {

    fun draw() {
        when (template.type) {
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> drawTraditionalHeader()
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> drawModernHeader()
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> drawGstFormalHeader()
        }
    }

    private fun drawTraditionalHeader() {
        val titlePaint = paints["title"] ?: TextPaint()
        val bodyPaint = paints["body"] ?: TextPaint()
        val centerX = layout.pageWidth / 2f
        var currentY = startY + Spacing.TRADITIONAL_TOP_PADDING

        PdfCanvasHelper.drawTextCentered(canvas, "★ ★ ★ ${invoiceData.business.businessName} ★ ★ ★", centerX, currentY, titlePaint)
        currentY += TextMeasurement.getTextHeight("H", titlePaint) + Spacing.TRADITIONAL_TITLE_GAP

        invoiceData.business.tagline?.let {
            PdfCanvasHelper.drawTextCentered(canvas, it, centerX, currentY, bodyPaint)
            currentY += Spacing.TRADITIONAL_LINE_GAP
        }

        PdfCanvasHelper.drawTextCentered(canvas, invoiceData.business.address, centerX, currentY, bodyPaint)
        currentY += Spacing.TRADITIONAL_LINE_GAP
        PdfCanvasHelper.drawTextCentered(canvas, "Mobile: ${invoiceData.business.mobile}", centerX, currentY, bodyPaint)
        currentY += Spacing.TRADITIONAL_LINE_GAP
        invoiceData.business.gstin?.let {
             PdfCanvasHelper.drawTextCentered(canvas, "GSTIN: $it", centerX, currentY, bodyPaint)
        }
    }

    private fun drawModernHeader() {
        val titlePaint = paints["title"] ?: TextPaint()
        val bodyPaint = paints["body"] ?: TextPaint()
        val headerPaint = paints["header"] ?: TextPaint()
        var currentY = startY + Spacing.MODERN_TOP_PADDING
        val startX = layout.margin
        val logoWidth = 120f
        val logoHeight = 120f

        if (template.showLogo) {
            invoiceData.business.logo?.let { logoFile ->
                BitmapHelper.getScaledBitmap(logoFile, logoWidth.toInt(), logoHeight.toInt())?.let {
                    canvas.drawBitmap(it, startX, currentY, null)
                }
            }
        }
        
        PdfCanvasHelper.drawTextRight(canvas, "INVOICE", layout.pageWidth - layout.margin, currentY + Spacing.MODERN_LINE_GAP, headerPaint)

        val textStartX = if (template.showLogo && invoiceData.business.logo != null) startX + logoWidth + 20f else startX
        canvas.drawText(invoiceData.business.businessName, textStartX, currentY, titlePaint)
        currentY += Spacing.MODERN_LINE_GAP
        canvas.drawText(invoiceData.business.address, textStartX, currentY, bodyPaint)
        currentY += Spacing.MODERN_LINE_GAP
        canvas.drawText("Email: ${invoiceData.business.email} | Mobile: ${invoiceData.business.mobile}", textStartX, currentY, bodyPaint)
        currentY += Spacing.MODERN_LINE_GAP
        invoiceData.business.gstin?.let {
            canvas.drawText("GSTIN: $it", textStartX, currentY, bodyPaint)
        }
    }

    private fun drawGstFormalHeader() {
        // Implementation similar to others...
    }
    
    private object Spacing {
        const val TRADITIONAL_TOP_PADDING = 60f
        const val TRADITIONAL_BOTTOM_PADDING = 40f
        const val TRADITIONAL_TITLE_GAP = 40f
        const val TRADITIONAL_LINE_GAP = 25f
        
        const val MODERN_TOP_PADDING = 40f
        const val MODERN_BOTTOM_PADDING = 60f
        const val MODERN_LINE_GAP = 25f
    }

    companion object {
        fun measureHeight(invoiceData: InvoiceData, template: InvoiceTemplate, paints: Map<String, TextPaint>): Float {
            val titlePaint = paints["title"] ?: TextPaint()
            var height = 0f

            when (template.type) {
                com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> {
                    height += Spacing.TRADITIONAL_TOP_PADDING
                    height += TextMeasurement.getTextHeight("H", titlePaint) + Spacing.TRADITIONAL_TITLE_GAP
                    invoiceData.business.tagline?.let { height += Spacing.TRADITIONAL_LINE_GAP }
                    height += Spacing.TRADITIONAL_LINE_GAP // address
                    height += Spacing.TRADITIONAL_LINE_GAP // mobile
                    invoiceData.business.gstin?.let { height += Spacing.TRADITIONAL_LINE_GAP }
                    height += Spacing.TRADITIONAL_BOTTOM_PADDING
                }
                com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> {
                    val hasLogo = template.showLogo && invoiceData.business.logo != null
                    var textBlockHeight = Spacing.MODERN_LINE_GAP * 3 // name, address, contact, gstin
                     invoiceData.business.gstin?.let { textBlockHeight += Spacing.MODERN_LINE_GAP }
                    val logoHeight = if(hasLogo) 120f else 0f
                    height += maxOf(logoHeight, textBlockHeight) + Spacing.MODERN_TOP_PADDING + Spacing.MODERN_BOTTOM_PADDING
                }
                com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> {
                    height = 250f // Keep as approximation for now
                }
            }
            return height
        }
    }
}
