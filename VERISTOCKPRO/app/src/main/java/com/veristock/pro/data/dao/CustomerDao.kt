
package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.veristock.pro.data.entity.CustomerEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface CustomerDao {
    @Query("SELECT * FROM customers WHERE is_active = 1 ORDER BY name ASC")
    fun getAllActiveCustomers(): Flow<List<CustomerEntity>>

    @Query("SELECT * FROM customers WHERE id = :id")
    suspend fun getCustomerById(id: Long): CustomerEntity?

    @Query("SELECT * FROM customers WHERE mobile = :mobile AND is_active = 1")
    suspend fun getCustomerByMobile(mobile: String): CustomerEntity?

    @Query("""
        SELECT * FROM customers 
        WHERE is_active = 1 
        AND (name LIKE '%' || :query || '%' OR mobile LIKE '%' || :query || '%')
        ORDER BY name ASC
        LIMIT 50
    """)
    fun searchCustomers(query: String): Flow<List<CustomerEntity>>

    // Now returns String to be converted to BigDecimal
    @Query("SELECT SUM(outstanding_balance) FROM customers WHERE is_active = 1")
    suspend fun getTotalOutstandingBalance(): String?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(customer: CustomerEntity): Long

    @Update
    suspend fun update(customer: CustomerEntity)

    // Parameters updated to String
    @Query("UPDATE customers SET outstanding_balance = outstanding_balance + :amount WHERE id = :id")
    suspend fun addToOutstanding(id: Long, amount: String)

    @Query("UPDATE customers SET outstanding_balance = outstanding_balance - :amount WHERE id = :id")
    suspend fun subtractFromOutstanding(id: Long, amount: String)

    @Query("""
        UPDATE customers 
        SET total_purchases = total_purchases + :amount, 
            total_orders = total_orders + 1, 
            last_purchase_date = :date 
        WHERE id = :id
    """)
    suspend fun incrementStats(id: Long, amount: String, date: Long)
}
