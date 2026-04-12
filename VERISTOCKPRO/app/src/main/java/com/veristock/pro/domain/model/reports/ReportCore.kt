package com.veristock.pro.domain.model.reports

import java.time.LocalDate

// --- Core Report Structures ---

data class ReportResult<T>(
    val data: List<T>,
    val summary: ReportSummary,
    val metadata: ReportMetadata
)

data class ReportSummary(
    val totalAmount: Double,
    val totalCount: Int,
    val averageAmount: Double,
    val minAmount: Double,
    val maxAmount: Double,
    val growthPercentage: Double? = null
)

data class ReportMetadata(
    val generatedAt: Long,
    val filters: ReportFilters,
    val executionTime: Long, // milliseconds
    val recordCount: Int,
    val pageInfo: PageInfo? = null
)

data class PageInfo(
    val currentPage: Int,
    val totalPages: Int,
    val pageSize: Int,
    val totalRecords: Int
)

// --- Filter Structures ---

enum class DateRange {
    TODAY,
    YESTERDAY,
    THIS_WEEK,
    LAST_WEEK,
    THIS_MONTH,
    LAST_MONTH,
    THIS_QUARTER,
    THIS_YEAR,
    CUSTOM
}

enum class SortOrder {
    ASCENDING,
    DESCENDING
}

enum class SortField {
    DATE,
    AMOUNT,
    QUANTITY,
    PROFIT
}

data class ReportFilters(
    val dateRange: DateRange = DateRange.THIS_MONTH,
    val startDate: Long? = null,
    val endDate: Long? = null,
    val searchQuery: String? = null,
    val sortBy: SortField = SortField.DATE,
    val sortOrder: SortOrder = SortOrder.DESCENDING,
    val page: Int = 1,
    val pageSize: Int = 50
)
