package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Query
import com.veristock.pro.domain.model.reports.SalesReportRow
import com.veristock.pro.domain.model.reports.SalesSummaryByDay

@Dao
interface ReportsDao {

    @Query("""
        SELECT 
            DATE(s.invoice_date / 1000, 'unixepoch', 'localtime') as date,
            SUM(s.grand_total) as totalSales,
            COUNT(*) as transactionCount,
            AVG(s.grand_total) as averageTicketSize,
            SUM(CASE WHEN s.payment_mode = 'CASH' THEN s.grand_total ELSE 0 END) as cashSales,
            SUM(CASE WHEN s.payment_mode != 'CASH' THEN s.grand_total ELSE 0 END) as digitalSales
        FROM sales s
        WHERE s.invoice_date BETWEEN :startDate AND :endDate
        GROUP BY date
        ORDER BY date DESC
    """)
    suspend fun getSalesByDate(startDate: Long, endDate: Long): List<SalesSummaryByDay>

    @Query("""
        SELECT
            s.invoice_date as date,
            s.invoice_number as invoiceNumber,
            s.customer_name as customerName,
            (SELECT COUNT(*) FROM sale_items si WHERE si.sale_id = s.id) as itemCount,
            s.subtotal as subtotal,
            s.total_tax as taxAmount,
            s.grand_total as grandTotal,
            s.payment_mode as paymentMode,
            s.payment_status as paymentStatus
        FROM sales s
        WHERE s.invoice_date BETWEEN :startDate AND :endDate
        ORDER BY s.invoice_date DESC
    """)
    suspend fun getSalesReportByDateRange(startDate: Long, endDate: Long): List<SalesReportRow>
}
