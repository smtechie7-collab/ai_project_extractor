
package com.veristock.pro.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Update
import com.veristock.pro.data.entity.ProductEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ProductDao {
    @Query("SELECT * FROM products WHERE is_active = 1 ORDER BY name ASC")
    fun getAllActiveProducts(): Flow<List<ProductEntity>>

    @Query("SELECT * FROM products WHERE id = :id")
    suspend fun getProductById(id: Long): ProductEntity?
    
    @Query("SELECT * FROM products WHERE id = :id")
    suspend fun getByIdForUpdate(id: Int): ProductEntity?

    /**
     * Efficiently fetches a list of products by their IDs.
     * This is the new bulk query for optimizing checkout.
     */
    @Query("SELECT * FROM products WHERE id IN (:ids)")
    suspend fun getProductsByIds(ids: List<Int>): List<ProductEntity>

    @Query("UPDATE products SET current_stock = :newStock WHERE id = :id")
    suspend fun updateStock(id: Int, newStock: Int)

    @Query("SELECT * FROM products WHERE barcode = :barcode AND is_active = 1")
    suspend fun getProductByBarcode(barcode: String): ProductEntity?

    @Query("""
        SELECT * FROM products 
        WHERE is_active = 1 
        AND (name LIKE '%' || :query || '%' OR model LIKE '%' || :query || '%')
        ORDER BY name ASC
        LIMIT 50
    """)
    fun searchProducts(query: String): Flow<List<ProductEntity>>

    @Query("SELECT * FROM products WHERE current_stock <= min_stock_level AND is_active = 1")
    fun getLowStockProducts(): Flow<List<ProductEntity>>

    @Query("SELECT COUNT(*) FROM products WHERE current_stock <= min_stock_level AND is_active = 1")
    suspend fun getLowStockProductCount(): Int

    @Query("SELECT COUNT(*) FROM products WHERE is_active = 1")
    suspend fun getTotalProductCount(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(product: ProductEntity): Long

    @Update
    suspend fun update(product: ProductEntity)

    @Query("UPDATE products SET is_active = 0 WHERE id = :id")
    suspend fun softDelete(id: Long)

    @Query("UPDATE products SET current_stock = current_stock + :quantity WHERE id = :id")
    suspend fun increaseStock(id: Long, quantity: Int)

    @Query("UPDATE products SET current_stock = current_stock - :quantity WHERE id = :id AND current_stock >= :quantity")
    suspend fun decreaseStock(id: Long, quantity: Int): Int  // Returns rows affected

    @Query("UPDATE products SET current_stock = :newStock WHERE id = :id")
    suspend fun setStock(id: Long, newStock: Int)

    @Transaction
    suspend fun updateStockWithValidation(id: Long, quantity: Int, isIncrease: Boolean): Boolean {
        return if (isIncrease) {
            increaseStock(id, quantity)
            true
        } else {
            val rowsAffected = decreaseStock(id, quantity)
            rowsAffected > 0  // True if stock was sufficient
        }
    }
}
