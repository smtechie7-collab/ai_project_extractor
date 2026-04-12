package com.veristock.pro.domain.mapper

import com.veristock.pro.core.pdf.models.BusinessHeaderData
import com.veristock.pro.core.pdf.models.CustomerData
import com.veristock.pro.core.pdf.models.InvoiceData
import com.veristock.pro.core.pdf.models.LegalData
import com.veristock.pro.core.pdf.models.PaymentData
import com.veristock.pro.core.pdf.models.SaleData
import com.veristock.pro.core.pdf.models.SaleItemData
import com.veristock.pro.core.pdf.models.TotalsData
import com.veristock.pro.domain.model.Invoice
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

fun Invoice.toInvoiceData(): InvoiceData {
    val businessHeaderData = BusinessHeaderData(
        businessName = businessProfile.businessName,
        tagline = businessProfile.tagline,
        address = businessProfile.fullAddress,
        mobile = businessProfile.mobile,
        email = businessProfile.email,
        gstin = businessProfile.gstin,
        logo = null, // Not implemented
        cin = null, // Not implemented
        pan = null // Not implemented
    )

    val customerData = CustomerData(
        name = customer.name,
        mobile = customer.mobile,
        email = customer.email,
        billingAddress = customer.fullAddress ?: "",
        shippingAddress = customer.fullAddress ?: "",
        gstin = customer.gstin
    )

    val sdf = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())
    val saleData = SaleData(
        invoiceNumber = sale.invoiceNumber,
        date = sdf.format(Date(sale.invoiceDate)),
        placeOfSupply = customer.state,
        reverseCharge = false // Not implemented
    )

    val saleItemsData = items.mapIndexed { index, saleItem ->
        SaleItemData(
            serialNumber = index + 1,
            description = saleItem.productName,
            hsn = saleItem.productHsn,
            imei = saleItem.imeiNumbers,
            quantity = saleItem.quantity.toDouble(),
            rate = saleItem.unitPrice.toDouble(),
            gstRate = saleItem.gstRate.toDouble(),
            amount = saleItem.totalAmount.toDouble()
        )
    }

    val totalsData = TotalsData(
        subtotal = sale.subtotal.toDouble(),
        cgst = sale.cgstAmount.toDouble(),
        sgst = sale.sgstAmount.toDouble(),
        igst = sale.igstAmount.toDouble(),
        totalTax = sale.totalTax.toDouble(),
        grandTotal = sale.grandTotal.toDouble(),
        amountInWords = "", // Not implemented
        taxAmountInWords = "" // Not implemented
    )

    val paymentData = PaymentData(
        method = sale.paymentMode,
        transactionId = sale.paymentReference,
        status = sale.paymentStatus,
        qrCode = null, // Not implemented
        bankDetails = null // Not implemented
    )

    val legalData = LegalData(
        termsAndConditions = "", // Not implemented
        declaration = null // Not implemented
    )

    return InvoiceData(
        business = businessHeaderData,
        customer = customerData,
        sale = saleData,
        items = saleItemsData,
        totals = totalsData,
        payment = paymentData,
        legal = legalData
    )
}
