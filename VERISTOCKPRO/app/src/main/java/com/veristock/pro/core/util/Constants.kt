package com.veristock.pro.core.util

object Constants {
    // GST Rates
    const val GST_5 = 5.0
    const val GST_12 = 12.0
    const val GST_18 = 18.0
    const val GST_28 = 28.0

    // Payment Modes
    const val PAYMENT_CASH = "CASH"
    const val PAYMENT_CARD = "CARD"
    const val PAYMENT_UPI = "UPI"
    const val PAYMENT_MIXED = "MIXED"
    const val PAYMENT_CREDIT = "CREDIT"

    // Payment Status
    const val PAYMENT_PAID = "PAID"
    const val PAYMENT_PARTIAL = "PARTIAL"
    const val PAYMENT_UNPAID = "UNPAID"

    // Sale Types
    const val SALE_B2C = "B2C"
    const val SALE_B2B = "B2B"

    // Stock Movement Types
    const val MOVEMENT_SALE = "SALE"
    const val MOVEMENT_PURCHASE = "PURCHASE"
    const val MOVEMENT_RETURN = "RETURN"
    const val MOVEMENT_ADJUSTMENT = "ADJUSTMENT"
    const val MOVEMENT_DAMAGE = "DAMAGE"
    const val MOVEMENT_OPENING = "OPENING_STOCK"

    // IMEI Status
    const val IMEI_IN_STOCK = "IN_STOCK"
    const val IMEI_SOLD = "SOLD"
    const val IMEI_RETURNED = "RETURNED"
    const val IMEI_DEFECTIVE = "DEFECTIVE"
    const val IMEI_SERVICE = "SERVICE"
}