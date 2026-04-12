
package com.veristock.pro.core.database

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.veristock.pro.data.dao.*
import com.veristock.pro.data.entity.*

@Database(
    entities = [
        BusinessProfileEntity::class,
        ProductEntity::class,
        CustomerEntity::class,
        SaleEntity::class,
        SaleItemEntity::class,
        ImeiInventoryEntity::class,
        StockMovementEntity::class,
        AppSettingEntity::class,
        InvoiceSequenceEntity::class,
        InvoicePdfMetadataEntity::class,
        // New entities for printing feature
        PrintJobEntity::class,
        PrinterProfileEntity::class
    ],
    version = 3, // Incremented version because of schema change
    exportSchema = true
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {

    abstract fun businessProfileDao(): BusinessProfileDao
    abstract fun productDao(): ProductDao
    abstract fun customerDao(): CustomerDao
    abstract fun saleDao(): SaleDao
    abstract fun saleItemDao(): SaleItemDao
    abstract fun imeiInventoryDao(): ImeiInventoryDao
    abstract fun stockMovementDao(): StockMovementDao
    abstract fun appSettingDao(): AppSettingDao
    abstract fun invoicePdfMetadataDao(): InvoicePdfMetadataDao
    abstract fun reportsDao(): ReportsDao

    // New DAOs for printing feature
    abstract fun printJobDao(): PrintJobDao
    abstract fun printerProfileDao(): PrinterProfileDao
    
    // abstract fun invoiceSequenceDao(): InvoiceSequenceDao // InvoiceSequence logic handled manually or via simple queries for now
}
