
package com.veristock.pro.core.print

import com.veristock.pro.core.print.model.BluetoothPrinterState
import com.veristock.pro.core.print.model.PrintJobStatus
import com.veristock.pro.core.print.model.PrintJobType
import com.veristock.pro.data.dao.PrintJobDao
import com.veristock.pro.data.dao.PrinterProfileDao
import com.veristock.pro.data.entity.PrintJobEntity
import com.veristock.pro.data.repository.BusinessRepository
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.data.repository.SaleRepository
import com.veristock.pro.domain.model.Customer
import com.veristock.pro.feature.saledetail.SaleDetailState
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import java.io.IOException
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class PrintJobManager @Inject constructor(
    private val bluetoothManager: BluetoothPrinterManager,
    private val printJobDao: PrintJobDao,
    private val printerProfileDao: PrinterProfileDao,
    private val saleRepository: SaleRepository,
    private val customerRepository: CustomerRepository,
    private val businessRepository: BusinessRepository
) {

    private val managerScope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private val _isProcessing = MutableStateFlow(false)

    private val _currentJobState = MutableStateFlow<PrintJobEntity?>(null)
    val currentJobState: StateFlow<PrintJobEntity?> = _currentJobState.asStateFlow()

    val jobs = printJobDao.getAllJobs()

    init {
        managerScope.launch {
            bluetoothManager.printerState.collect { state ->
                if (state == BluetoothPrinterState.CONNECTED) {
                    processQueue()
                }
            }
        }
    }

    fun addJobToQueue(saleId: Long, type: PrintJobType = PrintJobType.INVOICE) {
        managerScope.launch {
            val defaultProfile = printerProfileDao.getDefaultProfile()
            if (defaultProfile == null) {
                // TODO: Expose error to UI - No default printer set
                return@launch
            }
            val entity = PrintJobEntity(
                id = UUID.randomUUID().toString(),
                type = type,
                dataIdentifier = saleId.toString(),
                printerAddress = defaultProfile.deviceAddress,
                status = PrintJobStatus.QUEUED,
                createdAt = System.currentTimeMillis(),
                attempts = 0,
                lastError = null
            )
            printJobDao.insert(entity)
            _currentJobState.value = entity // Set as current job immediately
            processQueue()
        }
    }

    fun clearCurrentJobState() {
        _currentJobState.value = null
    }

    fun processQueue() {
        if (_isProcessing.value) return

        managerScope.launch {
            _isProcessing.value = true
            try {
                val jobsToProcess = printJobDao.getQueuedAndFailedJobs()
                for (job in jobsToProcess) {
                    _currentJobState.value = job
                    executeJob(job)
                }
            } finally {
                _isProcessing.value = false
            }
        }
    }

    private suspend fun executeJob(job: PrintJobEntity) {
        try {
            job.status = PrintJobStatus.PREPARING
            printJobDao.update(job)
            _currentJobState.value = job

            val saleId = job.dataIdentifier.toLongOrNull() ?: throw Exception("Invalid Sale ID")
            val sale = saleRepository.getSaleById(saleId.toInt()) ?: throw Exception("Sale not found")
            val customer = if (sale.customerId != null) {
                customerRepository.getCustomerById(sale.customerId)
            } else {
                null
            } ?: Customer(
                name = sale.customerName,
                mobile = sale.customerMobile ?: "",
                addressLine1 = sale.customerAddress
            )
            val businessProfile = businessRepository.getBusinessProfile().first() ?: throw Exception("Business Profile not found")
            val saleState = SaleDetailState(sale = sale, customer = customer)

            val profile = printerProfileDao.getProfileByAddress(job.printerAddress) ?: throw Exception("Printer profile not found")
            val formatter = ThermalLayoutFormatter(paperWidth = profile.paperWidth)
            val printData = formatter.format(saleState, businessProfile)

            val device = bluetoothManager.getDeviceByAddress(job.printerAddress)
                ?: throw Exception("Printer device not found or BT permission missing.")

            bluetoothManager.connect(device)

            var connectionAttempts = 0
            while (bluetoothManager.printerState.value != BluetoothPrinterState.CONNECTED && connectionAttempts < 10) {
                delay(1000)
                connectionAttempts++
            }

            if (bluetoothManager.printerState.value != BluetoothPrinterState.CONNECTED) {
                throw IOException("Failed to connect to printer after 10 seconds")
            }

            job.status = PrintJobStatus.PRINTING
            printJobDao.update(job)
            _currentJobState.value = job
            bluetoothManager.writeData(printData)

            job.status = PrintJobStatus.SUCCESS
            printJobDao.update(job)
            _currentJobState.value = job

        } catch (e: Exception) {
            job.attempts += 1
            job.status = if (job.attempts >= 3) PrintJobStatus.FAILED else job.status
            job.lastError = e.message
            printJobDao.update(job)
            _currentJobState.value = job
            bluetoothManager.disconnect()
        }
    }
}
