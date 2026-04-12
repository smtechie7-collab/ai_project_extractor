
package com.veristock.pro.feature.billing.components

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import java.io.File
import java.math.BigDecimal
import java.math.RoundingMode

@Composable
fun SaleSuccessDialog(
    invoiceNumber: String,
    totalAmount: BigDecimal, // Changed to BigDecimal
    saleId: Long,
    pdfGenerating: Boolean,
    generatedPdfFile: File?,
    pdfError: String?,
    onNewSale: () -> Unit,
    onViewInvoice: (Long) -> Unit,
    onSharePdf: (File) -> Unit,
    onOpenPdf: (File) -> Unit,
    onEmailPdf: (File) -> Unit,
    onRegeneratePdf: () -> Unit, // Simplified signature
    onDismiss: () -> Unit
) {
    var showRegenerateDialog by remember { mutableStateOf(false) }

    if (showRegenerateDialog) {
        RegeneratePdfDialog(
            onDismiss = { showRegenerateDialog = false },
            onConfirm = { _, _ ->
                onRegeneratePdf()
                showRegenerateDialog = false
            }
        )
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        icon = { Icon(Icons.Default.CheckCircle, contentDescription = "Success", modifier = Modifier.size(48.dp)) },
        title = { Text(text = "Sale Complete") },
        text = {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Invoice: $invoiceNumber", textAlign = TextAlign.Center)
                Text("Total: ₹${totalAmount.setScale(2, RoundingMode.HALF_UP).toPlainString()}", style = MaterialTheme.typography.titleLarge, textAlign = TextAlign.Center)
                Spacer(modifier = Modifier.height(16.dp))

                when {
                    pdfGenerating -> {
                        CircularProgressIndicator()
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Generating PDF...")
                    }
                    generatedPdfFile != null -> {
                        // Action buttons for the generated PDF
                    }
                    pdfError != null -> {
                        Text("PDF Error: $pdfError", color = MaterialTheme.colorScheme.error)
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onNewSale) {
                Text("New Sale")
            }
        },
        dismissButton = {
            TextButton(onClick = { onViewInvoice(saleId) }) {
                Text("Details")
            }
        }
    )
}
