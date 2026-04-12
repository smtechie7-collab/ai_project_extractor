package com.veristock.pro.domain.model

data class BusinessProfile(
    val id: Int = 1,
    val businessName: String,
    val ownerName: String? = null,
    val businessType: String = "ELECTRONICS",
    val tagline: String? = null, // Added for invoice

    // Tax & Legal
    val gstin: String? = null,
    val pan: String? = null,
    val cin: String? = null, // Added for GST invoice
    val stateCode: String? = null,

    // Contact
    val mobile: String,
    val alternateMobile: String? = null,
    val email: String? = null,
    val website: String? = null,

    // Address
    val addressLine1: String? = null,
    val addressLine2: String? = null,
    val city: String? = null,
    val state: String? = "Gujarat",
    val pincode: String? = null,

    // Branding
    val logoPath: String? = null,

    // Invoice Config
    val invoicePrefix: String = "INV",
    val invoiceCounter: Int = 1,
    val invoiceSuffix: String? = null,

    // Financial Year
    val financialYearStart: String = "2024-04-01",
    val financialYearEnd: String = "2025-03-31",

    // Terms
    val termsAndConditions: String = "Goods once sold cannot be returned. Subject to jurisdiction.",

    // Banking
    val bankName: String? = null,
    val bankAccountNumber: String? = null,
    val bankIfsc: String? = null,
    val branchName: String? = null, // Added for GST invoice
    val upiId: String? = null,

    // Metadata
    val createdAt: Long? = null,
    val updatedAt: Long? = null
) {
    val isGSTRegistered: Boolean
        get() = !gstin.isNullOrBlank()

    val fullAddress: String
        get() = listOfNotNull(addressLine1, addressLine2, city, state, pincode)
            .filter { it.isNotBlank() }
            .joinToString(", ")
}
