
package com.veristock.pro.data.dao

import androidx.room.*
import com.veristock.pro.data.entity.PrinterProfileEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface PrinterProfileDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(profile: PrinterProfileEntity)

    @Update
    suspend fun update(profile: PrinterProfileEntity)

    @Delete
    suspend fun delete(profile: PrinterProfileEntity)

    @Query("SELECT * FROM printer_profiles WHERE id = :id")
    suspend fun getProfileById(id: String): PrinterProfileEntity?

    @Query("SELECT * FROM printer_profiles WHERE deviceAddress = :address")
    suspend fun getProfileByAddress(address: String): PrinterProfileEntity?

    @Query("SELECT * FROM printer_profiles ORDER BY name ASC")
    fun getAllProfiles(): Flow<List<PrinterProfileEntity>>

    @Query("SELECT * FROM printer_profiles WHERE isDefault = 1 LIMIT 1")
    suspend fun getDefaultProfile(): PrinterProfileEntity?

    @Query("UPDATE printer_profiles SET isDefault = 0")
    suspend fun clearAllDefaults()
}
