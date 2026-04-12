package com.veristock.pro.core.pdf.renderers

import android.graphics.Canvas
import android.graphics.Paint
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate

class Thermal80Renderer : BaseRenderer {

    override fun render(
        canvas: Canvas,
        invoiceData: InvoiceData,
        layout: InvoiceLayout,
        template: InvoiceTemplate,
        paints: Map<String, TextPaint>
    ) {
        val titlePaint = paints["title"] ?: TextPaint()
        val bodyPaint = paints["body"] ?: TextPaint()
        val smallPaint = TextPaint(bodyPaint).apply { textSize = 8f }
        val centerX = layout.pageWidth / 2f
        var currentY = layout.margin
        val leftMargin = layout.margin
        val rightMargin = layout.pageWidth - layout.margin

        // --- Simplified Header ---
        titlePaint.textAlign = Paint.Align.CENTER
        canvas.drawText(invoiceData.business.businessName, centerX, currentY, titlePaint)
        currentY += titlePaint.descent() - titlePaint.ascent()

        bodyPaint.textAlign = Paint.Align.CENTER
        canvas.drawText(invoiceData.business.address, centerX, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()
        canvas.drawText("Ph: ${invoiceData.business.mobile}", centerX, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()

        // --- Invoice Details ---
        currentY += 20 // Add some space
        bodyPaint.textAlign = Paint.Align.LEFT
        canvas.drawText("Invoice: ${invoiceData.sale.invoiceNumber}", leftMargin, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()
        canvas.drawText("Date: ${invoiceData.sale.date}", leftMargin, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()

        // --- Customer Details ---
        currentY += 10
        canvas.drawText("Customer: ${invoiceData.customer.name}", leftMargin, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()

        // --- Dashed Line Separator ---
        val linePaint = Paint().apply { strokeWidth = 1f; pathEffect = android.graphics.DashPathEffect(floatArrayOf(4f, 2f), 0f) }
        currentY += 10
        canvas.drawLine(leftMargin, currentY, rightMargin, currentY, linePaint)
        currentY += 10

        // --- Sale Items (as a simple list) ---
        invoiceData.items.forEach { item ->
            canvas.drawText(item.description, leftMargin, currentY, bodyPaint)
            currentY += bodyPaint.descent() - bodyPaint.ascent()

            val qtyRate = "${item.quantity} x ₹${item.rate}"
            val amount = "₹${item.amount}"
            canvas.drawText(qtyRate, leftMargin, currentY, smallPaint)
            smallPaint.textAlign = Paint.Align.RIGHT
            canvas.drawText(amount, rightMargin, currentY, smallPaint)
            smallPaint.textAlign = Paint.Align.LEFT // Reset alignment
            currentY += smallPaint.descent() - smallPaint.ascent()
        }

        // --- Totals ---
        currentY += 10
        canvas.drawLine(leftMargin, currentY, rightMargin, currentY, linePaint)
        currentY += 20

        bodyPaint.textAlign = Paint.Align.RIGHT
        canvas.drawText("Subtotal: ₹${invoiceData.totals.subtotal}", rightMargin, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()
        canvas.drawText("Total Tax: ₹${invoiceData.totals.totalTax}", rightMargin, currentY, bodyPaint)
        currentY += bodyPaint.descent() - bodyPaint.ascent()
        
        titlePaint.textAlign = Paint.Align.RIGHT
        canvas.drawText("Grand Total: ₹${invoiceData.totals.grandTotal}", rightMargin, currentY, titlePaint)
        currentY += titlePaint.descent() - titlePaint.ascent()

        // --- Footer ---
        currentY += 30
        bodyPaint.textAlign = Paint.Align.CENTER
        canvas.drawText("Thank You!", centerX, currentY, bodyPaint)

    }
}
