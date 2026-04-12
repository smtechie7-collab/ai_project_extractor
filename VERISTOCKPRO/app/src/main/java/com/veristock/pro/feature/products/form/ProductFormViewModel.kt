
package com.veristock.pro.feature.products.form

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.data.repository.ProductRepository
import com.veristock.pro.domain.model.Product
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.math.BigDecimal
import javax.inject.Inject

@HiltViewModel
class ProductFormViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle,
    private val repository: ProductRepository
) : ViewModel() {

    private val productId: Long = savedStateHandle.get<Long>("productId") ?: 0L

    private val _state = MutableStateFlow(ProductFormState())
    val state: StateFlow<ProductFormState> = _state.asStateFlow()

    private val gstOptions = listOf("0", "5", "12", "18", "28")

    init {
        if (productId > 0) {
            loadProduct(productId)
        }
    }

    private fun loadProduct(id: Long) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            val product = repository.getProductById(id)
            if (product != null) {
                _state.update {
                    it.copy(
                        id = product.id.toLong(),
                        name = product.name,
                        category = product.category,
                        brand = product.brand ?: "",
                        model = product.model ?: "",
                        hsnCode = product.hsnCode,
                        barcode = product.barcode ?: "",
                        mrp = product.mrp.toPlainString(),
                        sellingPrice = product.sellingPrice.toPlainString(),
                        purchasePrice = product.purchasePrice?.toPlainString() ?: "",
                        gstRate = product.gstRate.toPlainString(),
                        currentStock = product.currentStock.toString(),
                        minStockLevel = product.minStockLevel.toString(),
                        unit = product.unit,
                        hasImei = product.hasImei,
                        hasSerial = product.hasSerial,
                        warrantyMonths = product.warrantyMonths.toString(),
                        isLoading = false
                    )
                }
            } else {
                _state.update { it.copy(isLoading = false, errorMessage = "Product not found") }
            }
        }
    }

    // Field Update Functions
    fun updateName(value: String) = _state.update { it.copy(name = value, nameError = validateName(value)) }
    fun updateCategory(value: String) = _state.update { it.copy(category = value, categoryError = validateCategory(value)) }
    fun updateBrand(value: String) = _state.update { it.copy(brand = value) }
    fun updateModel(value: String) = _state.update { it.copy(model = value) }
    fun updateHsn(value: String) = _state.update { it.copy(hsnCode = value) }
    fun updateBarcode(value: String) = _state.update { it.copy(barcode = value) }
    fun updateMrp(value: String) = _state.update { it.copy(mrp = value, mrpError = validateMrp(value)) }
    fun updateSellingPrice(value: String) = _state.update { it.copy(sellingPrice = value, sellingPriceError = validateSellingPrice(value, it.mrp)) }
    fun updatePurchasePrice(value: String) = _state.update { it.copy(purchasePrice = value) }
    fun updateGstRate(value: String) = _state.update { it.copy(gstRate = value, gstRateError = validateGstRate(value)) }
    fun updateCurrentStock(value: String) = _state.update { it.copy(currentStock = value, stockError = validateStock(value)) }
    fun updateMinStockLevel(value: String) = _state.update { it.copy(minStockLevel = value, minStockError = validateMinStock(value)) }
    fun updateUnit(value: String) = _state.update { it.copy(unit = value) }
    fun updateHasImei(value: Boolean) = _state.update { it.copy(hasImei = value) }
    fun updateHasSerial(value: Boolean) = _state.update { it.copy(hasSerial = value) }
    fun updateWarranty(value: String) = _state.update { it.copy(warrantyMonths = value) }

    // Validation Logic
    private fun validateName(name: String): String? {
        return when {
            name.isBlank() -> "Name is required"
            name.length < 2 -> "Name must be at least 2 characters"
            name.length > 100 -> "Name cannot exceed 100 characters"
            else -> null
        }
    }

    private fun validateCategory(category: String): String? {
        return if (category.isBlank()) "Category is required" else null
    }

    private fun validateMrp(mrp: String): String? {
        return when {
            mrp.isBlank() -> "MRP is required"
            mrp.toBigDecimalOrNull() == null -> "Invalid number"
            mrp.toBigDecimal() < BigDecimal.ZERO -> "MRP must be positive"
            else -> null
        }
    }

    private fun validateSellingPrice(price: String, mrp: String): String? {
        val priceValue = price.toBigDecimalOrNull()
        val mrpValue = mrp.toBigDecimalOrNull()
        return when {
            price.isBlank() -> "Selling price is required"
            priceValue == null -> "Invalid number"
            priceValue < BigDecimal.ZERO -> "Price must be positive"
            mrpValue != null && priceValue > mrpValue -> "Selling price cannot be more than MRP"
            else -> null
        }
    }

    private fun validateGstRate(rate: String): String? {
        return if (rate !in gstOptions) "Invalid GST Rate" else null
    }

    private fun validateStock(stock: String): String? {
        return when {
            stock.isBlank() -> "Stock is required"
            stock.toIntOrNull() == null -> "Invalid number"
            stock.toInt() < 0 -> "Stock must be positive"
            else -> null
        }
    }

    private fun validateMinStock(minStock: String): String? {
        return when {
            minStock.isBlank() -> "Min stock is required"
            minStock.toIntOrNull() == null -> "Invalid number"
            minStock.toInt() < 0 -> "Min stock must be positive"
            else -> null
        }
    }

    private fun validateForm(): Boolean {
        val state = _state.value
        val nameError = validateName(state.name)
        val categoryError = validateCategory(state.category)
        val mrpError = validateMrp(state.mrp)
        val sellingPriceError = validateSellingPrice(state.sellingPrice, state.mrp)
        val gstRateError = validateGstRate(state.gstRate)
        val stockError = validateStock(state.currentStock)
        val minStockError = validateMinStock(state.minStockLevel)

        _state.update {
            it.copy(
                nameError = nameError,
                categoryError = categoryError,
                mrpError = mrpError,
                sellingPriceError = sellingPriceError,
                gstRateError = gstRateError,
                stockError = stockError,
                minStockError = minStockError
            )
        }

        return listOfNotNull(
            nameError, categoryError, mrpError, sellingPriceError, gstRateError, stockError, minStockError
        ).isEmpty()
    }

    fun saveProduct() {
        if (!validateForm()) return

        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val currentState = _state.value
                val product = Product(
                    id = currentState.id.toInt(),
                    name = currentState.name.trim(),
                    category = currentState.category,
                    brand = currentState.brand.trim().takeIf { it.isNotBlank() },
                    model = currentState.model.trim().takeIf { it.isNotBlank() },
                    hsnCode = currentState.hsnCode.trim(),
                    barcode = currentState.barcode.trim().takeIf { it.isNotBlank() },
                    mrp = currentState.mrp.toBigDecimal(),
                    sellingPrice = currentState.sellingPrice.toBigDecimal(),
                    purchasePrice = currentState.purchasePrice.toBigDecimalOrNull(),
                    gstRate = currentState.gstRate.toBigDecimal(),
                    currentStock = currentState.currentStock.toInt(),
                    minStockLevel = currentState.minStockLevel.toInt(),
                    unit = currentState.unit,
                    hasImei = currentState.hasImei,
                    hasSerial = currentState.hasSerial,
                    warrantyMonths = currentState.warrantyMonths.toIntOrNull() ?: 0
                )

                val result = if (product.id == 0) {
                    repository.insertProduct(product)
                } else {
                    repository.updateProduct(product)
                }

                if (result.isSuccess) {
                    _state.update { it.copy(isLoading = false, isSaved = true) }
                } else {
                    _state.update { it.copy(isLoading = false, errorMessage = result.exceptionOrNull()?.message) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, errorMessage = e.message ?: "An unknown error occurred") }
            }
        }
    }
}
