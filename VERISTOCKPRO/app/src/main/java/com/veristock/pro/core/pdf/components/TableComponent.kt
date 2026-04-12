package com.veristock.pro.core.pdf.components

import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.RectF
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.utils.IndianCurrencyFormatter
import com.veristock.pro.core.pdf.utils.PdfCanvasHelper

class TableComponent(
    private val canvas: Canvas,
    private val invoiceData: InvoiceData,
    private val layout: InvoiceLayout,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>
) {

    private val tableLayout = layout.tableLayout

    fun draw() {
        drawHeader()
        drawRows()
        drawBorders()
    }

    private fun drawHeader() {
        val headerPaint = paints["header"] ?: TextPaint()
        val headerTexts = getHeaderTexts()
        val headerY = tableLayout.tableHeaderY

        tableLayout.columnXPositions.forEachIndexed { index, xPos ->
            val text = headerTexts.getOrNull(index) ?: ""
            val cellRect = RectF(xPos, headerY, xPos + tableLayout.columnWidths[index], headerY + tableLayout.headerHeight)
            drawCellText(text, cellRect, headerPaint, Layout.Alignment.ALIGN_CENTER)
        }
    }

    private fun drawRows() {
        val bodyPaint = paints["body"] ?: TextPaint()

        invoiceData.items.forEachIndexed { rowIndex, item ->
            val rowY = tableLayout.rowYPositions[rowIndex + 1] // +1 to skip header
            val rowHeight = tableLayout.rowHeights[rowIndex]

            val rowData = getRowData(item)

            tableLayout.columnXPositions.forEachIndexed { colIndex, xPos ->
                val text = rowData.getOrNull(colIndex) ?: ""
                val cellRect = RectF(xPos, rowY, xPos + tableLayout.columnWidths[colIndex], rowY + rowHeight)
                val alignment = if (colIndex > 1) Layout.Alignment.ALIGN_OPPOSITE else Layout.Alignment.ALIGN_NORMAL
                drawCellText(text, cellRect, bodyPaint, alignment)
            }
        }
    }

    private fun drawBorders() {
        val borderPaint = paints["border"] ?: Paint()
        val startX = layout.margin
        val endX = layout.pageWidth - layout.margin

        // Top border
        PdfCanvasHelper.drawHorizontalLine(canvas, startX, endX, tableLayout.tableHeaderY, borderPaint)
        // Header bottom border
        PdfCanvasHelper.drawHorizontalLine(canvas, startX, endX, tableLayout.tableBodyY, borderPaint)

        // Row separators
        tableLayout.rowYPositions.drop(1).forEachIndexed { index, y ->
            val finalY = y + tableLayout.rowHeights[index]
            PdfCanvasHelper.drawHorizontalLine(canvas, startX, endX, finalY, borderPaint)
        }

        // Column separators
        var bottomY = tableLayout.rowYPositions.last() + tableLayout.rowHeights.last()
        tableLayout.columnXPositions.forEach { x ->
            canvas.drawLine(x, tableLayout.tableHeaderY, x, bottomY, borderPaint)
        }
        canvas.drawLine(endX, tableLayout.tableHeaderY, endX, bottomY, borderPaint)
    }
    
    private fun drawCellText(
        text: String,
        cellRect: RectF,
        paint: TextPaint,
        alignment: Layout.Alignment
    ) {
        val staticLayout = StaticLayout.Builder
            .obtain(text, 0, text.length, paint, cellRect.width().toInt() - 16)
            .setAlignment(alignment)
            .build()

        canvas.save()
        canvas.translate(cellRect.left + 8f, cellRect.top + 8f)
        staticLayout.draw(canvas)
        canvas.restore()
    }

    private fun getHeaderTexts(): List<String> {
         return when (template.type) {
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> listOf("Sr", "Description", "Qty", "Rate", "Amount")
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> listOf("ITEM", "QTY", "RATE", "GST", "AMOUNT")
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> listOf("S.No", "DESCRIPTION", "HSN", "QTY", "RATE", "TAX", "AMOUNT")
        }
    }

    private fun getRowData(item: com.veristock.pro.core.pdf.models.SaleItemData): List<String> {
        return when (template.type) {
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> listOf(
                item.serialNumber.toString(),
                item.description,
                item.quantity.toString(),
                IndianCurrencyFormatter.format(item.rate),
                IndianCurrencyFormatter.format(item.amount)
            )
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> listOf(
                item.description,
                item.quantity.toString(),
                IndianCurrencyFormatter.format(item.rate),
                "${item.gstRate}%",
                IndianCurrencyFormatter.format(item.amount + (item.amount * item.gstRate / 100))
            )
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> listOf(
                item.serialNumber.toString(),
                item.description,
                item.hsn ?: "",
                item.quantity.toString(),
                IndianCurrencyFormatter.format(item.rate),
                 IndianCurrencyFormatter.format(item.amount * item.gstRate / 100),
                IndianCurrencyFormatter.format(item.amount)
            )
        }
    }
}
