package com.veristock.pro.domain.model

enum class InvoiceCopyType {
    ORIGINAL,           // Main copy for customer
    DUPLICATE,          // Business records
    TRIPLICATE,         // Transport/logistics
    QUADRUPLICATE,      // Tax records
    OFFICE_COPY,        // Internal use
    CUSTOMER_COPY       // Alias for ORIGINAL
}
