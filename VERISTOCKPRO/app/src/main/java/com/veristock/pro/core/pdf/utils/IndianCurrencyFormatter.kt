package com.veristock.pro.core.pdf.utils

object IndianCurrencyFormatter {

    /**
     * Formats a numeric amount into the Indian currency system string.
     * Example: 1234567.89 -> "₹12,34,567.89"
     */
    fun format(amount: Double): String {
        val amountStr = String.format("%.2f", amount)
        val (integerPart, decimalPart) = amountStr.split('.')

        if (integerPart.length <= 3) {
            return "₹$integerPart.$decimalPart"
        }

        val lastThreeDigits = integerPart.substring(integerPart.length - 3)
        val remainingDigits = integerPart.substring(0, integerPart.length - 3)

        val formattedRemaining = remainingDigits.reversed()
            .chunked(2)
            .joinToString(",")
            .reversed()

        return "₹$formattedRemaining,$lastThreeDigits.$decimalPart"
    }
}
