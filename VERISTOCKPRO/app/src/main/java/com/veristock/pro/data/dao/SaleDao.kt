
package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.veristock.pro.data.entity.SaleEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface SaleDao {
    @Query("SELECT * FROM sales ORDER BY invoice_date DESC LIMIT 100")
    fun getRecentSales(): Flow<List<SaleEntity>>

    @Query("SELECT * FROM sales WHERE id = :id")
    suspend fun getSaleById(id: Long): SaleEntity?

    @Query("SELECT * FROM sales WHERE invoice_number = :invoiceNumber")
    suspend fun getSaleByInvoiceNumber(invoiceNumber: String): SaleEntity?

    @Query("""
        SELECT * FROM sales 
        WHERE invoice_date >= :startDate AND invoice_date <= :endDate 
        ORDER BY invoice_date DESC
    """)
    fun getSalesByDateRange(startDate: Long, endDate: Long): Flow<List<SaleEntity>>

    @Query("SELECT * FROM sales WHERE payment_status = :status ORDER BY invoice_date DESC")
    fun getSalesByPaymentStatus(status: String): Flow<List<SaleEntity>>

    @Query("SELECT SUM(grand_total) FROM sales WHERE invoice_date >= :startDate")
    suspend fun getTotalSalesAmount(startDate: Long): String? // Changed to String

    @Query("SELECT COUNT(*) FROM sales WHERE invoice_date >= :startDate")
    suspend fun getSalesCount(startDate: Long): Int

    @Insert
    suspend fun insert(sale: SaleEntity): Long

    @Update
    suspend fun update(sale: SaleEntity)

    @Query("UPDATE sales SET print_count = print_count + 1, last_print_time = :printTime WHERE id = :id")
    suspend fun incrementPrintCount(id: Long, printTime: Long)
}
