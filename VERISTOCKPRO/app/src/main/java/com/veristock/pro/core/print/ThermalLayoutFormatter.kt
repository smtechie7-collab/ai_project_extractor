
package com.veristock.pro.core.print

import com.veristock.pro.core.print.model.PaperWidth
import com.veristock.pro.domain.model.BusinessProfile
import com.veristock.pro.domain.model.Sale
import com.veristock.pro.domain.model.SaleItem
import com.veristock.pro.feature.saledetail.SaleDetailState
import java.math.BigDecimal
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Formats invoice data into a thermal receipt layout using an EscPosCommandBuilder.
 */
class ThermalLayoutFormatter(
    private val paperWidth: PaperWidth,
    private val builder: EscPosCommandBuilder = EscPosCommandBuilder()
) {

    private val charsPerLine = paperWidth.charsPerLine
    private val dateFormat = SimpleDateFormat("dd-MMM-yyyy", Locale.getDefault())

    fun format(state: SaleDetailState, businessProfile: BusinessProfile): ByteArray {
        val sale = state.sale ?: return builder.build() // Return empty if no sale
        val customer = state.customer

        // 1. Header
        addHeader(businessProfile)

        // 2. Invoice Info
        builder.printSeparatorLine(charsPerLine, '-')
        val formattedDate = dateFormat.format(Date(sale.invoiceDate))
        builder.printLine(padRight(sale.invoiceNumber, formattedDate, charsPerLine))
        customer?.let {
            builder.printLine("Customer: ${it.name}")
            if (it.mobile.isNotBlank()) builder.printLine("Mobile: ${it.mobile}")
        }
        builder.printSeparatorLine(charsPerLine, '-')

        // 3. Items
        addItemsHeader()
        sale.items.forEach { addItem(it) }
        builder.printSeparatorLine(charsPerLine, '-')

        // 4. Totals
        addTotals(sale)

        // 5. Footer
        addFooter(sale, businessProfile)

        // 6. Cut paper
        builder.feedLines(3).cutPaper()

        return builder.build()
    }

    private fun addHeader(profile: BusinessProfile) {
        builder.setAlignment(EscPosCommandBuilder.Alignment.CENTER)
            .setBold(true)
            .setFontSize(EscPosCommandBuilder.FontSize.DOUBLE_HEIGHT)
            .printLine(profile.businessName.uppercase())
            .setFontSize(EscPosCommandBuilder.FontSize.NORMAL)
            .setBold(false)
        profile.addressLine1?.let { builder.printLine(it) }
        if (!profile.addressLine2.isNullOrBlank()) builder.printLine(profile.addressLine2)
        builder.printLine("Mobile: ${profile.mobile}")
        if (!profile.gstin.isNullOrBlank()) builder.printLine("GSTIN: ${profile.gstin}")
        builder.setAlignment(EscPosCommandBuilder.Alignment.LEFT)
    }

    private fun addItemsHeader() {
        when (paperWidth) {
            PaperWidth.MM_58 -> {
                // No header, use stacked layout for items
            }
            PaperWidth.MM_80 -> {
                val header = padRight("Item", "Amount", charsPerLine)
                builder.setBold(true).printLine(header).setBold(false)
                builder.printSeparatorLine(charsPerLine, '-')
            }
        }
    }

    private fun addItem(item: SaleItem) {
        when (paperWidth) {
            PaperWidth.MM_58 -> addStackedItem(item)
            PaperWidth.MM_80 -> addTableItem(item)
        }
    }

    private fun addStackedItem(item: SaleItem) {
        // Wrap long item names
        wrapText(item.productName, charsPerLine).forEach { builder.printLine(it) }

        val qtyRate = "${item.quantity} x ${formatPrice(item.unitPrice)}"
        val total = formatPrice(item.totalAmount)
        builder.printLine(padRight(qtyRate, total, charsPerLine))
    }

    private fun addTableItem(item: SaleItem) {
        val nameColWidth = charsPerLine - 14 // 14 for Qty, Rate, Amount
        val wrappedName = wrapText(item.productName, nameColWidth)
        val amount = formatPrice(item.totalAmount)

        builder.printLine(padRight(wrappedName.firstOrNull() ?: "", amount, charsPerLine))
        wrappedName.drop(1).forEach { builder.printLine(it) } // Print subsequent lines if wrapped
        val details = "  ${item.quantity} x ${formatPrice(item.unitPrice)}"
        builder.printLine(details)
    }

    private fun addTotals(sale: Sale) {
        builder.printLine(padRight("Subtotal:", formatPrice(sale.subtotal), charsPerLine))
        if (sale.discountAmount > BigDecimal.ZERO) {
            builder.printLine(padRight("Discount:", "-${formatPrice(sale.discountAmount)}", charsPerLine))
        }
        if (sale.cgstAmount > BigDecimal.ZERO) {
            builder.printLine(padRight("CGST:", formatPrice(sale.cgstAmount), charsPerLine))
        }
        if (sale.sgstAmount > BigDecimal.ZERO) {
            builder.printLine(padRight("SGST:", formatPrice(sale.sgstAmount), charsPerLine))
        }
        if (sale.igstAmount > BigDecimal.ZERO) {
            builder.printLine(padRight("IGST:", formatPrice(sale.igstAmount), charsPerLine))
        }
        builder.printSeparatorLine(charsPerLine, '-')
        builder.setBold(true).setFontSize(EscPosCommandBuilder.FontSize.DOUBLE_HEIGHT)
        builder.printLine(padRight("TOTAL:", formatPrice(sale.grandTotal), charsPerLine))
        builder.setFontSize(EscPosCommandBuilder.FontSize.NORMAL).setBold(false)
    }

    private fun addFooter(sale: Sale, profile: BusinessProfile) {
        builder.printSeparatorLine(charsPerLine, '=')
        builder.setAlignment(EscPosCommandBuilder.Alignment.CENTER)
        builder.printLine("Payment: ${sale.paymentMode} - ${sale.paymentStatus}")
        builder.printLine(profile.termsAndConditions)
        builder.setAlignment(EscPosCommandBuilder.Alignment.LEFT)
    }

    // --- Helper Functions ---

    private fun padRight(left: String, right: String, totalWidth: Int): String {
        val spaceNeeded = totalWidth - left.length - right.length
        val space = if (spaceNeeded > 0) " ".repeat(spaceNeeded) else ""
        return "$left$space$right"
    }

    private fun formatPrice(price: BigDecimal): String {
        return String.format(Locale.ENGLISH, "%.2f", price)
    }

    private fun wrapText(text: String, lineLength: Int): List<String> {
        val lines = mutableListOf<String>()
        var remainingText = text

        while (remainingText.length > lineLength) {
            var breakPoint = remainingText.substring(0, lineLength).lastIndexOf(' ')
            if (breakPoint == -1) { // No space found, hard break
                breakPoint = lineLength
            }
            lines.add(remainingText.substring(0, breakPoint).trim())
            remainingText = remainingText.substring(breakPoint).trim()
        }
        if (remainingText.isNotEmpty()) {
            lines.add(remainingText)
        }
        return lines
    }
}
