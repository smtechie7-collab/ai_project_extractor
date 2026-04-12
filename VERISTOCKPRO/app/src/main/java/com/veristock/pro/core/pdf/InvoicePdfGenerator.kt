
package com.veristock.pro.core.pdf

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import android.text.TextPaint
import androidx.core.graphics.withRotation
import com.veristock.pro.core.pdf.layout.InvoiceLayoutCalculator
import com.veristock.pro.core.pdf.models.InvoiceLayout
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.models.InvoiceTemplateType
import com.veristock.pro.core.pdf.models.ColorScheme
import com.veristock.pro.core.pdf.renderers.*
import com.veristock.pro.data.repository.InvoiceHistoryRepository
import com.veristock.pro.domain.mapper.toInvoiceData
import com.veristock.pro.domain.model.CopySettings
import com.veristock.pro.domain.model.Invoice
import com.veristock.pro.domain.model.InvoiceCopyType
import com.veristock.pro.domain.model.InvoicePdfMetadata
import com.veristock.pro.domain.model.PaperSize
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import javax.inject.Inject

class InvoicePdfGenerator @Inject constructor(
    private val context: Context,
    private val historyRepository: InvoiceHistoryRepository
) {

    suspend fun generateInvoice(
        invoice: Invoice,
        template: InvoiceTemplate,
        copySettings: List<CopySettings>
    ): Result<File> = withContext(Dispatchers.IO) { // Moved to IO thread
        val document = PdfDocument()
        val paints = createPaints(template)

        try {
            copySettings.forEachIndexed { index, copy ->
                val (width, initialHeight) = getPageDimensions(template.pageSize)
                val dynamicHeight = if (template.pageSize.isThermal) {
                    val layoutCalculator = InvoiceLayoutCalculator(invoice.toInvoiceData(), template, paints, width.toFloat(), Float.MAX_VALUE, 10f)
                    layoutCalculator.calculateDynamicHeight()
                } else {
                    initialHeight
                }

                val pageInfo = PdfDocument.PageInfo.Builder(width, dynamicHeight, index + 1).create()
                val page = document.startPage(pageInfo)
                renderPage(page.canvas, invoice, template, copy, paints, width, dynamicHeight)
                document.finishPage(page)
            }

            val file = getInvoiceFile(invoice.sale.invoiceNumber)
            FileOutputStream(file).use { document.writeTo(it) }
            document.close()

            val metadata = InvoicePdfMetadata(
                saleId = invoice.sale.id,
                templateType = template.type.name,
                paperSize = template.pageSize.name,
                copyTypes = copySettings.joinToString { it.copyType.name },
                fileSize = file.length(),
                filePath = file.absolutePath,
                generatedAt = System.currentTimeMillis() // Added timestamp
            )
            historyRepository.saveMetadata(metadata)

            Result.success(file)
        } catch (e: Exception) {
            document.close()
            Result.failure(e)
        }
    }

    fun generatePreview(invoice: Invoice, template: InvoiceTemplate): Bitmap {
        val paints = createPaints(template)
        val (width, initialHeight) = getPageDimensions(template.pageSize)

        val dynamicHeight = if (template.pageSize.isThermal) {
            val layoutCalculator = InvoiceLayoutCalculator(invoice.toInvoiceData(), template, paints, width.toFloat(), Float.MAX_VALUE, 10f)
            layoutCalculator.calculateDynamicHeight()
        } else {
            initialHeight
        }

        val bitmap = Bitmap.createBitmap(width, dynamicHeight, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)

        val originalCopySettings = CopySettings(InvoiceCopyType.ORIGINAL, "Original for Recipient", null, 0f, true, null)
        renderPage(canvas, invoice, template, originalCopySettings, paints, width, dynamicHeight)

        return bitmap
    }

    private fun renderPage(
        canvas: Canvas, 
        invoice: Invoice, 
        template: InvoiceTemplate, 
        copy: CopySettings, 
        paints: Map<String, TextPaint>, 
        width: Int, 
        height: Int
    ) {
        val invoiceData = invoice.toInvoiceData()

        canvas.drawColor(Color.WHITE)
        copy.watermarkText?.let { drawWatermark(canvas, it, width, height, copy.watermarkOpacity) }

        val renderer: BaseRenderer = if (template.pageSize.isThermal) {
            if (template.pageSize == PaperSize.THERMAL_58MM) Thermal58Renderer() else Thermal80Renderer()
        } else {
            when (template.type) {
                InvoiceTemplateType.TRADITIONAL -> TraditionalRenderer()
                InvoiceTemplateType.MODERN -> ModernRenderer()
                InvoiceTemplateType.GST_FORMAL -> GstFormalRenderer()
            }
        }

        val margin = if (template.pageSize.isThermal) 10f else 40f
        val layoutCalculator = InvoiceLayoutCalculator(invoiceData, template, paints, width.toFloat(), height.toFloat(), margin)
        val layout = layoutCalculator.calculate()
        
        renderer.render(canvas, invoiceData, layout, template, paints)

        if (!template.pageSize.isThermal) {
            drawCopyHeaderText(canvas, copy.headerText, width, paints["header"] ?: TextPaint())
        }
    }

    private fun getPageDimensions(pageSize: PaperSize): Pair<Int, Int> {
        return Pair(pageSize.widthPoints.toInt(), pageSize.heightPoints.toInt())
    }

    private fun drawWatermark(canvas: Canvas, text: String, width: Int, height: Int, opacity: Float) {
        // ...
    }

    private fun drawCopyHeaderText(canvas: Canvas, text: String, width: Int, paint: Paint) {
        // ...
    }

    fun getInvoiceFile(invoiceNumber: String): File {
        val dir = File(context.filesDir, "invoices")
        if (!dir.exists()) dir.mkdirs()
        val safeName = invoiceNumber.replace("/", "_").replace("\\", "_")
        return File(dir, "${safeName}.pdf")
    }

    private fun createPaints(template: InvoiceTemplate): Map<String, TextPaint> {
        // ...
        return emptyMap()
    }
}

private val PaperSize.isThermal: Boolean
    get() = this == PaperSize.THERMAL_58MM || this == PaperSize.THERMAL_80MM
