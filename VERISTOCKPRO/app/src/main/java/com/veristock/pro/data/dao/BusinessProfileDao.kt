package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Update
import com.veristock.pro.data.entity.BusinessProfileEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface BusinessProfileDao {
    @Query("SELECT * FROM business_profile WHERE id = 1")
    fun getBusinessProfile(): Flow<BusinessProfileEntity?>

    // Added for transactional use (Suspend function instead of Flow)
    @Query("SELECT * FROM business_profile WHERE id = 1")
    suspend fun getBusinessProfileSuspend(): BusinessProfileEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(profile: BusinessProfileEntity)

    @Update
    suspend fun update(profile: BusinessProfileEntity)

    @Query("SELECT invoice_counter FROM business_profile WHERE id = 1")
    suspend fun getCurrentInvoiceCounter(): Int?

    @Query("UPDATE business_profile SET invoice_counter = invoice_counter + 1 WHERE id = 1")
    suspend fun incrementInvoiceCounter()

    /**
     * Atomically increments and returns the new invoice number.
     * This must be called from within a database transaction.
     */
    @Transaction
    suspend fun generateNextInvoiceNumberLocked(): Int {
        incrementInvoiceCounter()
        return getCurrentInvoiceCounter() ?: throw IllegalStateException("Invoice counter not initialized")
    }
}