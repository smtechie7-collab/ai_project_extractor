
package com.veristock.pro.core.util

import java.math.BigDecimal
import java.math.RoundingMode

/**
 * A data class to hold the results of a GST calculation using BigDecimal for financial precision.
 */
data class GSTCalculationResult(
    val subtotal: BigDecimal,
    val discountAmount: BigDecimal,
    val taxableAmount: BigDecimal,
    val gstRate: BigDecimal,
    val isSameState: Boolean,
    val totalGST: BigDecimal,
    val cgst: BigDecimal,
    val sgst: BigDecimal,
    val igst: BigDecimal,
    val totalWithTax: BigDecimal,
    val roundOff: BigDecimal,
    val grandTotal: BigDecimal
)

/**
 * Provides a robust and safe way to calculate GST using BigDecimal to avoid floating-point inaccuracies.
 */
object GSTCalculation {

    private val SCALE = 2 // Standard for currency
    private val ROUNDING_MODE = RoundingMode.HALF_UP
    private val HUNDRED = BigDecimal("100")

    fun calculate(
        subtotal: BigDecimal,
        discountPercent: BigDecimal = BigDecimal.ZERO,
        discountAmount: BigDecimal = BigDecimal.ZERO,
        gstRate: BigDecimal,
        isSameState: Boolean
    ): GSTCalculationResult {
        // 1. Determine Discount
        val actualDiscountAmount = if (discountPercent > BigDecimal.ZERO) {
            subtotal.multiply(discountPercent).divide(HUNDRED, SCALE, ROUNDING_MODE)
        } else {
            discountAmount
        }.setScale(SCALE, ROUNDING_MODE)

        // 2. Calculate Taxable Amount
        val taxableAmount = subtotal.subtract(actualDiscountAmount).setScale(SCALE, ROUNDING_MODE)

        // 3. Calculate GST
        val gstMultiplier = gstRate.divide(HUNDRED, 4, ROUNDING_MODE) // Use higher precision for multiplier
        val totalGST = taxableAmount.multiply(gstMultiplier).setScale(SCALE, ROUNDING_MODE)

        val cgst: BigDecimal
        val sgst: BigDecimal
        val igst: BigDecimal

        if (isSameState) {
            val halfGst = totalGST.divide(BigDecimal("2"), SCALE, ROUNDING_MODE)
            cgst = halfGst
            sgst = halfGst
            igst = BigDecimal.ZERO.setScale(SCALE, ROUNDING_MODE)
        } else {
            cgst = BigDecimal.ZERO.setScale(SCALE, ROUNDING_MODE)
            sgst = BigDecimal.ZERO.setScale(SCALE, ROUNDING_MODE)
            igst = totalGST
        }

        // 4. Calculate Final Total
        val totalWithTax = taxableAmount.add(totalGST)

        // 5. Calculate Rounding
        val grandTotalRounded = totalWithTax.setScale(0, RoundingMode.HALF_UP)
        val roundOff = grandTotalRounded.subtract(totalWithTax).setScale(SCALE, ROUNDING_MODE)

        return GSTCalculationResult(
            subtotal = subtotal.setScale(SCALE, ROUNDING_MODE),
            discountAmount = actualDiscountAmount,
            taxableAmount = taxableAmount,
            gstRate = gstRate,
            isSameState = isSameState,
            totalGST = totalGST,
            cgst = cgst,
            sgst = sgst,
            igst = igst,
            totalWithTax = totalWithTax.setScale(SCALE, ROUNDING_MODE),
            roundOff = roundOff,
            grandTotal = grandTotalRounded.setScale(SCALE, ROUNDING_MODE)
        )
    }
}
