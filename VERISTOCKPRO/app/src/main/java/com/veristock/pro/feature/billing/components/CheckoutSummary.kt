
package com.veristock.pro.feature.billing.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.veristock.pro.domain.model.InvoiceCopyType
import com.veristock.pro.domain.model.PaperSize
import com.veristock.pro.feature.billing.PaymentMode
import java.math.BigDecimal
import java.math.RoundingMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CheckoutSummary(
    subtotal: BigDecimal,
    cgstAmount: BigDecimal,
    sgstAmount: BigDecimal,
    igstAmount: BigDecimal,
    totalTax: BigDecimal,
    grandTotal: BigDecimal,
    paymentMode: PaymentMode,
    copySelection: Map<InvoiceCopyType, Boolean>,
    paperSize: PaperSize,
    onCopySelectionChanged: (InvoiceCopyType, Boolean) -> Unit,
    onPaperSizeChanged: (PaperSize) -> Unit,
    onPaymentModeChange: (PaymentMode) -> Unit,
    onPreview: () -> Unit,
    onCheckout: () -> Unit,
    canCheckout: Boolean,
    isLoading: Boolean,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(4.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Column(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("BILL SUMMARY", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            HorizontalDivider()

            SummaryRow("Subtotal", subtotal)

            if (cgstAmount > BigDecimal.ZERO || sgstAmount > BigDecimal.ZERO) {
                SummaryRow("CGST", cgstAmount)
                SummaryRow("SGST", sgstAmount)
            } else if (igstAmount > BigDecimal.ZERO) {
                SummaryRow("IGST", igstAmount)
            }

            HorizontalDivider()

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Grand Total", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("₹${grandTotal.toPlainString()}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            }

            Spacer(Modifier.height(8.dp))
            PaperSizeSelector(selectedSize = paperSize, onSizeSelected = onPaperSizeChanged)
            Spacer(Modifier.height(8.dp))
            CopySelectionRow(copySelection = copySelection, onCopySelectionChanged = onCopySelectionChanged)
            Spacer(Modifier.height(8.dp))
            PaymentModeSelector(selectedMode = paymentMode, onModeSelect = onPaymentModeChange)
            Spacer(Modifier.height(8.dp))

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onPreview, modifier = Modifier.weight(1f).height(56.dp), enabled = canCheckout && !isLoading) {
                    Text("Preview")
                }
                Button(onClick = onCheckout, modifier = Modifier.weight(2f).height(56.dp), enabled = canCheckout && !isLoading) {
                    if (isLoading) {
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                    } else {
                        Text("CHECKOUT - ₹${grandTotal.setScale(0, RoundingMode.HALF_UP).toPlainString()}", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
    }
}

@Composable
private fun SummaryRow(label: String, amount: BigDecimal) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, style = MaterialTheme.typography.bodyLarge)
        Text("₹${amount.setScale(2, RoundingMode.HALF_UP).toPlainString()}", style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
    }
}

@Composable
fun CopySelectionRow(
    copySelection: Map<InvoiceCopyType, Boolean>,
    onCopySelectionChanged: (InvoiceCopyType, Boolean) -> Unit
) {
    Column {
        Text("Generate Copies:", style = MaterialTheme.typography.titleSmall)
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) {
            copySelection.forEach { (type, isSelected) ->
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = isSelected, onCheckedChange = { onCopySelectionChanged(type, it) })
                    Text(type.name.lowercase().replaceFirstChar { it.uppercase() }, style = MaterialTheme.typography.bodyMedium)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PaperSizeSelector(
    selectedSize: PaperSize,
    onSizeSelected: (PaperSize) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }

    Column {
        Text("Paper Size:", style = MaterialTheme.typography.titleSmall)
        ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
            TextField(
                value = selectedSize.displayName,
                onValueChange = {},
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                modifier = Modifier.menuAnchor().fillMaxWidth()
            )
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                PaperSize.values().forEach { size ->
                    DropdownMenuItem(
                        text = { Text(size.displayName) },
                        onClick = {
                            onSizeSelected(size)
                            expanded = false
                        }
                    )
                }
            }
        }
    }
}
