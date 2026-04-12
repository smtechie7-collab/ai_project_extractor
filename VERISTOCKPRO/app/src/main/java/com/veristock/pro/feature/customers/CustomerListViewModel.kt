
package com.veristock.pro.feature.customers

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.domain.model.Customer
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.math.BigDecimal
import javax.inject.Inject

data class CustomerListState(
    val customers: List<Customer> = emptyList(),
    val filteredCustomers: List<Customer> = emptyList(),
    val searchQuery: String = "",
    val isLoading: Boolean = true,
    val errorMessage: String? = null,
    val totalCustomers: Int = 0,
    val totalOutstanding: BigDecimal = BigDecimal.ZERO
)

@HiltViewModel
class CustomerListViewModel @Inject constructor(
    private val customerRepository: CustomerRepository
) : ViewModel() {

    private val _state = MutableStateFlow(CustomerListState())
    val state: StateFlow<CustomerListState> = _state.asStateFlow()

    init {
        loadCustomers()
    }

    fun loadCustomers() {
        viewModelScope.launch {
            customerRepository.getAllActiveCustomers()
                .onStart { _state.update { it.copy(isLoading = true) } }
                .catch { e ->
                    _state.update {
                        it.copy(
                            errorMessage = "Failed to load customers: ${e.message}",
                            isLoading = false
                        )
                    }
                }
                .collect { customerList ->
                    val totalOutstanding = customerList.fold(BigDecimal.ZERO) { acc, customer -> acc + customer.outstandingBalance }
                    _state.update {
                        it.copy(
                            customers = customerList,
                            filteredCustomers = if (it.searchQuery.isBlank()) customerList else it.filteredCustomers,
                            totalCustomers = customerList.size,
                            totalOutstanding = totalOutstanding,
                            isLoading = false
                        )
                    }
                    // Re-apply search if it exists
                    if (_state.value.searchQuery.isNotBlank()) {
                        searchCustomers(_state.value.searchQuery)
                    }
                }
        }
    }

    fun searchCustomers(query: String) {
        val trimmedQuery = query.trim()
        _state.update { it.copy(searchQuery = trimmedQuery) }

        val filteredList = if (trimmedQuery.isBlank()) {
            _state.value.customers
        } else {
            _state.value.customers.filter {
                it.name.contains(trimmedQuery, ignoreCase = true) ||
                it.mobile.contains(trimmedQuery, ignoreCase = true)
            }
        }
        _state.update { it.copy(filteredCustomers = filteredList) }
    }

    fun refreshCustomers() {
        loadCustomers()
    }
}
