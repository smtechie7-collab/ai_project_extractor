
package com.veristock.pro.data.repository

import com.veristock.pro.core.util.Constants
import com.veristock.pro.data.dao.ProductDao
import com.veristock.pro.data.dao.StockMovementDao
import com.veristock.pro.data.entity.ProductEntity
import com.veristock.pro.data.entity.StockMovementEntity
import com.veristock.pro.domain.model.Product
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.math.BigDecimal
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ProductRepository @Inject constructor(
    private val productDao: ProductDao,
    private val stockMovementDao: StockMovementDao
) {

    fun getAllActiveProducts(): Flow<List<Product>> {
        return productDao.getAllActiveProducts().map { entities ->
            entities.map { it.toDomainModel() }
        }
    }

    suspend fun getProductById(id: Long): Product? {
        return productDao.getProductById(id)?.toDomainModel()
    }

    suspend fun getProductsByIds(ids: List<Int>): List<Product> {
        return productDao.getProductsByIds(ids).map { it.toDomainModel() }
    }

    suspend fun getProductByBarcode(barcode: String): Product? {
        return productDao.getProductByBarcode(barcode)?.toDomainModel()
    }

    fun searchProducts(query: String): Flow<List<Product>> {
        return productDao.searchProducts(query).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }

    fun getLowStockProducts(): Flow<List<Product>> {
        return productDao.getLowStockProducts().map { entities ->
            entities.map { it.toDomainModel() }
        }
    }

    suspend fun getLowStockProductCount(): Int {
        return productDao.getLowStockProductCount()
    }

    suspend fun getTotalProductCount(): Int {
        return productDao.getTotalProductCount()
    }

    suspend fun insertProduct(product: Product): Result<Long> {
        return try {
            val entity = product.toEntity()
            val productId = productDao.insert(entity)

            if (product.currentStock > 0) {
                recordStockMovement(
                    productId = productId,
                    movementType = Constants.MOVEMENT_OPENING,
                    quantityChange = product.currentStock,
                    stockBefore = 0,
                    stockAfter = product.currentStock,
                    remarks = "Opening stock"
                )
            }

            Result.success(productId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateProduct(product: Product): Result<Unit> {
        return try {
            val entity = product.toEntity()
            productDao.update(entity)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deleteProduct(productId: Long): Result<Unit> {
        return try {
            val product = getProductById(productId)
            if (product != null) {
                val updatedProduct = product.copy(isActive = false)
                updateProduct(updatedProduct)
            } else {
                Result.failure(Exception("Product not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private suspend fun recordStockMovement(
        productId: Long,
        movementType: String,
        quantityChange: Int,
        stockBefore: Int,
        stockAfter: Int,
        remarks: String? = null
    ) {
        val movement = StockMovementEntity(
            productId = productId.toInt(),
            movementType = movementType,
            quantityChange = quantityChange,
            stockBefore = stockBefore,
            stockAfter = stockAfter,
            remarks = remarks,
            movementDate = System.currentTimeMillis(),
            createdAt = System.currentTimeMillis(),
            referenceType = null,
            referenceId = null,
            referenceNumber = null,
            imeiId = null,
            imeiNumber = null
        )
        stockMovementDao.insert(movement)
    }
}

private fun String.toBigDecimalOrZero(): BigDecimal = BigDecimal(this)
private fun String?.toBigDecimalOrZeroNullable(): BigDecimal? = this?.let { BigDecimal(it) }

private fun ProductEntity.toDomainModel(): Product {
    return Product(
        id = id,
        name = name,
        description = description,
        category = category,
        brand = brand,
        model = model,
        sku = sku,
        hsnCode = hsnCode,
        barcode = barcode,
        mrp = mrp.toBigDecimalOrZero(),
        sellingPrice = sellingPrice.toBigDecimalOrZero(),
        purchasePrice = purchasePrice.toBigDecimalOrZeroNullable(),
        gstRate = gstRate.toBigDecimalOrZero(),
        currentStock = currentStock,
        minStockLevel = minStockLevel,
        maxStockLevel = maxStockLevel,
        unit = unit,
        hasImei = hasImei,
        hasSerial = hasSerial,
        warrantyMonths = warrantyMonths,
        isActive = isActive,
        isFeatured = isFeatured,
        imagePath = imagePath,
        notes = notes,
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}

private fun Product.toEntity(): ProductEntity {
    return ProductEntity(
        id = id,
        name = name,
        description = description,
        category = category,
        brand = brand,
        model = model,
        sku = sku ?: "SKU${System.currentTimeMillis()}",
        hsnCode = hsnCode,
        barcode = barcode,
        mrp = mrp.toPlainString(),
        sellingPrice = sellingPrice.toPlainString(),
        purchasePrice = purchasePrice?.toPlainString(),
        gstRate = gstRate.toPlainString(),
        currentStock = currentStock,
        minStockLevel = minStockLevel,
        maxStockLevel = maxStockLevel,
        unit = unit,
        hasImei = hasImei, // Corrected typo from hasIimei
        hasSerial = hasSerial,
        warrantyMonths = warrantyMonths,
        isActive = isActive,
        isFeatured = isFeatured,
        imagePath = imagePath,
        notes = notes,
        createdAt = createdAt ?: System.currentTimeMillis(),
        updatedAt = System.currentTimeMillis()
    )
}
