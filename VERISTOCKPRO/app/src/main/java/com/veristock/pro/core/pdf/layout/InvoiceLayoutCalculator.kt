
package com.veristock.pro.core.pdf.layout

import android.text.TextPaint
import com.veristock.pro.core.pdf.components.CustomerInfoComponent
import com.veristock.pro.core.pdf.components.FooterComponent
import com.veristock.pro.core.pdf.components.HeaderComponent
import com.veristock.pro.core.pdf.components.TotalsComponent
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate

class InvoiceLayoutCalculator(
    private val invoiceData: InvoiceData,
    private val template: InvoiceTemplate,
    private val paints: Map<String, TextPaint>,
    private val pageWidth: Float,
    private val pageHeight: Float,
    private val margin: Float
) {

    fun calculate(): InvoiceLayout {
        val availableWidth = pageWidth - (margin * 2)
        var currentY = margin

        val headerStartY = currentY
        val headerHeight = HeaderComponent.measureHeight(invoiceData, template, paints)
        currentY += headerHeight

        val customerInfoStartY = currentY
        val customerInfoHeight = CustomerInfoComponent.measureHeight(invoiceData, template, paints, availableWidth)
        currentY += customerInfoHeight

        val tableStartY = currentY
        val tableCalculator = TableLayoutCalculator(invoiceData, template, paints, availableWidth)
        val rawTableLayout = tableCalculator.calculate()
        currentY += rawTableLayout.totalHeight

        val totalsStartY = currentY
        val totalsHeight = TotalsComponent.measureHeight(invoiceData, template, paints, availableWidth)
        currentY += totalsHeight

        val footerStartY = currentY
        
        val shiftedRowY = rawTableLayout.rowYPositions.map { it + tableStartY }
        val shiftedTableLayout = rawTableLayout.copy(
            tableHeaderY = tableStartY,
            tableBodyY = rawTableLayout.tableBodyY + tableStartY,
            rowYPositions = shiftedRowY
        )
        
        return InvoiceLayout(
            pageHeight = pageHeight,
            pageWidth = pageWidth,
            margin = margin,
            headerStartY = headerStartY,
            customerInfoStartY = customerInfoStartY,
            tableStartY = tableStartY,
            totalsStartY = totalsStartY,
            footerStartY = footerStartY,
            tableLayout = shiftedTableLayout
        )
    }

    /**
     * Performs a "measure pass" to calculate the total required vertical height for the invoice.
     */
    fun calculateDynamicHeight(): Int {
        val availableWidth = pageWidth - (margin * 2)
        var totalHeight = margin // Start with top margin

        totalHeight += HeaderComponent.measureHeight(invoiceData, template, paints)
        totalHeight += CustomerInfoComponent.measureHeight(invoiceData, template, paints, availableWidth)
        
        val tableCalculator = TableLayoutCalculator(invoiceData, template, paints, availableWidth)
        val tableLayout = tableCalculator.calculate()
        totalHeight += tableLayout.totalHeight
        
        totalHeight += TotalsComponent.measureHeight(invoiceData, template, paints, availableWidth)
        totalHeight += FooterComponent.measureHeight(invoiceData, template, paints)

        totalHeight += margin // Add bottom margin

        return totalHeight.toInt()
    }
}
