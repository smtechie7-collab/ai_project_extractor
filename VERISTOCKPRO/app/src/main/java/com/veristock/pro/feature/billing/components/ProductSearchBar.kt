
package com.veristock.pro.feature.billing.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.unit.dp
import com.veristock.pro.domain.model.Product
import java.math.BigDecimal
import java.math.RoundingMode

@Composable
fun ProductSearchBar(
    searchQuery: String,
    searchResults: List<Product>,
    onSearchChange: (String) -> Unit,
    onProductSelect: (Product) -> Unit,
    onClearSearch: () -> Unit,
    modifier: Modifier = Modifier
) {
    var isSearchActive by remember { mutableStateOf(false) }

    Column(modifier = modifier.fillMaxWidth()) {
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { newQuery ->
                onSearchChange(newQuery)
                isSearchActive = newQuery.isNotBlank()
            },
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Search products...") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
            trailingIcon = {
                if (searchQuery.isNotBlank()) {
                    IconButton(onClick = {
                        onClearSearch()
                        isSearchActive = false
                    }) {
                        Icon(Icons.Default.Close, contentDescription = "Clear")
                    }
                }
            },
            singleLine = true,
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
            keyboardActions = KeyboardActions(onSearch = { /* Search already happening on change */ })
        )

        AnimatedVisibility(visible = isSearchActive && searchQuery.isNotBlank()) {
            Card(modifier = Modifier.fillMaxWidth(), elevation = CardDefaults.cardElevation(8.dp)) {
                if (searchResults.isEmpty()) {
                    Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                        Text("No products found", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                } else {
                    LazyColumn(modifier = Modifier.heightIn(max = 300.dp)) {
                        items(items = searchResults.take(10), key = { it.id }) { product ->
                            ProductSearchResultItem(
                                product = product,
                                onClick = {
                                    onProductSelect(product)
                                    onClearSearch()
                                    isSearchActive = false
                                }
                            )
                            if (product != searchResults.last()) {
                                HorizontalDivider()
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ProductSearchResultItem(product: Product, onClick: () -> Unit) {
    ListItem(
        headlineContent = { Text(product.name, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium) },
        supportingContent = {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text("₹${product.sellingPrice.setScale(2, RoundingMode.HALF_UP).toPlainString()}", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                Text(
                    text = "Stock: ${product.currentStock}",
                    style = MaterialTheme.typography.bodySmall,
                    color = when {
                        product.isOutOfStock -> MaterialTheme.colorScheme.error
                        product.isLowStock -> MaterialTheme.colorScheme.tertiary
                        else -> MaterialTheme.colorScheme.onSurfaceVariant
                    }
                )
            }
        },
        modifier = Modifier.clickable(onClick = onClick)
    )
}
