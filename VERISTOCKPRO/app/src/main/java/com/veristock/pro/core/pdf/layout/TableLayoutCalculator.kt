package com.veristock.pro.core.pdf.layout

import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.models.TableLayout
import com.veristock.pro.core.pdf.utils.TextMeasurement

class TableLayoutCalculator(
    private val invoiceData: InvoiceData,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>,
    private val availableWidth: Float
) {

    fun calculate(): TableLayout {
        val columnWidths = calculateColumnWidths()
        val columnXPositions = calculateColumnXPositions(columnWidths)
        val (rowHeights, headerHeight) = calculateRowHeights(columnWidths)
        val (rowYPositions, tableBodyY, tableHeaderY) = calculateRowYPositions(rowHeights, headerHeight)
        val totalHeight = headerHeight + rowHeights.sum()

        return TableLayout(
            columnWidths = columnWidths,
            columnXPositions = columnXPositions,
            headerHeight = headerHeight,
            rowHeights = rowHeights,
            totalHeight = totalHeight,
            rowYPositions = rowYPositions,
            tableHeaderY = tableHeaderY,
            tableBodyY = tableBodyY
        )
    }

    private fun calculateColumnWidths(): List<Float> {
        val percentages = when (template.type) {
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> listOf(0.08f, 0.42f, 0.1f, 0.15f, 0.25f)
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> listOf(0.40f, 0.10f, 0.15f, 0.15f, 0.20f)
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> listOf(0.05f, 0.35f, 0.1f, 0.08f, 0.12f, 0.15f, 0.15f)
        }
        val widths = percentages.map { it * availableWidth }.toMutableList()
        val diff = availableWidth - widths.sum()
        widths[widths.lastIndex] += diff
        return widths
    }

    private fun calculateColumnXPositions(columnWidths: List<Float>): List<Float> {
        val positions = mutableListOf<Float>()
        var currentX = margin
        columnWidths.forEach {
            positions.add(currentX)
            currentX += it
        }
        return positions
    }

    private fun calculateRowHeights(columnWidths: List<Float>): Pair<List<Float>, Float> {
        val bodyPaint = paints["body"] ?: TextPaint()
        val headerPaint = paints["header"] ?: TextPaint()
        val padding = 20f

        val headerTexts = getHeaderTexts()
        val headerTextHeight = headerTexts.indices.maxOfOrNull { i ->
            val text = headerTexts.getOrNull(i) ?: ""
            val width = columnWidths.getOrNull(i)?.toInt() ?: 0
            if (text.isEmpty() || width <= 0) 0f else createStaticLayout(text, width, headerPaint).height.toFloat()
        } ?: 0f
        val headerHeight = headerTextHeight + padding
        
        val rowHeights = invoiceData.items.map { item ->
            val descWidth = columnWidths.getOrNull(1)?.toInt() ?: 0
            val descriptionLayout = if (descWidth > 0) createStaticLayout(item.description, descWidth, bodyPaint) else null
            val minHeight = TextMeasurement.getTextHeight(" ", bodyPaint)
            (descriptionLayout?.height?.toFloat() ?: minHeight) + padding
        }
        
        return Pair(rowHeights, headerHeight)
    }
    
    private fun calculateRowYPositions(rowHeights: List<Float>, headerHeight: Float): Triple<List<Float>, Float, Float> {
        val positions = mutableListOf<Float>()
        var currentY = 0f
        positions.add(currentY)
        currentY += headerHeight
        val tableHeaderY = 0f
        val tableBodyY = currentY
        
        rowHeights.forEach {
            positions.add(currentY)
            currentY += it
        }
        return Triple(positions, tableBodyY, tableHeaderY)
    }
    
    private fun getHeaderTexts(): List<String> {
         return when (template.type) {
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.TRADITIONAL -> listOf("Sr", "Description", "Qty", "Rate", "Amount")
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.MODERN -> listOf("ITEM", "QTY", "RATE", "GST", "AMOUNT")
            com.veristock.pro.core.pdf.models.InvoiceTemplateType.GST_FORMAL -> listOf("S.No", "DESCRIPTION OF GOODS", "HSN CODE", "QTY", "RATE", "TAX", "AMOUNT")
        }
    }

    private fun createStaticLayout(text: String, width: Int, paint: TextPaint): StaticLayout {
        return StaticLayout.Builder
            .obtain(text, 0, text.length, paint, width)
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .build()
    }

    private val margin = 40f
}
