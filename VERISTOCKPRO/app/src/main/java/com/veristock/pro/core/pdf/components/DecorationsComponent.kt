package com.veristock.pro.core.pdf.components

import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.RectF
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.utils.PdfCanvasHelper

class DecorationsComponent(
    private val canvas: Canvas,
    private val layout: InvoiceLayout,
    private val template: InvoiceTemplate,
    private val paints: Map<String, Paint>
) {

    fun draw() {
        when (template.borderStyle) {
            com.veristock.pro.core.pdf.models.BorderStyle.SIMPLE -> drawSimpleBorder()
            com.veristock.pro.core.pdf.models.BorderStyle.DOUBLE_LINE -> drawDoubleLineBorder()
            com.veristock.pro.core.pdf.models.BorderStyle.DECORATIVE -> drawDecorativeBorder()
            else -> {}
        }

        if (template.showDecorations && template.type == com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL) {
            drawReligiousSymbols()
        }
    }

    private fun drawSimpleBorder() {
        // Safe get or default, forcing STROKE style to prevent filling the page black
        val borderPaint = (paints["border"] ?: Paint()).apply {
            style = Paint.Style.STROKE
            if (strokeWidth == 0f) strokeWidth = 1f
        }

        val rect = RectF(
            layout.margin,
            layout.margin,
            layout.pageWidth - layout.margin,
            layout.pageHeight - layout.margin
        )
        canvas.drawRect(rect, borderPaint)
    }

    private fun drawDoubleLineBorder() {
        val borderPaint = (paints["border"] ?: Paint()).apply {
            style = Paint.Style.STROKE
            if (strokeWidth == 0f) strokeWidth = 1f
        }

        val rect1 = RectF(
            layout.margin,
            layout.margin,
            layout.pageWidth - layout.margin,
            layout.pageHeight - layout.margin
        )
        val rect2 = RectF(
            layout.margin + 5,
            layout.margin + 5,
            layout.pageWidth - layout.margin - 5,
            layout.pageHeight - layout.margin - 5
        )

        canvas.drawRect(rect1, borderPaint)
        canvas.drawRect(rect2, borderPaint)
    }

    private fun drawDecorativeBorder() {
        val borderPaint = (paints["border"] ?: Paint()).apply {
            style = Paint.Style.STROKE
            if (strokeWidth == 0f) strokeWidth = 1f
        }

        PdfCanvasHelper.drawDashedLine(canvas, layout.margin, layout.pageWidth - layout.margin, layout.margin, borderPaint)
        PdfCanvasHelper.drawDashedLine(canvas, layout.margin, layout.pageWidth - layout.margin, layout.pageHeight - layout.margin, borderPaint)
    }

    private fun drawReligiousSymbols() {
        val symbolPaint = paints["symbol"] ?: Paint()
        canvas.drawText("ॐ", layout.margin + 20, layout.margin + 40, symbolPaint)
        canvas.drawText("ॐ", layout.pageWidth - layout.margin - 60, layout.margin + 40, symbolPaint)
    }
}