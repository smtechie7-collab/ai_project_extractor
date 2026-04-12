package com.veristock.pro.core.session

import com.veristock.pro.data.repository.BusinessRepository
import com.veristock.pro.data.repository.SettingsRepository
import com.veristock.pro.domain.model.BusinessProfile
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.runBlocking
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Singleton that holds the current business profile in memory.
 * Initialized once at app startup from a persistent source.
 */
@Singleton
class BusinessSession @Inject constructor(
    settingsRepository: SettingsRepository,
    businessRepository: BusinessRepository
) {

    private val _businessProfile = MutableStateFlow<BusinessProfile?>(null)
    val businessProfile: StateFlow<BusinessProfile?> = _businessProfile.asStateFlow()

    private val _isSetupComplete = MutableStateFlow(false)
    val isSetupComplete: StateFlow<Boolean> = _isSetupComplete.asStateFlow()

    init {
        // This synchronous, blocking read is a valid pattern for determining
        // the app's critical initial state before the UI is composed.
        _isSetupComplete.value = runBlocking {
            settingsRepository.isAppSetupComplete()
        }

        if (_isSetupComplete.value) {
            _businessProfile.value = runBlocking { businessRepository.getBusinessProfileOnce() }
        }
    }

    /**
     * Updates the current business profile in the session.
     */
    fun updateProfile(profile: BusinessProfile) {
        _businessProfile.value = profile
        _isSetupComplete.value = true
    }

    /**
     * Gets the current business profile, throwing an exception if it's not available.
     */
    fun requireBusinessProfile(): BusinessProfile {
        return _businessProfile.value
            ?: throw IllegalStateException("Business session not initialized or setup is incomplete.")
    }

    /**
     * Checks if the business is in the same state as a customer for tax calculations.
     */
    fun isSameState(customerState: String?): Boolean {
        val businessState = _businessProfile.value?.state
        return customerState.isNullOrBlank() || customerState.equals(businessState, ignoreCase = true)
    }

    /**
     * Gets the state code for GST purposes.
     */
    fun getStateCode(): String? {
        return _businessProfile.value?.stateCode
    }

    /**
     * Checks if the business is registered for GST.
     */
    fun isGSTRegistered(): Boolean {
        return _businessProfile.value?.isGSTRegistered == true
    }
}