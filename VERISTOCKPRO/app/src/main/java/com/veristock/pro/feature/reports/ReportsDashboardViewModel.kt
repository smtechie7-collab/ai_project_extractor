package com.veristock.pro.feature.reports

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.data.repository.ReportsRepository
import com.veristock.pro.domain.model.reports.SalesSummaryByDay
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class DashboardState(
    val isLoading: Boolean = true,
    val todayStats: SalesSummaryByDay? = null,
    val errorMessage: String? = null
)

@HiltViewModel
class ReportsDashboardViewModel @Inject constructor(
    private val reportsRepository: ReportsRepository
) : ViewModel() {

    private val _state = MutableStateFlow(DashboardState())
    val state: StateFlow<DashboardState> = _state.asStateFlow()

    init {
        loadDashboardData()
    }

    fun loadDashboardData() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }

            val result = reportsRepository.getDailySalesSummary(System.currentTimeMillis())

            result.onSuccess {
                _state.update { state -> state.copy(isLoading = false, todayStats = it) }
            }.onFailure {
                _state.update { state -> state.copy(isLoading = false, errorMessage = it.message) }
            }
        }
    }
}
