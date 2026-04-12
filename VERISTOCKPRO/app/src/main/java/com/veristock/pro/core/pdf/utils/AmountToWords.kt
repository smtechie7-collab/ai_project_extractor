package com.veristock.pro.core.pdf.utils

import kotlin.math.roundToLong

object AmountToWords {

    private val units = arrayOf(
        "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"
    )
    private val tens = arrayOf("", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety")

    private fun convertToWords(number: Long): String {
        if (number == 0L) {
            return ""
        }

        if (number < 0) {
            return "Minus " + convertToWords(-number)
        }

        if (number < 20) {
            return units[number.toInt()]
        }

        if (number < 100) {
            return tens[number.toInt() / 10] + (if (number % 10 != 0L) " " + units[(number % 10).toInt()] else "")
        }

        if (number < 1000) {
            return units[(number / 100).toInt()] + " Hundred" + (if (number % 100 != 0L) " " + convertToWords(number % 100) else "")
        }

        if (number < 100000) {
            return convertToWords(number / 1000) + " Thousand" + (if (number % 1000 != 0L) " " + convertToWords(number % 1000) else "")
        }

        if (number < 10000000) {
            return convertToWords(number / 100000) + " Lakh" + (if (number % 100000 != 0L) " " + convertToWords(number % 100000) else "")
        }

        return convertToWords(number / 10000000) + " Crore" + (if (number % 10000000 != 0L) " " + convertToWords(number % 10000000) else "")
    }

    /**
     * Converts a double amount to its word representation in Indian currency format.
     * Example: 148680.00 -> "One Lakh Forty Eight Thousand Six Hundred Eighty Rupees Only"
     */
    fun convert(amount: Double): String {
        if (amount < 0) return "Invalid Amount"
        if (amount == 0.0) return "Zero Rupees Only"

        val wholePart = amount.toLong()
        val fractionalPart = ((amount - wholePart) * 100).roundToLong()

        val wholeWords = convertToWords(wholePart)
        val rupeesText = if (wholePart == 1L) "Rupee" else "Rupees"
        
        var result = "$wholeWords $rupeesText"

        if (fractionalPart > 0) {
            val fractionalWords = convertToWords(fractionalPart)
            val paisaText = if (fractionalPart == 1L) "Paisa" else "Paisa"
            result += " and $fractionalWords $paisaText"
        }

        return (result.trim().replace("\\s+".toRegex(), " ") + " Only").trim()
    }
}
