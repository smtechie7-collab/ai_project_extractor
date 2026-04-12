package com.veristock.pro.feature.reports

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.data.repository.ReportsRepository
import com.veristock.pro.domain.model.reports.DateRange
import com.veristock.pro.domain.model.reports.ReportFilters
import com.veristock.pro.domain.model.reports.ReportResult
import com.veristock.pro.domain.model.reports.SalesReportRow
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.Calendar
import javax.inject.Inject

data class DateRangeReportState(
    val isLoading: Boolean = true,
    val filters: ReportFilters = ReportFilters(),
    val reportResult: ReportResult<SalesReportRow>? = null,
    val errorMessage: String? = null
)

@HiltViewModel
class DateRangeReportViewModel @Inject constructor(
    private val reportsRepository: ReportsRepository
) : ViewModel() {

    private val _state = MutableStateFlow(DateRangeReportState())
    val state: StateFlow<DateRangeReportState> = _state.asStateFlow()

    init {
        onFiltersChanged(DateRange.THIS_MONTH, null, null)
    }

    fun onFiltersChanged(range: DateRange, customStart: Long?, customEnd: Long?) {
        val cal = Calendar.getInstance()
        val (start, end) = when (range) {
            DateRange.TODAY -> {
                cal.set(Calendar.HOUR_OF_DAY, 0); cal.set(Calendar.MINUTE, 0); cal.set(Calendar.SECOND, 0)
                val s = cal.timeInMillis
                cal.add(Calendar.DAY_OF_YEAR, 1)
                val e = cal.timeInMillis
                Pair(s, e)
            }
            DateRange.THIS_WEEK -> {
                cal.set(Calendar.DAY_OF_WEEK, cal.firstDayOfWeek)
                val s = cal.timeInMillis
                cal.add(Calendar.WEEK_OF_YEAR, 1)
                val e = cal.timeInMillis
                Pair(s, e)
            }
            DateRange.THIS_MONTH -> {
                cal.set(Calendar.DAY_OF_MONTH, 1)
                val s = cal.timeInMillis
                cal.add(Calendar.MONTH, 1)
                val e = cal.timeInMillis
                Pair(s, e)
            }
            DateRange.CUSTOM -> Pair(customStart, customEnd)
            else -> Pair(0L, System.currentTimeMillis())
        }

        val newFilters = state.value.filters.copy(dateRange = range, startDate = start, endDate = end)
        _state.update { it.copy(filters = newFilters) }
        fetchReportData()
    }

    private fun fetchReportData() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            
            val result = reportsRepository.getSalesReportByDateRange(state.value.filters)

            result.onSuccess {
                _state.update { state -> state.copy(isLoading = false, reportResult = it) }
            }.onFailure {
                _state.update { state -> state.copy(isLoading = false, errorMessage = it.message) }
            }
        }
    }
}
