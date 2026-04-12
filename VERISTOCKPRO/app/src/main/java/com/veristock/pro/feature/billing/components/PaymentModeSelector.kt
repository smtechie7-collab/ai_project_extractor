package com.veristock.pro.feature.billing.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.veristock.pro.feature.billing.PaymentMode

@Composable
fun PaymentModeSelector(
    selectedMode: PaymentMode,
    onModeSelect: (PaymentMode) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        Text(
            text = "Payment Mode",
            style = MaterialTheme.typography.labelLarge
        )
        Spacer(Modifier.height(8.dp))
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            PaymentMode.entries.take(3).forEach { mode ->  // CASH, CARD, UPI only
                FilterChip(
                    selected = selectedMode == mode,
                    onClick = { onModeSelect(mode) },
                    label = { Text(mode.displayName) },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}