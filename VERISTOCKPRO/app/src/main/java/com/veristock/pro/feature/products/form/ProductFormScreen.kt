package com.veristock.pro.feature.products.form

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductFormScreen(
    onSaveComplete: () -> Unit,
    onBackClick: () -> Unit,
    viewModel: ProductFormViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(state.isSaved) {
        if (state.isSaved) {
            onSaveComplete()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (state.id == 0L) "Add Product" else "Edit Product") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            Button(
                onClick = viewModel::saveProduct,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                enabled = !state.isLoading
            ) {
                if (state.isLoading) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.dp)
                } else {
                    Text("Save Product")
                }
            }
        }
    ) { padding ->
        if (state.isLoading && state.id > 0) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(horizontal = 16.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Basic Info Section
                SectionTitle("Basic Information")
                OutlinedTextField(
                    value = state.name,
                    onValueChange = viewModel::updateName,
                    label = { Text("Product Name*") },
                    isError = state.nameError != null,
                    modifier = Modifier.fillMaxWidth()
                )
                state.nameError?.let { ErrorText(it) }

                FormDropdown(
                    label = "Category*",
                    options = listOf("Mobile", "Accessory", "Tablet", "Laptop", "Smartwatch", "Audio", "Gaming", "Other"),
                    selected = state.category,
                    onSelected = viewModel::updateCategory,
                    error = state.categoryError
                )

                OutlinedTextField(value = state.brand, onValueChange = viewModel::updateBrand, label = { Text("Brand") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = state.model, onValueChange = viewModel::updateModel, label = { Text("Model") }, modifier = Modifier.fillMaxWidth())

                // Identification Section
                SectionTitle("Identification")
                OutlinedTextField(value = state.hsnCode, onValueChange = viewModel::updateHsn, label = { Text("HSN Code") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = state.barcode, onValueChange = viewModel::updateBarcode, label = { Text("Barcode") }, modifier = Modifier.fillMaxWidth())

                // Pricing Section
                SectionTitle("Pricing")
                PriceInputField(label = "MRP*", value = state.mrp, onValueChange = viewModel::updateMrp, error = state.mrpError)
                PriceInputField(label = "Selling Price*", value = state.sellingPrice, onValueChange = viewModel::updateSellingPrice, error = state.sellingPriceError)
                PriceInputField(label = "Purchase Price", value = state.purchasePrice, onValueChange = viewModel::updatePurchasePrice)
                FormDropdown(
                    label = "GST Rate*",
                    options = listOf("0", "5", "12", "18", "28"),
                    selected = state.gstRate,
                    onSelected = viewModel::updateGstRate,
                    error = state.gstRateError
                )

                // Inventory Section
                SectionTitle("Inventory")
                StockInputField(label = "Current Stock*", value = state.currentStock, onValueChange = viewModel::updateCurrentStock, error = state.stockError)
                StockInputField(label = "Min Stock Level*", value = state.minStockLevel, onValueChange = viewModel::updateMinStockLevel, error = state.minStockError)
                OutlinedTextField(value = state.unit, onValueChange = viewModel::updateUnit, label = { Text("Unit (e.g., Piece)") }, modifier = Modifier.fillMaxWidth())

                // Electronics Section
                SectionTitle("Electronics (Optional)")
                SwitchRow(label = "Has IMEI", checked = state.hasImei, onCheckedChange = viewModel::updateHasImei)
                SwitchRow(label = "Has Serial Number", checked = state.hasSerial, onCheckedChange = viewModel::updateHasSerial)
                StockInputField(label = "Warranty (in months)", value = state.warrantyMonths, onValueChange = viewModel::updateWarranty)

                Spacer(Modifier.height(80.dp)) // Spacer for bottom button
            }
        }
    }
}

@Composable
private fun SectionTitle(title: String) {
    Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 16.dp, bottom = 8.dp))
}

@Composable
private fun ErrorText(text: String) {
    Text(text, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall, modifier = Modifier.padding(start = 16.dp))
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun FormDropdown(label: String, options: List<String>, selected: String, onSelected: (String) -> Unit, error: String?) {
    var expanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
        OutlinedTextField(
            value = selected,
            onValueChange = {},
            modifier = Modifier.fillMaxWidth().menuAnchor(MenuAnchorType.PrimaryNotEditable),
            readOnly = true,
            label = { Text(label) },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            isError = error != null
        )
        ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { option ->
                DropdownMenuItem(text = { Text(option) }, onClick = { onSelected(option); expanded = false })
            }
        }
    }
    error?.let { ErrorText(it) }
}

@Composable
private fun PriceInputField(label: String, value: String, onValueChange: (String) -> Unit, error: String? = null) {
    val pattern = remember { Regex("^\\d*(\\.\\d{0,2})?$") }
    OutlinedTextField(
        value = value,
        onValueChange = { 
            if (it.isEmpty() || it.matches(pattern)) {
                onValueChange(it)
            }
         },
        label = { Text(label) },
        isError = error != null,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
        modifier = Modifier.fillMaxWidth()
    )
    error?.let { ErrorText(it) }
}

@Composable
private fun StockInputField(label: String, value: String, onValueChange: (String) -> Unit, error: String? = null) {
    OutlinedTextField(
        value = value,
        onValueChange = { 
            if (it.isEmpty() || it.all { char -> char.isDigit() }) {
                onValueChange(it)
            }
        },
        label = { Text(label) },
        isError = error != null,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
        modifier = Modifier.fillMaxWidth()
    )
    error?.let { ErrorText(it) }
}

@Composable
private fun SwitchRow(label: String, checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(label)
        Switch(checked = checked, onCheckedChange = onCheckedChange)
    }
}
