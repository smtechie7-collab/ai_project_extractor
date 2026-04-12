
package com.veristock.pro.feature.billing

import com.veristock.pro.domain.model.Customer
import com.veristock.pro.domain.model.InvoiceCopyType
import com.veristock.pro.domain.model.PaperSize
import com.veristock.pro.domain.model.Product
import java.io.File
import java.math.BigDecimal
import java.math.RoundingMode

private val SCALE = 2
private val ROUNDING_MODE = RoundingMode.HALF_UP

data class CartItem(
    val product: Product,
    val quantity: Int,
    val unitPrice: BigDecimal, // Changed to BigDecimal
    val gstRate: BigDecimal      // Changed to BigDecimal
) {
    val subtotal: BigDecimal
        get() = unitPrice.multiply(BigDecimal(quantity)).setScale(SCALE, ROUNDING_MODE)

    val gstAmount: BigDecimal
        get() = subtotal.multiply(gstRate).divide(BigDecimal(100), SCALE, ROUNDING_MODE)

    val total: BigDecimal
        get() = subtotal.add(gstAmount).setScale(SCALE, ROUNDING_MODE)

    fun cgst(): BigDecimal = (gstAmount.divide(BigDecimal(2), SCALE, ROUNDING_MODE))
    fun sgst(): BigDecimal = (gstAmount.divide(BigDecimal(2), SCALE, ROUNDING_MODE))
    fun igst(): BigDecimal = gstAmount
}

enum class PaymentMode(val displayName: String) {
    CASH("Cash"),
    CARD("Card"),
    UPI("UPI"),
    MIXED("Mixed"),
    CREDIT("Credit")
}

data class BillingState(
    val cartItems: List<CartItem> = emptyList(),

    val customer: Customer? = null,
    val customerName: String = "",
    val customerMobile: String = "",

    val searchQuery: String = "",
    val searchResults: List<Product> = emptyList(),

    // All financial fields are now BigDecimal
    val subtotal: BigDecimal = BigDecimal.ZERO,
    val discountAmount: BigDecimal = BigDecimal.ZERO,
    val taxableAmount: BigDecimal = BigDecimal.ZERO,
    val cgstAmount: BigDecimal = BigDecimal.ZERO,
    val sgstAmount: BigDecimal = BigDecimal.ZERO,
    val igstAmount: BigDecimal = BigDecimal.ZERO,
    val totalTax: BigDecimal = BigDecimal.ZERO,
    val totalAmount: BigDecimal = BigDecimal.ZERO,
    val roundOff: BigDecimal = BigDecimal.ZERO,
    val grandTotal: BigDecimal = BigDecimal.ZERO,

    val paymentMode: PaymentMode = PaymentMode.CASH,
    val paymentReference: String = "",
    val paidAmount: BigDecimal = BigDecimal.ZERO,

    val isSaving: Boolean = false,
    val saleComplete: Boolean = false,
    val completedSaleId: Long? = null,
    val errorMessage: String? = null,
    val isCustomerSearchActive: Boolean = false,

    // PDF Generation State - Memory leak fixed
    val pdfGenerating: Boolean = false,
    val generatedPdfFile: File? = null,
    val pdfError: String? = null,
    val previewFile: File? = null, // Changed from Bitmap to File
    val regenerationComplete: Boolean = false,

    val copySelection: Map<InvoiceCopyType, Boolean> = mapOf(
        InvoiceCopyType.ORIGINAL to true,
        InvoiceCopyType.DUPLICATE to true,
        InvoiceCopyType.TRIPLICATE to false,
        InvoiceCopyType.OFFICE_COPY to false
    ),

    val paperSize: PaperSize = PaperSize.A4
) {
    val itemCount: Int get() = cartItems.sumOf { it.quantity }
    val canCheckout: Boolean get() = cartItems.isNotEmpty() && customerName.isNotBlank()
}

// The unsafe Double.round2() extension function has been removed.
