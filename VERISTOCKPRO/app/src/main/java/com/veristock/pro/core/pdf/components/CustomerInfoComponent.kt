package com.veristock.pro.core.pdf.components

import android.graphics.Canvas
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import kotlin.math.max

class CustomerInfoComponent(
    private val canvas: Canvas,
    private val invoiceData: InvoiceData,
    private val layout: InvoiceLayout,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>,
    private val startY: Float
) {

    fun draw() {
        val bodyPaint = paints["body"] ?: TextPaint()
        val headerPaint = paints["header"] ?: TextPaint()
        
        val contentWidth = layout.pageWidth - (layout.margin * 2)
        val halfWidth = contentWidth / 2f
        val leftX = layout.margin
        val rightX = layout.margin + halfWidth

        var currentY = startY

        // Titles
        canvas.drawText("BILL TO:", leftX, currentY, headerPaint)
        canvas.drawText("SHIP TO:", rightX, currentY, headerPaint)
        currentY += 30f

        // Customer Name
        canvas.drawText(invoiceData.customer.name, leftX, currentY, bodyPaint)
        canvas.drawText(invoiceData.customer.name, rightX, currentY, bodyPaint)
        currentY += 25f
        
        // Address
        val addressY = currentY
        val billToAddress = invoiceData.customer.billingAddress
        val shipToAddress = invoiceData.customer.shippingAddress
        
        val billToLayout = createStaticLayout(billToAddress, halfWidth.toInt(), bodyPaint)
        val shipToLayout = createStaticLayout(shipToAddress, halfWidth.toInt(), bodyPaint)

        canvas.save()
        canvas.translate(leftX, addressY)
        billToLayout.draw(canvas)
        canvas.restore()

        canvas.save()
        canvas.translate(rightX, addressY)
        shipToLayout.draw(canvas)
        canvas.restore()
        
        currentY += max(billToLayout.height, shipToLayout.height) + 10f
        
        // GSTIN if available
        invoiceData.customer.gstin?.let {
             canvas.drawText("GSTIN: $it", leftX, currentY, bodyPaint)
        }
    }

    companion object {
        fun measureHeight(invoiceData: InvoiceData, template: InvoiceTemplate, paints: Map<String, TextPaint>, width: Float): Float {
            val bodyPaint = paints["body"] ?: TextPaint()
            var height = 30f // For title
            height += 25f // For name
            
            val halfWidth = width / 2f
            val billToLayout = createStaticLayout(invoiceData.customer.billingAddress, halfWidth.toInt(), bodyPaint)
            val shipToLayout = createStaticLayout(invoiceData.customer.shippingAddress, halfWidth.toInt(), bodyPaint)
            
            height += max(billToLayout.height, shipToLayout.height) + 10f
            
            if(invoiceData.customer.gstin != null) {
                height += 25f
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
