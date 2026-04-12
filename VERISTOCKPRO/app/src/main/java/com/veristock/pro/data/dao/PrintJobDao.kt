
package com.veristock.pro.data.dao

import androidx.room.*
import com.veristock.pro.data.entity.PrintJobEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface PrintJobDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(job: PrintJobEntity)

    @Update
    suspend fun update(job: PrintJobEntity)

    @Delete
    suspend fun delete(job: PrintJobEntity)

    @Query("SELECT * FROM print_jobs WHERE id = :id")
    suspend fun getJobById(id: String): PrintJobEntity?

    @Query("SELECT * FROM print_jobs ORDER BY createdAt ASC")
    fun getAllJobs(): Flow<List<PrintJobEntity>>

    @Query("SELECT * FROM print_jobs WHERE status IN ('QUEUED', 'FAILED') ORDER BY createdAt ASC")
    suspend fun getQueuedAndFailedJobs(): List<PrintJobEntity>
    
    @Query("DELETE FROM print_jobs WHERE createdAt < :timestamp")
    suspend fun clearOldJobs(timestamp: Long)

    @Query("DELETE FROM print_jobs")
    suspend fun clearAll()
}
