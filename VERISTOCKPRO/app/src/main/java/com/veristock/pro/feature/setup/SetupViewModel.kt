
package com.veristock.pro.feature.setup

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.veristock.pro.core.util.ImageCompressor
import com.veristock.pro.data.repository.BusinessRepository
import com.veristock.pro.data.repository.SettingsRepository
import com.veristock.pro.domain.model.BusinessProfile
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SetupUiState(
    val businessName: String = "",
    val businessNameError: String? = null,
    val gstin: String = "",
    val gstinError: String? = null,
    val mobile: String = "",
    val mobileError: String? = null,
    val address: String = "",
    val city: String = "",
    val state: String = "Gujarat",
    val pincode: String = "",
    val logoPath: String? = null,
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val isSetupComplete: Boolean = false
)

@HiltViewModel
class SetupViewModel @Inject constructor(
    application: Application,
    private val businessRepository: BusinessRepository,
    private val settingsRepository: SettingsRepository
) : AndroidViewModel(application) {

    private val _uiState = MutableStateFlow(SetupUiState())
    val uiState: StateFlow<SetupUiState> = _uiState.asStateFlow()

    fun onBusinessNameChange(name: String) {
        _uiState.update { it.copy(businessName = name, businessNameError = null) }
    }

    fun onGstinChange(gstin: String) {
        _uiState.update { it.copy(gstin = gstin, gstinError = null) }
    }

    fun onMobileChange(mobile: String) {
        _uiState.update { it.copy(mobile = mobile, mobileError = null) }
    }

    fun onAddressChange(address: String) {
        _uiState.update { it.copy(address = address) }
    }

    fun onCityChange(city: String) {
        _uiState.update { it.copy(city = city) }
    }

    fun onStateChange(state: String) {
        _uiState.update { it.copy(state = state) }
    }

    fun onPincodeChange(pincode: String) {
        _uiState.update { it.copy(pincode = pincode) }
    }

    fun onLogoSelected(uri: Uri) {
        viewModelScope.launch {
            val compressedFile = ImageCompressor.compressLogo(getApplication(), uri)
            _uiState.update { it.copy(logoPath = compressedFile?.absolutePath) }
        }
    }

    private fun validate(): Boolean {
        var isValid = true
        val currentState = _uiState.value

        if (currentState.businessName.length < 2) {
            _uiState.update { it.copy(businessNameError = "Business name must be at least 2 characters") }
            isValid = false
        }

        if (currentState.mobile.length != 10) {
            _uiState.update { it.copy(mobileError = "Mobile number must be 10 digits") }
            isValid = false
        }

        if (currentState.gstin.isNotEmpty() && currentState.gstin.length != 15) {
            _uiState.update { it.copy(gstinError = "GSTIN must be 15 characters") }
            isValid = false
        }

        return isValid
    }

    fun saveBusinessProfile() {
        if (!validate()) {
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val profile = BusinessProfile(
                    businessName = _uiState.value.businessName,
                    gstin = _uiState.value.gstin,
                    mobile = _uiState.value.mobile,
                    addressLine1 = _uiState.value.address,
                    city = _uiState.value.city,
                    state = _uiState.value.state,
                    pincode = _uiState.value.pincode,
                    logoPath = _uiState.value.logoPath
                )
                businessRepository.saveBusinessProfile(profile)
                settingsRepository.setAppSetupComplete(true)
                _uiState.update { it.copy(isLoading = false, isSetupComplete = true) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, errorMessage = e.message ?: "An unknown error occurred") }
            }
        }
    }
}
