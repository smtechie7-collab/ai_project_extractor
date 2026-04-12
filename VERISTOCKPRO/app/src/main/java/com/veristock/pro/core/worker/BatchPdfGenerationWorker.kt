package com.veristock.pro.core.worker

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import androidx.work.workDataOf
import com.veristock.pro.core.pdf.InvoicePdfGenerator
import com.veristock.pro.core.pdf.models.BorderStyle
import com.veristock.pro.core.pdf.models.ColorScheme
import com.veristock.pro.core.pdf.models.FontSize
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.models.InvoiceTemplateType
import com.veristock.pro.core.session.BusinessSession
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.data.repository.SaleRepository
import com.veristock.pro.domain.model.CopySettings
import com.veristock.pro.domain.model.Invoice
import com.veristock.pro.domain.model.InvoiceCopyType
import com.veristock.pro.domain.model.PaperSize
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

@HiltWorker
class BatchPdfGenerationWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val saleRepository: SaleRepository,
    private val customerRepository: CustomerRepository,
    private val businessSession: BusinessSession,
    private val invoicePdfGenerator: InvoicePdfGenerator
) : CoroutineWorker(appContext, workerParams) {

    companion object {
        const val KEY_SALE_IDS = "SALE_IDS"
        const val KEY_PROGRESS = "PROGRESS"
        const val KEY_TOTAL = "TOTAL"
    }

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val saleIds = inputData.getLongArray(KEY_SALE_IDS)
        if (saleIds == null || saleIds.isEmpty()) {
            return@withContext Result.failure()
        }

        try {
            val profile = businessSession.requireBusinessProfile()
            val totalSales = saleIds.size

            val template = InvoiceTemplate(
                type = InvoiceTemplateType.MODERN,
                pageSize = PaperSize.A4,
                showLogo = true,
                tagline = profile.tagline,
                borderStyle = BorderStyle.SIMPLE,
                fontSize = FontSize.MEDIUM,
                colorScheme = ColorScheme.BLACK_WHITE,
                footerMessage = "Thank you!",
                showDecorations = false,
                useRegionalLanguage = false,
                regionalLanguage = null
            )

            val copySettings = listOf(
                CopySettings(InvoiceCopyType.ORIGINAL, "Original for Recipient", null, 0f, true, null),
                CopySettings(InvoiceCopyType.DUPLICATE, "Duplicate for Supplier", "DUPLICATE", 0.3f, true, null)
            )

            for (i in saleIds.indices) {
                val saleId = saleIds[i]
                setProgress(workDataOf(KEY_PROGRESS to (i + 1), KEY_TOTAL to totalSales))

                val sale = saleRepository.getSaleById(saleId.toInt())
                val customer = sale?.customerId?.let { customerRepository.getCustomerById(it) }

                if (sale == null || customer == null) {
                    continue
                }

                val invoice = Invoice(sale, sale.items, customer, profile)
                invoicePdfGenerator.generateInvoice(invoice, template, copySettings)
            }

            Result.success()
        } catch (e: Exception) {
            Result.failure()
        }
    }
}
