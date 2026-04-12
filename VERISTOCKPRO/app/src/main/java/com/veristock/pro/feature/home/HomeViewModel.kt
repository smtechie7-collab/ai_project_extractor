
package com.veristock.pro.feature.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.data.repository.ProductRepository
import com.veristock.pro.data.repository.SaleRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.math.BigDecimal
import java.util.Calendar
import javax.inject.Inject

data class DashboardStats(
    val todaySales: BigDecimal = BigDecimal.ZERO,
    val todayTransactions: Int = 0,
    val lowStockCount: Int = 0,
    val totalProducts: Int = 0,
    val outstandingAmount: BigDecimal = BigDecimal.ZERO
)

data class HomeUiState(
    val stats: DashboardStats = DashboardStats(),
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val errorMessage: String? = null
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val saleRepository: SaleRepository,
    private val productRepository: ProductRepository,
    private val customerRepository: CustomerRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadDashboardData()
    }

    fun refreshDashboard() {
        viewModelScope.launch {
            _uiState.update { it.copy(isRefreshing = true) }
            loadDashboardData(isRefresh = true)
        }
    }

    private fun loadDashboardData(isRefresh: Boolean = false) {
        if (!isRefresh) {
            _uiState.update { it.copy(isLoading = true) }
        }

        viewModelScope.launch {
            try {
                val startOfToday = Calendar.getInstance().apply {
                    set(Calendar.HOUR_OF_DAY, 0)
                    set(Calendar.MINUTE, 0)
                    set(Calendar.SECOND, 0)
                    set(Calendar.MILLISECOND, 0)
                }.timeInMillis

                val salesData = async { saleRepository.getTotalSalesAmount(startOfToday) }
                val transactionCountData = async { saleRepository.getSalesCount(startOfToday) }
                val lowStockData = async { productRepository.getLowStockProductCount() }
                val totalProductsData = async { productRepository.getTotalProductCount() }
                val outstandingAmountData = async { customerRepository.getTotalOutstandingBalance() }

                val dashboardStats = DashboardStats(
                    todaySales = salesData.await() ?: BigDecimal.ZERO,
                    todayTransactions = transactionCountData.await(),
                    lowStockCount = lowStockData.await(),
                    totalProducts = totalProductsData.await(),
                    outstandingAmount = BigDecimal.valueOf(outstandingAmountData.await() ?: 0.0)
                )

                _uiState.update {
                    it.copy(
                        stats = dashboardStats,
                        isLoading = false,
                        isRefreshing = false
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        errorMessage = e.message ?: "An error occurred",
                        isLoading = false,
                        isRefreshing = false
                    )
                }
            }
        }
    }
}
