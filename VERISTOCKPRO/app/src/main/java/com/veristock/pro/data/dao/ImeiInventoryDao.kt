package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.veristock.pro.data.entity.ImeiInventoryEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ImeiInventoryDao {
    @Query("SELECT * FROM imei_inventory WHERE imei_number = :imei")
    suspend fun getByImei(imei: String): ImeiInventoryEntity?

    @Query("SELECT * FROM imei_inventory WHERE product_id = :productId AND status = 'IN_STOCK'")
    fun getAvailableStockForProduct(productId: Long): Flow<List<ImeiInventoryEntity>>

    @Query("SELECT * FROM imei_inventory WHERE status = :status")
    fun getInventoryByStatus(status: String): Flow<List<ImeiInventoryEntity>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(inventory: ImeiInventoryEntity): Long

    @Update
    suspend fun update(inventory: ImeiInventoryEntity)

    @Query("UPDATE imei_inventory SET status = :status, sale_id = :saleId, sale_item_id = :saleItemId, sale_date = :saleDate WHERE imei_number = :imei")
    suspend fun markAsSold(imei: String, saleId: Long, saleItemId: Long, saleDate: Long, status: String = "SOLD")
}