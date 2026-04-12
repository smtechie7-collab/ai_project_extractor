
package com.veristock.pro.domain.model

import java.math.BigDecimal

data class Customer(
    val id: Int = 0,
    val name: String,
    val mobile: String,
    val alternateMobile: String? = null,
    val email: String? = null,

    val gstin: String? = null,
    val businessName: String? = null,

    val addressLine1: String? = null,
    val addressLine2: String? = null,
    val city: String? = null,
    val state: String? = null,
    val pincode: String? = null,

    // Financial fields now use BigDecimal for precision
    val creditLimit: BigDecimal = BigDecimal.ZERO,
    val outstandingBalance: BigDecimal = BigDecimal.ZERO,

    val totalPurchases: BigDecimal = BigDecimal.ZERO,
    val totalOrders: Int = 0,
    val lastPurchaseDate: Long? = null,

    val notes: String? = null,
    val isActive: Boolean = true,
    val createdAt: Long? = null,
    val updatedAt: Long? = null
) {
    val isB2B: Boolean
        get() = !gstin.isNullOrBlank()

    val hasOutstanding: Boolean
        get() = outstandingBalance > BigDecimal.ZERO

    val canGiveCredit: Boolean
        get() = outstandingBalance < creditLimit

    val fullAddress: String?
        get() = listOfNotNull(addressLine1, addressLine2, city, state, pincode)
            .filter { it.isNotBlank() }
            .joinToString(", ")
            .takeIf { it.isNotBlank() }
}
