package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Single row configuration table for the business profile.
 * Constraints: ID must be 1.
 */
@Entity(tableName = "business_profile")
data class BusinessProfileEntity(
    @PrimaryKey
    @ColumnInfo(name = "id")
    val id: Int = 1,

    // Basic Info
    @ColumnInfo(name = "business_name")
    val businessName: String,

    @ColumnInfo(name = "owner_name")
    val ownerName: String?,

    @ColumnInfo(name = "business_type", defaultValue = "ELECTRONICS")
    val businessType: String = "ELECTRONICS",

    // Tax Info
    @ColumnInfo(name = "gstin")
    val gstin: String?, // 15 characters

    @ColumnInfo(name = "pan")
    val pan: String?, // 10 characters

    @ColumnInfo(name = "state_code")
    val stateCode: String?, // e.g., "24"

    // Contact
    @ColumnInfo(name = "mobile")
    val mobile: String,

    @ColumnInfo(name = "alternate_mobile")
    val alternateMobile: String?,

    @ColumnInfo(name = "email")
    val email: String?,

    @ColumnInfo(name = "website")
    val website: String?,

    // Address
    @ColumnInfo(name = "address_line1")
    val addressLine1: String?,

    @ColumnInfo(name = "address_line2")
    val addressLine2: String?,

    @ColumnInfo(name = "city")
    val city: String?,

    @ColumnInfo(name = "state", defaultValue = "Gujarat")
    val state: String = "Gujarat",

    @ColumnInfo(name = "pincode")
    val pincode: String?,

    // Branding
    @ColumnInfo(name = "logo_path")
    val logoPath: String?,

    // Invoice Config
    @ColumnInfo(name = "invoice_prefix", defaultValue = "INV")
    val invoicePrefix: String = "INV",

    @ColumnInfo(name = "invoice_counter", defaultValue = "1")
    val invoiceCounter: Int = 1,

    @ColumnInfo(name = "invoice_suffix")
    val invoiceSuffix: String?,

    // Financial Year
    @ColumnInfo(name = "financial_year_start", defaultValue = "2024-04-01")
    val financialYearStart: String = "2024-04-01",

    @ColumnInfo(name = "financial_year_end", defaultValue = "2025-03-31")
    val financialYearEnd: String = "2025-03-31",

    // Terms & Conditions
    @ColumnInfo(name = "terms_and_conditions", defaultValue = "Goods once sold cannot be returned.")
    val termsAndConditions: String = "Goods once sold cannot be returned.",

    // Banking
    @ColumnInfo(name = "bank_name")
    val bankName: String?,

    @ColumnInfo(name = "bank_account_number")
    val bankAccountNumber: String?,

    @ColumnInfo(name = "bank_ifsc")
    val bankIfsc: String?,

    @ColumnInfo(name = "upi_id")
    val upiId: String?,

    // Metadata
    @ColumnInfo(name = "created_at")
    val createdAt: Long,

    @ColumnInfo(name = "updated_at")
    val updatedAt: Long
)