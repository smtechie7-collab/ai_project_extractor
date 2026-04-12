package com.veristock.pro.feature.billing.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Checkbox
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.veristock.pro.core.pdf.models.BorderStyle
import com.veristock.pro.core.pdf.models.ColorScheme
import com.veristock.pro.core.pdf.models.FontSize
import com.veristock.pro.core.pdf.models.InvoiceTemplate
import com.veristock.pro.core.pdf.models.InvoiceTemplateType
import com.veristock.pro.domain.model.CopySettings
import com.veristock.pro.domain.model.InvoiceCopyType
import com.veristock.pro.domain.model.PaperSize

@Composable
fun RegeneratePdfDialog(
    onDismiss: () -> Unit,
    onConfirm: (template: InvoiceTemplate, copies: List<CopySettings>) -> Unit
) {
    var selectedTemplate by remember { mutableStateOf(InvoiceTemplate(
        type = InvoiceTemplateType.MODERN,
        showLogo = true,
        tagline = null,
        borderStyle = BorderStyle.SIMPLE,
        fontSize = FontSize.MEDIUM,
        colorScheme = ColorScheme.BLACK_WHITE,
        footerMessage = "Thank you for your business!",
        showDecorations = false,
        useRegionalLanguage = false,
        regionalLanguage = null,
        pageSize = PaperSize.A4
    )) }
    val copySelection = remember {
        mutableStateMapOf(
            InvoiceCopyType.ORIGINAL to true,
            InvoiceCopyType.DUPLICATE to false,
            InvoiceCopyType.TRIPLICATE to false,
            InvoiceCopyType.OFFICE_COPY to false
        )
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Regenerate PDF") },
        text = {
            Column {
                Text("Choose a template and the copies to generate.")
                Spacer(modifier = Modifier.height(16.dp))

                // Simplified template selector for this example
                // A real implementation would have a dropdown or list of templates
                Text("Template: Modern (Default)")

                Spacer(modifier = Modifier.height(16.dp))

                Text("Copies to generate:")
                copySelection.forEach { (type, isSelected) ->
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = isSelected, onCheckedChange = { copySelection[type] = it })
                        Text(type.name.lowercase().replaceFirstChar { it.uppercase() })
                    }
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    val selectedCopies = copySelection.filter { it.value }.map { (type, _) ->
                        when (type) {
                            InvoiceCopyType.ORIGINAL -> CopySettings(InvoiceCopyType.ORIGINAL, "Original for Recipient", null, 0f, true, null)
                            InvoiceCopyType.DUPLICATE -> CopySettings(InvoiceCopyType.DUPLICATE, "Duplicate for Supplier", "DUPLICATE", 0.3f, true, null)
                            InvoiceCopyType.TRIPLICATE -> CopySettings(InvoiceCopyType.TRIPLICATE, "Triplicate for Transporter", "TRIPLICATE", 0.3f, true, null)
                            InvoiceCopyType.OFFICE_COPY -> CopySettings(InvoiceCopyType.OFFICE_COPY, "Office Copy", "OFFICE COPY", 0.3f, true, null)
                            else -> CopySettings(InvoiceCopyType.ORIGINAL, "Original for Recipient", null, 0f, true, null)
                        }
                    }
                    onConfirm(selectedTemplate, selectedCopies)
                }
            ) {
                Text("Regenerate")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
