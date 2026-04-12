
package com.veristock.pro.feature.products.list

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.data.repository.ProductRepository
import com.veristock.pro.domain.model.Product
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the Product List screen.
 */
data class ProductListState(
    val products: List<Product> = emptyList(),
    val filteredProducts: List<Product> = emptyList(),
    val searchQuery: String = "",
    val isLoading: Boolean = true,
    val showDeleteDialog: Boolean = false,
    val productToDelete: Product? = null,
    val errorMessage: String? = null
)

/**
 * ViewModel for the Product List screen.
 */
@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val productRepository: ProductRepository
) : ViewModel() {

    private val _state = MutableStateFlow(ProductListState())
    val state: StateFlow<ProductListState> = _state.asStateFlow()

    init {
        loadProducts()
    }

    /**
     * Loads the list of products from the repository.
     * Can be used for initial loading and for pull-to-refresh.
     */
    fun loadProducts() {
        viewModelScope.launch {
            productRepository.getAllActiveProducts()
                .onStart { _state.update { it.copy(isLoading = true) } }
                .catch { e ->
                    _state.update {
                        it.copy(
                            errorMessage = "Failed to load products: ${e.message}",
                            isLoading = false
                        )
                    }
                }
                .collect { productList ->
                    _state.update {
                        it.copy(
                            products = productList,
                            filteredProducts = productList,
                            isLoading = false,
                            searchQuery = "" // Reset search on refresh
                        )
                    }
                }
        }
    }

    /**
     * Searches the product list based on a query string.
     * The search is case-insensitive and checks the product name, brand, and category.
     * @param query The text to search for.
     */
    fun searchProducts(query: String) {
        _state.update { it.copy(searchQuery = query) }

        val filteredList = if (query.isBlank()) {
            _state.value.products
        } else {
            _state.value.products.filter {
                it.name.contains(query, ignoreCase = true) ||
                it.brand.orEmpty().contains(query, ignoreCase = true) ||
                it.category.orEmpty().contains(query, ignoreCase = true)
            }
        }
        _state.update { it.copy(filteredProducts = filteredList) }
    }

    /**
     * Shows the delete confirmation dialog for the selected product.
     * @param product The product to be deleted.
     */
    fun showDeleteConfirmation(product: Product) {
        _state.update { it.copy(showDeleteDialog = true, productToDelete = product) }
    }

    /**
     * Cancels the delete operation and closes the confirmation dialog.
     */
    fun cancelDelete() {
        _state.update { it.copy(showDeleteDialog = false, productToDelete = null) }
    }

    /**
     * Confirms the deletion of the product.
     * It calls the repository to delete the product and then hides the dialog.
     */
    fun confirmDelete() {
        val productToDelete = _state.value.productToDelete ?: return

        viewModelScope.launch {
            val result = productRepository.deleteProduct(productToDelete.id.toLong())

            if (result.isSuccess) {
                // The Flow will automatically update the list.
                _state.update { it.copy(showDeleteDialog = false, productToDelete = null) }
            } else {
                _state.update {
                    it.copy(
                        errorMessage = result.exceptionOrNull()?.message ?: "Error deleting product",
                        showDeleteDialog = false, // Hide dialog even on failure
                        productToDelete = null
                    )
                }
            }
        }
    }
}
