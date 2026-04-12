package com.veristock.pro.feature.batchgeneration

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import com.veristock.pro.core.worker.BatchPdfGenerationWorker
import com.veristock.pro.data.repository.SaleRepository
import com.veristock.pro.domain.model.Sale
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.Date
import javax.inject.Inject

enum class BatchOutputFormat {
    SINGLE_PDF, ZIP_FILE
}

data class BatchGenerationState(
    val startDate: Long = System.currentTimeMillis(),
    val endDate: Long = System.currentTimeMillis(),
    val outputFormat: BatchOutputFormat = BatchOutputFormat.ZIP_FILE,
    val matchingSales: List<Sale> = emptyList(),
    val isFetchingSales: Boolean = false,
    val workId: java.util.UUID? = null
)

@HiltViewModel
class BatchGenerationViewModel @Inject constructor(
    private val saleRepository: SaleRepository,
    private val workManager: WorkManager
) : ViewModel() {

    private val _state = MutableStateFlow(BatchGenerationState())
    val state = _state.asStateFlow()

    init {
        // Fetch today's sales by default when the screen loads
        fetchSalesForDateRange()
    }

    fun onDateRangeChanged(startDate: Long, endDate: Long) {
        _state.update { it.copy(startDate = startDate, endDate = endDate) }
        fetchSalesForDateRange()
    }

    fun onOutputFormatChanged(format: BatchOutputFormat) {
        _state.update { it.copy(outputFormat = format) }
    }

    private fun fetchSalesForDateRange() {
        viewModelScope.launch {
            _state.update { it.copy(isFetchingSales = true) }
            val sales = saleRepository.getSalesByDateRange(_state.value.startDate, _state.value.endDate).first()
            _state.update { it.copy(matchingSales = sales, isFetchingSales = false) }
        }
    }

    fun startBatchGeneration() {
        viewModelScope.launch {
            val saleIds = _state.value.matchingSales.map { it.id }.toLongArray()

            if (saleIds.isEmpty()) {
                return@launch
            }

            val workRequest = OneTimeWorkRequestBuilder<BatchPdfGenerationWorker>()
                .setInputData(workDataOf(BatchPdfGenerationWorker.KEY_SALE_IDS to saleIds))
                .build()

            workManager.enqueue(workRequest)
            _state.update { it.copy(workId = workRequest.id) }
        }
    }
}
