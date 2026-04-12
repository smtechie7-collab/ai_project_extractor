package com.veristock.pro.data.repository.impl

import android.content.SharedPreferences
import com.google.gson.Gson
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.data.repository.PreferencesRepository
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class DefaultPreferencesRepository @Inject constructor(
    private val prefs: SharedPreferences,
    private val gson: Gson
) : PreferencesRepository {

    override suspend fun saveInvoiceTemplate(template: InvoiceTemplate) {
        val jsonString = gson.toJson(template)
        prefs.edit().putString(KEY_INVOICE_TEMPLATE, jsonString).apply()
    }

    override suspend fun getInvoiceTemplate(): InvoiceTemplate? {
        val jsonString = prefs.getString(KEY_INVOICE_TEMPLATE, null)
        return if (jsonString != null) {
            gson.fromJson(jsonString, InvoiceTemplate::class.java)
        } else {
            null
        }
    }

    companion object {
        private const val KEY_INVOICE_TEMPLATE = "invoice_template_prefs"
    }
}
