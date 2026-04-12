package com.veristock.pro.core.email

import com.veristock.pro.domain.model.Invoice

object EmailTemplate {

    fun createEmailBody(invoice: Invoice): String {
        val business = invoice.businessProfile
        val sale = invoice.sale
        val customer = invoice.customer

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; color: #333; }
                .header { background: #1E3A8A; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .footer { background: #F3F4F6; padding: 15px; font-size: 12px; text-align: center; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>${business.businessName}</h1>
                <p>${business.tagline ?: ""}</p>
            </div>
            <div class="content">
                <p>Dear ${customer.name},</p>
                <p>Thank you for your business. Please find attached the invoice for your recent purchase.</p>
                <table>
                    <tr><td><strong>Invoice Number:</strong></td><td>${sale.invoiceNumber}</td></tr>
                    <tr><td><strong>Invoice Date:</strong></td><td>${sale.invoiceDate}</td></tr>
                    <tr><td><strong>Total Amount:</strong></td><td>₹${sale.grandTotal}</td></tr>
                    <tr><td><strong>Status:</strong></td><td>${sale.paymentStatus}</td></tr>
                </table>
                <p>If you have any questions, please feel free to contact us.</p>
            </div>
            <div class="footer">
                <p><strong>${business.businessName}</strong></p>
                <p>${business.addressLine1}, ${business.city}, ${business.state} ${business.pincode}</p>
                <p>Phone: ${business.mobile} | Email: ${business.email}</p>
                <p>GSTIN: ${business.gstin ?: ""}</p>
            </div>
        </body>
        </html>
        """
    }
}
