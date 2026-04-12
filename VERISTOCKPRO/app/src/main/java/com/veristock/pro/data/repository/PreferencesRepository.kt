package com.veristock.pro.data.repository

import com.veristock.pro.core.pdf.models.InvoiceTemplate

interface PreferencesRepository {
    suspend fun saveInvoiceTemplate(template: InvoiceTemplate)
    suspend fun getInvoiceTemplate(): InvoiceTemplate?
}
