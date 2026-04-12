package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.veristock.pro.data.entity.InvoicePdfMetadataEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface InvoicePdfMetadataDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(metadata: InvoicePdfMetadataEntity): Long

    @Query("SELECT * FROM invoice_pdf_metadata WHERE saleId = :saleId ORDER BY generatedAt DESC")
    fun getHistoryForSale(saleId: Long): Flow<List<InvoicePdfMetadataEntity>>

}
