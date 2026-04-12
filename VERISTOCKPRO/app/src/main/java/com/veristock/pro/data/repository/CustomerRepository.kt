
package com.veristock.pro.data.repository

import com.veristock.pro.data.dao.CustomerDao
import com.veristock.pro.data.entity.CustomerEntity
import com.veristock.pro.domain.model.Customer
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.math.BigDecimal
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CustomerRepository @Inject constructor(
    private val customerDao: CustomerDao
) {

    fun getAllActiveCustomers(): Flow<List<Customer>> {
        return customerDao.getAllActiveCustomers().map { entities ->
            entities.map { it.toDomainModel() }
        }
    }

    suspend fun getCustomerById(id: Long): Customer? {
        return customerDao.getCustomerById(id)?.toDomainModel()
    }

    suspend fun getCustomerByMobile(mobile: String): Customer? {
        return customerDao.getCustomerByMobile(mobile)?.toDomainModel()
    }

    fun searchCustomers(query: String): Flow<List<Customer>> {
        return customerDao.searchCustomers(query).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }

    suspend fun getTotalOutstandingBalance(): Double {
        return customerDao.getTotalOutstandingBalance()?.toDoubleOrNull() ?: 0.0
    }

    suspend fun insertCustomer(customer: Customer): Result<Long> {
        return try {
            // Check if customer with same mobile exists
            val existing = customerDao.getCustomerByMobile(customer.mobile)
            if (existing != null) {
                return Result.failure(Exception("Customer with mobile ${customer.mobile} already exists"))
            }

            val entity = customer.toEntity()
            val customerId = customerDao.insert(entity)
            Result.success(customerId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateCustomer(customer: Customer): Result<Unit> {
        return try {
            val entity = customer.toEntity()
            customerDao.update(entity)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Quick customer creation (for billing flow)
     */
    suspend fun createQuickCustomer(name: String, mobile: String): Result<Long> {
        return try {
            // Check if exists
            val existing = customerDao.getCustomerByMobile(mobile)
            if (existing != null) {
                return Result.success(existing.id.toLong())
            }

            val customer = CustomerEntity(
                id = 0,
                name = name,
                mobile = mobile,
                alternateMobile = null,
                email = null,
                gstin = null,
                businessName = null,
                addressLine1 = null,
                addressLine2 = null,
                city = null,
                state = null,
                pincode = null,
                creditLimit = "0.0",
                outstandingBalance = "0.0",
                totalPurchases = "0.0",
                totalOrders = 0,
                lastPurchaseDate = null,
                notes = null,
                isActive = true,
                createdAt = System.currentTimeMillis(),
                updatedAt = System.currentTimeMillis()
            )

            val customerId = customerDao.insert(customer)
            Result.success(customerId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

private fun CustomerEntity.toDomainModel(): Customer {
    return Customer(
        id = id,
        name = name,
        mobile = mobile,
        alternateMobile = alternateMobile,
        email = email,
        gstin = gstin,
        businessName = businessName,
        addressLine1 = addressLine1,
        addressLine2 = addressLine2,
        city = city,
        state = state,
        pincode = pincode,
        creditLimit = creditLimit.toBigDecimal(),
        outstandingBalance = outstandingBalance.toBigDecimal(),
        totalPurchases = totalPurchases.toBigDecimal(),
        totalOrders = totalOrders,
        lastPurchaseDate = lastPurchaseDate,
        notes = notes,
        isActive = isActive,
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}

private fun Customer.toEntity(): CustomerEntity {
    return CustomerEntity(
        id = id,
        name = name,
        mobile = mobile,
        alternateMobile = alternateMobile,
        email = email,
        gstin = gstin,
        businessName = businessName,
        addressLine1 = addressLine1,
        addressLine2 = addressLine2,
        city = city,
        state = state,
        pincode = pincode,
        creditLimit = creditLimit.toPlainString(),
        outstandingBalance = outstandingBalance.toPlainString(),
        totalPurchases = totalPurchases.toPlainString(),
        totalOrders = totalOrders,
        lastPurchaseDate = lastPurchaseDate,
        notes = notes,
        isActive = isActive,
        createdAt = createdAt ?: System.currentTimeMillis(),
        updatedAt = System.currentTimeMillis()
    )
}
