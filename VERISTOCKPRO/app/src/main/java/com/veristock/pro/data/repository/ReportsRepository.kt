package com.veristock.pro.data.repository

import com.veristock.pro.domain.model.reports.*

interface ReportsRepository {
    // Sales reports
    suspend fun getDailySalesSummary(dateMillis: Long): Result<SalesSummaryByDay>
    suspend fun getSalesReportByDateRange(filters: ReportFilters): Result<ReportResult<SalesReportRow>>
    
    // GST reports
    suspend fun getGstSummary(filters: ReportFilters): Result<GstSummary>
    suspend fun getGstr1Data(filters: ReportFilters): Result<List<Gstr1Row>>
    
    // Product reports
    suspend fun getProductSalesReport(filters: ReportFilters): Result<ReportResult<ProductSalesRow>>
    suspend fun getTopProducts(filters: ReportFilters, limit: Int = 10): Result<List<TopProduct>>
    
    // Customer reports
    suspend fun getCustomerPurchaseReport(filters: ReportFilters): Result<ReportResult<CustomerPurchaseRow>>
    suspend fun getCustomerSegmentation(): Result<List<CustomerSegment>>
}
