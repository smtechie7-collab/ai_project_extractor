package com.veristock.pro.core.util

import java.text.NumberFormat
import java.util.Locale

object CurrencyFormatter {
    private val indianFormat = NumberFormat.getCurrencyInstance(Locale("en", "IN"))

    fun format(amount: Double): String {
        return try {
            indianFormat.format(amount)
        } catch (e: Exception) {
            "₹ $amount"
        }
    }

    fun formatWithoutSymbol(amount: Double): String {
        return String.format(Locale("en", "IN"), "%.2f", amount)
    }
}