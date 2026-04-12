
package com.veristock.pro.feature.billing

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.veristock.pro.feature.billing.components.*
import com.veristock.pro.feature.customers.QuickCustomerDialog

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BillingScreen(
    onBackClick: () -> Unit,
    onViewInvoice: (Long) -> Unit,
    viewModel: BillingViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()
    val context = LocalContext.current
    val haptics = LocalHapticFeedback.current

    var showCustomerDialog by remember { mutableStateOf(false) }
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(state.errorMessage) {
        state.errorMessage?.let {
            snackbarHostState.showSnackbar(message = it, duration = SnackbarDuration.Short)
        }
    }

    if (state.saleComplete && state.completedSaleId != null) {
        SaleSuccessDialog(
            invoiceNumber = "INV-${state.completedSaleId}",
            totalAmount = state.grandTotal,
            saleId = state.completedSaleId!!,
            pdfGenerating = state.pdfGenerating,
            generatedPdfFile = state.generatedPdfFile,
            pdfError = state.pdfError,
            onNewSale = { viewModel.clearAfterSale() },
            onViewInvoice = { saleId ->
                onViewInvoice(saleId)
                viewModel.clearAfterSale()
            },
            onSharePdf = { file -> viewModel.sharePdf(context, file) },
            onOpenPdf = { file -> viewModel.sharePdf(context, file) },
            onEmailPdf = { /* viewModel.emailInvoice(state.completedSaleId!!, file) */ },
            onRegeneratePdf = { /* viewModel.regenerateInvoicePdf() */ },
            onDismiss = { viewModel.clearAfterSale() }
        )
    }

    if (showCustomerDialog) {
        QuickCustomerDialog(
            onDismiss = { showCustomerDialog = false },
            onCreateCustomer = { name, mobile, onSuccess, onError ->
                // viewModel.createQuickCustomer(name, mobile, onSuccess, onError)
            }
        )
    }

    state.previewFile?.let {
        InvoicePreviewDialog(
            previewFile = it,
            onDismiss = viewModel::clearPreview,
            onGeneratePdf = viewModel::checkout,
            isGenerating = state.isSaving
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("New Sale") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                },
                actions = {
                    if (state.itemCount > 0) {
                        BadgedBox(
                            badge = { Badge { Text("${state.itemCount}") } }
                        ) {
                            Icon(Icons.Default.ShoppingCart, "Cart", modifier = Modifier.padding(end = 16.dp))
                        }
                    }
                }
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        bottomBar = {
            if (state.cartItems.isNotEmpty()) {
                CheckoutSummary(
                    subtotal = state.subtotal,
                    cgstAmount = state.cgstAmount,
                    sgstAmount = state.sgstAmount,
                    igstAmount = state.igstAmount,
                    totalTax = state.totalTax,
                    grandTotal = state.grandTotal,
                    paymentMode = state.paymentMode,
                    copySelection = state.copySelection,
                    paperSize = state.paperSize,
                    onCopySelectionChanged = viewModel::onCopySelectionChanged,
                    onPaperSizeChanged = viewModel::setPaperSize,
                    onPaymentModeChange = { /* viewModel.setPaymentMode(it) */ },
                    onPreview = viewModel::generatePreview,
                    onCheckout = {
                        haptics.performHapticFeedback(HapticFeedbackType.LongPress)
                        viewModel.checkout()
                    },
                    canCheckout = state.canCheckout,
                    isLoading = state.isSaving,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            CustomerSection(
                customerName = state.customerName,
                customerMobile = state.customerMobile,
                onNameChange = { /* viewModel.updateCustomerName(it) */ },
                onMobileChange = { /* viewModel.updateCustomerMobile(it) */ },
                onAddCustomerClick = { showCustomerDialog = true },
                modifier = Modifier.padding(16.dp)
            )

            HorizontalDivider()

            ProductSearchBar(
                searchQuery = state.searchQuery,
                searchResults = state.searchResults,
                onSearchChange = { /* viewModel.searchProducts(it) */ },
                onProductSelect = { product ->
                    haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    viewModel.addToCart(product, quantity = 1)
                },
                onClearSearch = { /* viewModel.clearSearch() */ },
                modifier = Modifier.padding(16.dp)
            )

            HorizontalDivider()

            Box(modifier = Modifier.weight(1f)) {
                if (state.cartItems.isEmpty()) {
                    EmptyState(
                        icon = Icons.Default.ShoppingCart,
                        title = "Cart is empty",
                        message = "Search for products to add them to the cart."
                    )
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(
                            items = state.cartItems,
                            key = { it.product.id }
                        ) { cartItem ->
                            CartItemCard(
                                cartItem = cartItem,
                                onQuantityIncrease = {
                                    haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                                    viewModel.updateQuantity(cartItem.product.id, cartItem.quantity + 1)
                                },
                                onQuantityDecrease = {
                                    haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                                    viewModel.updateQuantity(cartItem.product.id, cartItem.quantity - 1)
                                },
                                onRemove = {
                                    haptics.performHapticFeedback(HapticFeedbackType.LongPress)
                                    // viewModel.removeFromCart(cartItem.product.id)
                                }
                            )
                        }
                    }
                }
            }
        }

        if (state.isSaving) {
            // Saving overlay...
        }
    }
}
