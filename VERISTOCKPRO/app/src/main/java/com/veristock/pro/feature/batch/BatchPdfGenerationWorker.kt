package com.veristock.pro.feature.batch

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.ForegroundInfo
import androidx.work.WorkerParameters
import com.veristock.pro.R
import com.veristock.pro.core.pdf.InvoicePdfGenerator
import com.veristock.pro.core.pdf.models.BorderStyle
import com.veristock.pro.core.pdf.models.ColorScheme
import com.veristock.pro.core.pdf.models.FontSize
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.models.InvoiceTemplateType
import com.veristock.pro.data.repository.BusinessRepository
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.data.repository.SaleRepository
import com.veristock.pro.domain.model.CopySettings
import com.veristock.pro.domain.model.Customer
import com.veristock.pro.domain.model.Invoice
import com.veristock.pro.domain.model.InvoiceCopyType
import com.veristock.pro.domain.model.PaperSize
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

@HiltWorker
class BatchPdfGenerationWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val saleRepository: SaleRepository,
    private val customerRepository: CustomerRepository,
    private val businessRepository: BusinessRepository,
    private val pdfGenerator: InvoicePdfGenerator
) : CoroutineWorker(appContext, workerParams) {

    private val notificationManager = appContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

    override suspend fun doWork(): Result {
        val saleIds = inputData.getLongArray("SALE_IDS") ?: return Result.failure()
        val outputFormat = inputData.getString("OUTPUT_FORMAT") ?: OutputFormat.ZIP_FILE.name

        createNotificationChannel()
        val notificationId = 1

        return try {
            val outputFiles = mutableListOf<File>()

            saleIds.forEachIndexed { index, saleId ->
                val progress = (index + 1) / saleIds.size.toFloat()
                val notification = createProgressNotification(index + 1, saleIds.size)
                setForeground(ForegroundInfo(notificationId, notification))

                val sale = saleRepository.getSaleById(saleId.toInt()) ?: return@forEachIndexed
                val customer = sale.customerId?.let { customerRepository.getCustomerById(it) } ?: Customer(name=sale.customerName, mobile=sale.customerMobile ?: "")
                val businessProfile = businessRepository.getBusinessProfileOnce() ?: return@forEachIndexed

                val invoice = Invoice(sale, sale.items, customer, businessProfile)

                val template = InvoiceTemplate(
                    type = InvoiceTemplateType.MODERN,
                    pageSize = PaperSize.A4,
                    showLogo = true,
                    tagline = businessProfile.tagline,
                    borderStyle = BorderStyle.SIMPLE,
                    fontSize = FontSize.MEDIUM,
                    colorScheme = ColorScheme.BLACK_WHITE,
                    footerMessage = "Thank you for your business!",
                    showDecorations = false,
                    useRegionalLanguage = false,
                    regionalLanguage = null
                )

                val copySettings = listOf(
                    CopySettings(InvoiceCopyType.ORIGINAL, "Original for Recipient", null, 0f, true, null)
                )

                val result = pdfGenerator.generateInvoice(invoice, template, copySettings)
                result.onSuccess {
                    outputFiles.add(it)
                }
            }

            if (outputFormat == OutputFormat.ZIP_FILE.name) {
                createZip(outputFiles)
            }

            showCompletionNotification(saleIds.size)
            Result.success()
        } catch (e: Exception) {
            showErrorNotification(e.message)
            Result.failure()
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("batch_pdf", "Batch PDF Generation", NotificationManager.IMPORTANCE_LOW)
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun createProgressNotification(current: Int, total: Int): android.app.Notification {
        return NotificationCompat.Builder(applicationContext, "batch_pdf")
            .setContentTitle("Generating Invoices")
            .setContentText("$current / $total")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setOngoing(true)
            .setProgress(total, current, false)
            .build()
    }

    private fun showCompletionNotification(count: Int) {
        val notification = NotificationCompat.Builder(applicationContext, "batch_pdf")
            .setContentTitle("Batch Generation Complete")
            .setContentText("$count invoices generated successfully.")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .build()
        notificationManager.notify(2, notification)
    }

    private fun showErrorNotification(error: String?) {
        val notification = NotificationCompat.Builder(applicationContext, "batch_pdf")
            .setContentTitle("Batch Generation Failed")
            .setContentText(error ?: "An unknown error occurred.")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .build()
        notificationManager.notify(3, notification)
    }

    private fun createZip(files: List<File>) {
        val zipFile = File(applicationContext.cacheDir, "invoices_batch.zip")
        ZipOutputStream(FileOutputStream(zipFile)).use { zipOut ->
            files.forEach { file ->
                FileInputStream(file).use { fileIn ->
                    val entry = ZipEntry(file.name)
                    zipOut.putNextEntry(entry)
                    fileIn.copyTo(zipOut)
                    zipOut.closeEntry()
                }
            }
        }
    }
}
