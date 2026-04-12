package com.veristock.pro.feature.settings.invoices

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.models.InvoiceTemplateType
import com.veristock.pro.data.repository.PreferencesRepository
import com.veristock.pro.domain.model.PaperSize
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class InvoiceSettingsViewModel @Inject constructor(
    private val preferencesRepository: PreferencesRepository
) : ViewModel() {

    private val _state = MutableStateFlow<InvoiceTemplate?>(null)
    val state = _state.asStateFlow()

    init {
        loadSettings()
    }

    private fun loadSettings() {
        viewModelScope.launch {
            // Load the saved template from preferences, or use a default
            val savedTemplate = preferencesRepository.getInvoiceTemplate() ?: createDefaultTemplate()
            _state.value = savedTemplate
        }
    }

    fun onTemplateTypeChange(templateType: InvoiceTemplateType) {
        _state.update { it?.copy(type = templateType) }
        saveSettings()
    }

    fun onPageSizeChange(pageSize: PaperSize) {
        _state.update { it?.copy(pageSize = pageSize) }
        saveSettings()
    }

    private fun saveSettings() {
        viewModelScope.launch {
            _state.value?.let {
                preferencesRepository.saveInvoiceTemplate(it)
            }
        }
    }

    private fun createDefaultTemplate(): InvoiceTemplate {
        return InvoiceTemplate(
            type = InvoiceTemplateType.MODERN,
            pageSize = PaperSize.A4,
            showLogo = true,
            tagline = "Quality Products, Best Prices",
            borderStyle = com.veristock.pro.core.pdf.models.BorderStyle.SIMPLE,
            fontSize = com.veristock.pro.core.pdf.models.FontSize.MEDIUM,
            colorScheme = com.veristock.pro.core.pdf.models.ColorScheme.BLACK_WHITE,
            footerMessage = "Thank you for your business!",
            showDecorations = false,
            useRegionalLanguage = false,
            regionalLanguage = null
        )
    }
}
