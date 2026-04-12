
package com.veristock.pro.feature.saledetail

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.core.print.PrintJobManager
import com.veristock.pro.data.entity.PrintJobEntity
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.data.repository.InvoiceHistoryRepository
import com.veristock.pro.data.repository.SaleRepository
import com.veristock.pro.domain.model.Customer
import com.veristock.pro.domain.model.InvoicePdfMetadata
import com.veristock.pro.domain.model.Sale
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SaleDetailState(
    val sale: Sale? = null,
    val customer: Customer? = null,
    val history: List<InvoicePdfMetadata> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class SaleDetailViewModel @Inject constructor(
    private val saleRepository: SaleRepository,
    private val customerRepository: CustomerRepository,
    private val invoiceHistoryRepository: InvoiceHistoryRepository,
    private val printJobManager: PrintJobManager,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _state = MutableStateFlow(SaleDetailState())
    val state = _state.asStateFlow()

    val printJobState: StateFlow<PrintJobEntity?> = printJobManager.currentJobState

    init {
        loadSaleDetails()
    }

    fun printSale() {
        val saleId = savedStateHandle.get<Long>("saleId") ?: return
        printJobManager.addJobToQueue(saleId)
    }

    fun clearPrintJobState() {
        printJobManager.clearCurrentJobState()
    }

    private fun loadSaleDetails() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val saleId = savedStateHandle.get<Long>("saleId") ?: throw IllegalStateException("Sale ID not found")

                val sale = saleRepository.getSaleById(saleId.toInt()) ?: throw Exception("Sale not found")

                val customer = if (sale.customerId != null) {
                    customerRepository.getCustomerById(sale.customerId)
                } else {
                    // Fallback for guest sales
                    Customer(
                        name = sale.customerName,
                        mobile = sale.customerMobile ?: "",
                        addressLine1 = sale.customerAddress
                    )
                }

                invoiceHistoryRepository.getHistoryForSale(saleId).collect { history ->
                    _state.update { it.copy(sale = sale, customer = customer, history = history, isLoading = false) }
                }

            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }
}
