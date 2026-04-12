package com.veristock.pro.core.email

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.core.content.FileProvider
import com.veristock.pro.domain.model.Invoice
import java.io.File

class EmailManager(private val context: Context) {

    fun sendInvoiceEmail(invoice: Invoice, pdfFile: File) {
        val uri = FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", pdfFile)

        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "message/rfc822"
            putExtra(Intent.EXTRA_EMAIL, arrayOf(invoice.customer.email))
            putExtra(Intent.EXTRA_SUBJECT, "Invoice #${invoice.sale.invoiceNumber} from ${invoice.businessProfile.businessName}")
            putExtra(Intent.EXTRA_TEXT, EmailTemplate.createEmailBody(invoice))
            putExtra(Intent.EXTRA_STREAM, uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }

        try {
            context.startActivity(Intent.createChooser(intent, "Send Email"))
        } catch (e: Exception) {
            // Handle case where no email app is installed
        }
    }
}
