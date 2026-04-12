package com.veristock.pro.data.repository

import com.veristock.pro.data.dao.BusinessProfileDao
import com.veristock.pro.data.entity.BusinessProfileEntity
import com.veristock.pro.domain.model.BusinessProfile
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class BusinessRepository @Inject constructor(
    private val businessProfileDao: BusinessProfileDao
) {

    /**
     * Get business profile as Flow (reactive)
     */
    fun getBusinessProfile(): Flow<BusinessProfile?> {
        return businessProfileDao.getBusinessProfile().map { entity ->
            entity?.toDomainModel()
        }
    }

    /**
     * Get business profile once (suspend)
     */
    suspend fun getBusinessProfileOnce(): BusinessProfile? {
        val entity = businessProfileDao.getBusinessProfile().first()
        return entity?.toDomainModel()
    }

    /**
     * Create or update business profile
     */
    suspend fun saveBusinessProfile(profile: BusinessProfile): Result<Unit> {
        return try {
            val entity = profile.toEntity()
            businessProfileDao.insert(entity)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Update existing profile
     */
    suspend fun updateBusinessProfile(profile: BusinessProfile): Result<Unit> {
        return try {
            val entity = profile.toEntity()
            businessProfileDao.update(entity)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Check if business setup is complete
     */
    suspend fun isBusinessSetupComplete(): Boolean {
        val profile = businessProfileDao.getBusinessProfile().first()
        return profile != null && profile.businessName.isNotBlank()
    }

    /**
     * Get current invoice counter
     */
    suspend fun getCurrentInvoiceCounter(): Int {
        return businessProfileDao.getCurrentInvoiceCounter() ?: 1
    }

    /**
     * Increment invoice counter
     */
    suspend fun incrementInvoiceCounter() {
        businessProfileDao.incrementInvoiceCounter()
    }
}

// Extension functions for entity <-> domain mapping
private fun BusinessProfileEntity.toDomainModel(): BusinessProfile {
    return BusinessProfile(
        id = id,
        businessName = businessName,
        ownerName = ownerName,
        businessType = businessType,
        gstin = gstin,
        pan = pan,
        stateCode = stateCode,
        mobile = mobile,
        alternateMobile = alternateMobile,
        email = email,
        website = website,
        addressLine1 = addressLine1,
        addressLine2 = addressLine2,
        city = city,
        state = state,
        pincode = pincode,
        logoPath = logoPath,
        invoicePrefix = invoicePrefix,
        invoiceCounter = invoiceCounter,
        invoiceSuffix = invoiceSuffix,
        financialYearStart = financialYearStart,
        financialYearEnd = financialYearEnd,
        termsAndConditions = termsAndConditions,
        bankName = bankName,
        bankAccountNumber = bankAccountNumber,
        bankIfsc = bankIfsc,
        upiId = upiId,
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}

private fun BusinessProfile.toEntity(): BusinessProfileEntity {
    return BusinessProfileEntity(
        id = id,
        businessName = businessName,
        ownerName = ownerName,
        businessType = businessType,
        gstin = gstin,
        pan = pan,
        stateCode = stateCode,
        mobile = mobile,
        alternateMobile = alternateMobile,
        email = email,
        website = website,
        addressLine1 = addressLine1,
        addressLine2 = addressLine2,
        city = city,
        state = state ?: "Gujarat", // Fix: Handle nullable domain state
        pincode = pincode,
        logoPath = logoPath,
        invoicePrefix = invoicePrefix,
        invoiceCounter = invoiceCounter,
        invoiceSuffix = invoiceSuffix,
        financialYearStart = financialYearStart,
        financialYearEnd = financialYearEnd,
        termsAndConditions = termsAndConditions ?: "", // Fix: Handle nullable domain terms
        bankName = bankName,
        bankAccountNumber = bankAccountNumber,
        bankIfsc = bankIfsc,
        upiId = upiId,
        createdAt = createdAt ?: System.currentTimeMillis(),
        updatedAt = System.currentTimeMillis()
    )
}