package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import com.veristock.pro.data.entity.StockMovementEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface StockMovementDao {
    @Insert
    suspend fun insert(movement: StockMovementEntity)

    @Query("SELECT * FROM stock_movements WHERE product_id = :productId ORDER BY movement_date DESC")
    fun getMovementsForProduct(productId: Long): Flow<List<StockMovementEntity>>

    @Query("SELECT * FROM stock_movements WHERE movement_date >= :startDate AND movement_date <= :endDate ORDER BY movement_date DESC")
    fun getMovementsByDateRange(startDate: Long, endDate: Long): Flow<List<StockMovementEntity>>
}