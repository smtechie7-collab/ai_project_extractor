
package com.veristock.pro.feature.billing

import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import androidx.core.content.FileProvider
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.core.email.EmailManager
import com.veristock.pro.core.pdf.InvoicePdfGenerator
import com.veristock.pro.core.pdf.models.*
import com.veristock.pro.core.session.BusinessSession
import com.veristock.pro.core.util.GSTCalculation
import com.veristock.pro.data.entity.SaleEntity
import com.veristock.pro.data.entity.SaleItemEntity
import com.veristock.pro.data.repository.CustomerRepository
import com.veristock.pro.data.repository.ProductRepository
import com.veristock.pro.data.repository.SaleRepository
import com.veristock.pro.domain.model.*
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.math.BigDecimal
import javax.inject.Inject

@HiltViewModel
class BillingViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
    private val productRepository: ProductRepository,
    private val customerRepository: CustomerRepository,
    private val saleRepository: SaleRepository,
    private val businessSession: BusinessSession,
    private val invoicePdfGenerator: InvoicePdfGenerator,
    private val emailManager: EmailManager
) : ViewModel() {

    private val _state = MutableStateFlow(BillingState())
    val state: StateFlow<BillingState> = _state.asStateFlow()

    private var businessProfile: BusinessProfile? = null
    private var searchJob: Job? = null

    init {
        loadBusinessProfile()
    }

    private fun loadBusinessProfile() {
        viewModelScope.launch {
            businessProfile = businessSession.requireBusinessProfile()
            if (_state.value.cartItems.isNotEmpty()) {
                calculateTotals()
            }
        }
    }
    
    fun onCopySelectionChanged(copyType: InvoiceCopyType, isSelected: Boolean) {
        val currentSelection = _state.value.copySelection.toMutableMap()
        currentSelection[copyType] = isSelected
        _state.update { it.copy(copySelection = currentSelection) }
    }

    fun setPaperSize(paperSize: PaperSize) {
        _state.update { it.copy(paperSize = paperSize) }
    }

    fun setPaymentMode(mode: PaymentMode) {
        _state.update { it.copy(paymentMode = mode) }
    }

    fun sharePdf(context: Context, file: File) {
        val uri = FileProvider.getUriForFile(context, "com.veristock.pro.fileprovider", file)
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "application/pdf"
            putExtra(Intent.EXTRA_STREAM, uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        context.startActivity(Intent.createChooser(intent, "Share Invoice"))
    }

    fun addToCart(product: Product, quantity: Int = 1) {
        if (quantity <= 0) return
        val originalCart = _state.value.cartItems
        val existingItem = originalCart.find { it.product.id == product.id }
        val newQuantity = (existingItem?.quantity ?: 0) + quantity

        val optimisticCart = if (existingItem != null) {
            originalCart.map { if (it.product.id == product.id) it.copy(quantity = newQuantity) else it }
        } else {
            originalCart + CartItem(product = product, quantity = quantity, unitPrice = product.sellingPrice, gstRate = product.gstRate)
        }
        _state.update { it.copy(cartItems = optimisticCart) }
        calculateTotals()

        viewModelScope.launch {
            val productInDb = productRepository.getProductById(product.id.toLong())
            if (productInDb == null || productInDb.currentStock < newQuantity) {
                _state.update { it.copy(cartItems = originalCart, errorMessage = "Insufficient stock for ${product.name}") }
                calculateTotals()
            }
        }
    }

    fun updateQuantity(productId: Int, quantity: Int) {
        val newCart = if (quantity > 0) {
            _state.value.cartItems.map { if (it.product.id == productId) it.copy(quantity = quantity) else it }
        } else {
            _state.value.cartItems.filter { it.product.id != productId }
        }
        _state.update { it.copy(cartItems = newCart) }
        calculateTotals()
    }

    fun removeFromCart(productId: Int) {
        val newCart = _state.value.cartItems.filter { it.product.id != productId }
        _state.update { it.copy(cartItems = newCart) }
        calculateTotals()
    }

    fun clearAfterSale() {
        _state.update { BillingState() }
    }

    fun clearPreview() {
        _state.value.previewFile?.delete()
        _state.update { it.copy(previewFile = null) }
    }

    fun setCustomer(customer: Customer?) {
        _state.update { it.copy(customer = customer, customerName = customer?.name ?: "", customerMobile = customer?.mobile ?: "") }
        calculateTotals()
    }

    fun updateCustomerName(name: String) {
        _state.update { it.copy(customerName = name) }
    }

    fun updateCustomerMobile(mobile: String) {
        if (mobile.length <= 10 && mobile.all { it.isDigit() }) {
            _state.update { it.copy(customerMobile = mobile) }
        }
    }

    fun searchProducts(query: String) {
        _state.update { it.copy(searchQuery = query) }
        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            delay(300)
            if (query.isNotBlank()) {
                productRepository.searchProducts(query).distinctUntilChanged()
                    .catch { e -> _state.update { it.copy(errorMessage = "Search failed: ${e.message}") } }
                    .onEach { results -> _state.update { it.copy(searchResults = results) } }.launchIn(this)
            } else {
                _state.update { it.copy(searchResults = emptyList()) }
            }
        }
    }

    fun clearSearch() {
        _state.update { it.copy(searchQuery = "", searchResults = emptyList()) }
    }

    private suspend fun validateStockBeforeCheckout(): Boolean {
        val cartItems = _state.value.cartItems
        if (cartItems.isEmpty()) return true
        val productIds = cartItems.map { it.product.id }
        val productsFromDb = productRepository.getProductsByIds(productIds)
        for (item in cartItems) {
            val productInDb = productsFromDb.find { it.id == item.product.id }
            if (productInDb == null || productInDb.currentStock < item.quantity) {
                _state.update { it.copy(errorMessage = "Insufficient stock for ${item.product.name}") }
                return false
            }
        }
        return true
    }

    fun checkout() {
        viewModelScope.launch {
            if (!validateStockBeforeCheckout()) return@launch
            _state.update { it.copy(isSaving = true) }
            try {
                val currentState = _state.value
                val profile = businessProfile ?: throw IllegalStateException("Business profile not found")
                val customerId = currentState.customer?.id

                val saleEntity = SaleEntity(
                    invoiceNumber = "TEMP",
                    invoiceDate = System.currentTimeMillis(),
                    customerId = customerId,
                    customerName = currentState.customerName,
                    customerMobile = currentState.customerMobile,
                    customerGstin = currentState.customer?.gstin,
                    customerAddress = currentState.customer?.fullAddress,
                    customerState = currentState.customer?.state,
                    subtotal = currentState.subtotal.toPlainString(),
                    discountType = "NONE",
                    discountPercent = "0.0",
                    discountAmount = currentState.discountAmount.toPlainString(),
                    taxableAmount = currentState.taxableAmount.toPlainString(),
                    cgstAmount = currentState.cgstAmount.toPlainString(),
                    sgstAmount = currentState.sgstAmount.toPlainString(),
                    igstAmount = currentState.igstAmount.toPlainString(),
                    totalTax = currentState.totalTax.toPlainString(),
                    totalAmount = currentState.totalAmount.toPlainString(),
                    roundOff = currentState.roundOff.toPlainString(),
                    grandTotal = currentState.grandTotal.toPlainString(),
                    paymentMode = currentState.paymentMode.name,
                    paymentStatus = if (currentState.paymentMode == PaymentMode.CREDIT) "DUE" else "PAID",
                    paidAmount = if (currentState.paymentMode == PaymentMode.CREDIT) "0.0" else currentState.grandTotal.toPlainString(),
                    paymentReference = currentState.paymentReference,
                    paymentDetailsJson = null,
                    lastPrintTime = null,
                    sharedAt = null,
                    notes = null,
                    internalNotes = null,
                    createdAt = System.currentTimeMillis(),
                    updatedAt = System.currentTimeMillis()
                )

                val itemEntities = currentState.cartItems.map { item ->
                    SaleItemEntity(
                        productId = item.product.id,
                        saleId = 0,
                        productName = item.product.name,
                        productHsn = item.product.hsnCode,
                        productCategory = item.product.category,
                        quantity = item.quantity,
                        unit = item.product.unit,
                        mrp = item.product.mrp.toPlainString(),
                        unitPrice = item.unitPrice.toPlainString(),
                        taxableValue = item.subtotal.toPlainString(),
                        gstRate = item.gstRate.toPlainString(),
                        totalTax = item.gstAmount.toPlainString(),
                        totalAmount = item.total.toPlainString(),
                        imeiNumbers = null,
                        serialNumbers = null,
                        createdAt = System.currentTimeMillis(),
                        discountAmount = "0.0",
                        discountPercent = "0.0",
                        cgstAmount = item.cgst().toPlainString(),
                        sgstAmount = item.sgst().toPlainString(),
                        igstAmount = item.igst().toPlainString(),
                        cgstPercent = if (item.igst() > BigDecimal.ZERO) "0.0" else item.gstRate.divide(BigDecimal(2)).toPlainString(),
                        sgstPercent = if (item.igst() > BigDecimal.ZERO) "0.0" else item.gstRate.divide(BigDecimal(2)).toPlainString(),
                        igstPercent = if (item.igst() > BigDecimal.ZERO) item.gstRate.toPlainString() else "0.0"
                    )
                }

                val saleId = saleRepository.createSaleWithTransaction(saleEntity, itemEntities, currentState.cartItems)
                _state.update { it.copy(isSaving = false, saleComplete = true, completedSaleId = saleId) }
                generateInvoicePdf(saleId)
            } catch (e: Exception) {
                _state.update { it.copy(isSaving = false, errorMessage = e.localizedMessage ?: "Checkout failed") }
            }
        }
    }

    fun generatePreview() {
        viewModelScope.launch {
            val currentState = _state.value
            val profile = businessProfile ?: return@launch
            val invoice = createInvoiceFromState(currentState, profile)
            val template = InvoiceTemplate(
                type = InvoiceTemplateType.MODERN,
                pageSize = currentState.paperSize,
                showLogo = true,
                tagline = profile.tagline,
                borderStyle = BorderStyle.SIMPLE,
                fontSize = FontSize.MEDIUM,
                colorScheme = ColorScheme.BLACK_WHITE,
                footerMessage = "Thank You!",
                showDecorations = false,
                useRegionalLanguage = false,
                regionalLanguage = null
            )
            val bitmap = invoicePdfGenerator.generatePreview(invoice, template)

            val previewFile = File(context.cacheDir, "preview_${System.currentTimeMillis()}.png")
            try {
                FileOutputStream(previewFile).use { out ->
                    bitmap.compress(Bitmap.CompressFormat.PNG, 80, out)
                }
                _state.value.previewFile?.delete()
                _state.update { it.copy(previewFile = previewFile) }
            } catch (e: IOException) {
                _state.update { it.copy(errorMessage = "Could not save preview file: ${e.localizedMessage}") }
            }
        }
    }

    private fun createInvoiceFromState(currentState: BillingState, profile: BusinessProfile): Invoice {
        val customer = currentState.customer ?: Customer(name = currentState.customerName, mobile = currentState.customerMobile)
        val sale = Sale(
            id = -1,
            invoiceNumber = "PREVIEW",
            invoiceDate = System.currentTimeMillis(),
            customerName = customer.name,
            subtotal = currentState.subtotal,
            taxableAmount = currentState.taxableAmount,
            totalTax = currentState.totalTax,
            totalAmount = currentState.totalAmount,
            grandTotal = currentState.grandTotal,
            paymentMode = currentState.paymentMode.name
        )
        val saleItems = currentState.cartItems.map { cartItem ->
            SaleItem(
                productId = cartItem.product.id.toLong(),
                productName = cartItem.product.name,
                quantity = cartItem.quantity,
                unitPrice = cartItem.unitPrice,
                taxableValue = cartItem.subtotal,
                gstRate = cartItem.gstRate,
                totalTax = cartItem.gstAmount,
                totalAmount = cartItem.total,
                mrp = cartItem.product.mrp
            )
        }
        return Invoice(sale, saleItems, customer, profile)
    }

    private fun generateInvoicePdf(saleId: Long) {
        viewModelScope.launch {
            _state.update { it.copy(pdfGenerating = true, generatedPdfFile = null, pdfError = null) }
            try {
                val savedSale = saleRepository.getSaleById(saleId.toInt()) ?: throw Exception("Saved sale not found")
                val customer = savedSale.customerId?.let { customerRepository.getCustomerById(it) } ?: Customer(name = savedSale.customerName, mobile = savedSale.customerMobile ?: "")
                val invoice = Invoice(savedSale, savedSale.items, customer, businessProfile!!)
                val template = InvoiceTemplate(
                    type = InvoiceTemplateType.MODERN,
                    pageSize = _state.value.paperSize,
                    showLogo = true,
                    tagline = businessProfile!!.tagline,
                    borderStyle = BorderStyle.SIMPLE,
                    fontSize = FontSize.MEDIUM,
                    colorScheme = ColorScheme.BLACK_WHITE,
                    footerMessage = "thank you",
                    showDecorations = false,
                    useRegionalLanguage = false,
                    regionalLanguage = null
                )
                val copySettings = _state.value.copySelection.filter { it.value }.map { (type, _) ->
                    CopySettings(copyType = type, headerText = "${type.name.lowercase().replaceFirstChar { it.uppercase() }} Copy", watermarkText = null, watermarkOpacity = 0f, showInFooter = false, colorIndicator = null)
                }

                val result = invoicePdfGenerator.generateInvoice(invoice, template, copySettings)
                result.onSuccess { file ->
                    _state.update { it.copy(pdfGenerating = false, generatedPdfFile = file) }
                }.onFailure { error ->
                    _state.update { it.copy(pdfGenerating = false, pdfError = error.message) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(pdfGenerating = false, pdfError = e.localizedMessage ?: "PDF generation failed.") }
            }
        }
    }

    private fun calculateTotals() {
        val items = _state.value.cartItems
        if (items.isEmpty()) {
            _state.update { it.copy(subtotal = BigDecimal.ZERO, taxableAmount = BigDecimal.ZERO, cgstAmount = BigDecimal.ZERO, sgstAmount = BigDecimal.ZERO, igstAmount = BigDecimal.ZERO, totalTax = BigDecimal.ZERO, totalAmount = BigDecimal.ZERO, roundOff = BigDecimal.ZERO, grandTotal = BigDecimal.ZERO) }
            return
        }

        val subtotal = items.fold(BigDecimal.ZERO) { acc, item -> acc.add(item.subtotal) }
        val discount = _state.value.discountAmount.min(subtotal)

        val businessState = businessProfile?.state ?: ""
        val customerState = _state.value.customer?.state ?: ""
        val isSameState = businessState.equals(customerState, ignoreCase = true) || customerState.isEmpty()

        val result = GSTCalculation.calculate(
            subtotal = subtotal,
            discountAmount = discount,
            gstRate = if (items.isNotEmpty()) items.first().gstRate else BigDecimal.ZERO,
            isSameState = isSameState
        )

        _state.update { it.copy(subtotal = result.subtotal, taxableAmount = result.taxableAmount, cgstAmount = result.cgst, sgstAmount = result.sgst, igstAmount = result.igst, totalTax = result.totalGST, totalAmount = result.totalWithTax, roundOff = result.roundOff, grandTotal = result.grandTotal) }
    }
}
