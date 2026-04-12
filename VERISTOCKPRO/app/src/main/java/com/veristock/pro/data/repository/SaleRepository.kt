
package com.veristock.pro.data.repository

import androidx.room.withTransaction
import com.veristock.pro.core.database.AppDatabase
import com.veristock.pro.data.dao.*
import com.veristock.pro.data.entity.*
import com.veristock.pro.domain.model.Sale
import com.veristock.pro.domain.model.SaleItem
import com.veristock.pro.feature.billing.CartItem
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.math.BigDecimal
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SaleRepository @Inject constructor(
    private val database: AppDatabase,
    private val saleDao: SaleDao,
    private val saleItemDao: SaleItemDao,
    private val productDao: ProductDao,
    private val customerDao: CustomerDao,
    private val businessProfileDao: BusinessProfileDao,
    private val stockMovementDao: StockMovementDao
) {

    fun getRecentSales(): Flow<List<Sale>> {
        return saleDao.getRecentSales().map { list ->
            list.map { it.toDomainModel() }
        }
    }

    fun getSalesByDateRange(startDate: Long, endDate: Long): Flow<List<Sale>> {
        return saleDao.getSalesByDateRange(startDate, endDate).map { list ->
            list.map { it.toDomainModel() }
        }
    }

    suspend fun getSaleById(id: Int): Sale? {
        val saleEntity = saleDao.getSaleById(id.toLong()) ?: return null
        val itemsEntity = saleItemDao.getItemsForSale(id.toLong())

        val saleItems = itemsEntity.map { it.toDomainModel() }
        return saleEntity.toDomainModel().copy(items = saleItems)
    }

    suspend fun getTotalSalesAmount(startDate: Long): BigDecimal? {
        return saleDao.getTotalSalesAmount(startDate)?.let { BigDecimal(it) }
    }

    suspend fun getSalesCount(startDate: Long): Int {
        return saleDao.getSalesCount(startDate)
    }

    @Throws(Exception::class)
    suspend fun createSaleWithTransaction(
        sale: SaleEntity,
        items: List<SaleItemEntity>,
        cartItems: List<CartItem>
    ): Long {

        return database.withTransaction {
            val profile = businessProfileDao.getBusinessProfileSuspend()
                ?: throw IllegalStateException("Business Profile not found. Please complete business setup first.")

            val nextCounter = businessProfileDao.generateNextInvoiceNumberLocked()
            val fySuffix = getFinancialYearSuffix(profile.financialYearStart)
            val invoiceNumber = "${profile.invoicePrefix}/$fySuffix/${nextCounter.toString().padStart(5, '0')}"

            val saleIdLong = saleDao.insert(sale.copy(invoiceNumber = invoiceNumber))
            val saleIdInt = saleIdLong.toInt()

            saleItemDao.insertAll(items.map { it.copy(saleId = saleIdInt) })

            cartItems.forEach { cartItem ->
                val product = productDao.getByIdForUpdate(cartItem.product.id)
                    ?: throw Exception("Product with ID ${cartItem.product.id} not found.")

                val stockBefore = product.currentStock
                val stockAfter = stockBefore - cartItem.quantity

                if (stockAfter < 0) {
                    throw Exception("Insufficient stock for ${product.name}. Available: $stockBefore, Required: ${cartItem.quantity}")
                }

                productDao.updateStock(product.id, stockAfter)

                val stockMovement = StockMovementEntity(
                    productId = product.id,
                    movementType = "SALE",
                    referenceType = "SALE_INVOICE",
                    referenceId = saleIdInt,
                    referenceNumber = invoiceNumber,
                    quantityChange = -cartItem.quantity,
                    stockBefore = stockBefore,
                    stockAfter = stockAfter,
                    imeiId = null,
                    imeiNumber = null,
                    movementDate = System.currentTimeMillis(),
                    remarks = "Stock deducted for invoice $invoiceNumber",
                    createdBy = "SYSTEM",
                    createdAt = System.currentTimeMillis()
                )
                stockMovementDao.insert(stockMovement)
            }

            sale.customerId?.let { customerId ->
                customerDao.incrementStats(
                    customerId.toLong(),
                    sale.grandTotal, // This is now a String and matches the DAO
                    System.currentTimeMillis()
                )
            }

            saleIdLong
        }
    }

    private fun getFinancialYearSuffix(fyStart: String): String {
        return try {
            val year = fyStart.substring(0, 4).toInt()
            val nextYear = (year + 1).toString().substring(2, 4)
            "$year-$nextYear"
        } catch (e: Exception) {
            "24-25" // Fallback
        }
    }
}

private fun String.toBigDecimalOrZero(): BigDecimal = BigDecimal(this)
private fun String?.toBigDecimalOrZeroNullable(): BigDecimal? = this?.let { BigDecimal(it) }

private fun SaleEntity.toDomainModel(): Sale {
    return Sale(
        id = id.toLong(),
        customerId = customerId?.toLong(),
        invoiceNumber = invoiceNumber,
        invoiceDate = invoiceDate,
        customerName = customerName,
        customerMobile = customerMobile,
        customerGstin = customerGstin,
        customerAddress = customerAddress,
        customerState = customerState,
        grandTotal = grandTotal.toBigDecimalOrZero(),
        subtotal = subtotal.toBigDecimalOrZero(),
        taxableAmount = taxableAmount.toBigDecimalOrZero(),
        totalTax = totalTax.toBigDecimalOrZero(),
        totalAmount = totalAmount.toBigDecimalOrZero(),
        cgstAmount = cgstAmount.toBigDecimalOrZero(),
        sgstAmount = sgstAmount.toBigDecimalOrZero(),
        igstAmount = igstAmount.toBigDecimalOrZero(),
        roundOff = roundOff.toBigDecimalOrZero(),
        paymentStatus = paymentStatus,
        paymentMode = paymentMode,
        paidAmount = paidAmount.toBigDecimalOrZero(),
        paymentReference = paymentReference,
        paymentDetailsJson = paymentDetailsJson,
        saleType = saleType,
        invoiceType = invoiceType,
        printCount = printCount,
        lastPrintTime = lastPrintTime,
        isShared = isShared,
        sharedAt = sharedAt,
        notes = notes,
        internalNotes = internalNotes,
        createdBy = createdBy,
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}

private fun SaleItemEntity.toDomainModel(): SaleItem {
    return SaleItem(
        id = id.toLong(),
        saleId = saleId.toLong(),
        productId = productId.toLong(),
        productName = productName,
        productHsn = productHsn,
        productCategory = productCategory,
        quantity = quantity,
        unit = unit,
        mrp = mrp.toBigDecimalOrZeroNullable(),
        unitPrice = unitPrice.toBigDecimalOrZero(),
        discountPercent = discountPercent.toBigDecimalOrZero(),
        discountAmount = discountAmount.toBigDecimalOrZero(),
        taxableValue = taxableValue.toBigDecimalOrZero(),
        gstRate = gstRate.toBigDecimalOrZero(),
        cgstPercent = cgstPercent.toBigDecimalOrZero(),
        sgstPercent = sgstPercent.toBigDecimalOrZero(),
        igstPercent = igstPercent.toBigDecimalOrZero(),
        cgstAmount = cgstAmount.toBigDecimalOrZero(),
        sgstAmount = sgstAmount.toBigDecimalOrZero(),
        igstAmount = igstAmount.toBigDecimalOrZero(),
        totalTax = totalTax.toBigDecimalOrZero(),
        totalAmount = totalAmount.toBigDecimalOrZero(),
        imeiNumbers = imeiNumbers,
        serialNumbers = serialNumbers,
        createdAt = createdAt
    )
}
