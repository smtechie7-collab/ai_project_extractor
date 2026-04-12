package com.veristock.pro.domain.model

data class Invoice(
    val sale: Sale,
    val items: List<SaleItem>,
    val customer: Customer,
    val businessProfile: BusinessProfile
) {
    val isSameState: Boolean
        get() = customer.state.isNullOrBlank() ||
                customer.state.equals(businessProfile.state, ignoreCase = true)

    val taxType: String
        get() = if (isSameState) "CGST+SGST" else "IGST"
}
