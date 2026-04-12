package com.veristock.pro.core.util

import com.veristock.pro.data.dao.BusinessProfileDao
import kotlinx.coroutines.flow.first

class InvoiceNumberGenerator(
    private val businessProfileDao: BusinessProfileDao
) {
    suspend fun generateNextInvoiceNumber(): String {
        val profile = businessProfileDao.getBusinessProfile().first()
            ?: throw IllegalStateException("Business profile not set up")

        val counter = profile.invoiceCounter
        businessProfileDao.incrementInvoiceCounter()

        val financialYear = getFinancialYearSuffix(profile.financialYearStart)

        return "${profile.invoicePrefix}/$financialYear/${counter.toString().padStart(5, '0')}"
        // Example: INV/2024-25/00001
    }

    private fun getFinancialYearSuffix(fyStart: String): String {
        // fyStart format: "2024-04-01"
        return try {
            val year = fyStart.substring(0, 4).toInt()
            val nextYear = (year + 1).toString().substring(2, 4)
            "$year-$nextYear"
        } catch (e: Exception) {
            // Fallback if date string is malformed
            "24-25"
        }
    }
}