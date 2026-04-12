
package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Query
import androidx.room.Transaction

@Dao
interface InvoiceSequenceDao {

    /**
     * Atomically increments the invoice counter and returns the NEW value.
     * This is the key to preventing invoice number collisions.
     */
    @Query("UPDATE business_profile SET invoiceCounter = invoiceCounter + 1 WHERE id = 1")
    suspend fun incrementInvoiceCounter()

    @Query("SELECT invoiceCounter FROM business_profile WHERE id = 1")
    suspend fun getCurrentInvoiceCounter(): Int

    @Transaction
    suspend fun getNextInvoiceNumber(): Int {
        incrementInvoiceCounter()
        return getCurrentInvoiceCounter()
    }
}
