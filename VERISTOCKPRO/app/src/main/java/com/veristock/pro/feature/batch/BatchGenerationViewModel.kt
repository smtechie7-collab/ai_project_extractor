package com.veristock.pro.feature.batch

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import com.veristock.pro.data.repository.SaleRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class BatchGenerationViewModel @Inject constructor(
    private val saleRepository: SaleRepository,
    private val workManager: WorkManager
) : ViewModel() {

    private val _state = MutableStateFlow(BatchGenerationState())
    val state: StateFlow<BatchGenerationState> = _state.asStateFlow()

    fun setDateRange(start: Long, end: Long) {
        _state.update { it.copy(startDate = start, endDate = end) }
        fetchSales()
    }

    fun setOutputFormat(format: OutputFormat) {
        _state.update { it.copy(outputFormat = format) }
    }

    private fun fetchSales() {
        viewModelScope.launch {
            saleRepository.getSalesByDateRange(state.value.startDate, state.value.endDate)
                .collect { sales ->
                    _state.update { it.copy(foundSales = sales, matchingInvoiceCount = sales.size) }
                }
        }
    }

    fun startGeneration() {
        val saleIds = state.value.foundSales.map { it.id }.toLongArray()

        val workRequest = OneTimeWorkRequestBuilder<BatchPdfGenerationWorker>()
            .setInputData(workDataOf(
                "SALE_IDS" to saleIds,
                "OUTPUT_FORMAT" to state.value.outputFormat.name
            ))
            .build()

        workManager.enqueue(workRequest)

        _state.update { it.copy(isGenerating = true) }
    }
}
