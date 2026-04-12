
package com.veristock.pro.di

import android.content.Context
import androidx.room.Room
import com.veristock.pro.core.database.AppDatabase
import com.veristock.pro.data.dao.*
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "veristock_pro.db"
        ).fallbackToDestructiveMigration().build()
    }

    @Provides
    fun provideBusinessProfileDao(db: AppDatabase): BusinessProfileDao = db.businessProfileDao()

    @Provides
    fun provideProductDao(db: AppDatabase): ProductDao = db.productDao()

    @Provides
    fun provideCustomerDao(db: AppDatabase): CustomerDao = db.customerDao()

    @Provides
    fun provideSaleDao(db: AppDatabase): SaleDao = db.saleDao()

    @Provides
    fun provideSaleItemDao(db: AppDatabase): SaleItemDao = db.saleItemDao()

    @Provides
    fun provideImeiInventoryDao(db: AppDatabase): ImeiInventoryDao = db.imeiInventoryDao()

    @Provides
    fun provideStockMovementDao(db: AppDatabase): StockMovementDao = db.stockMovementDao()

    @Provides
    fun provideAppSettingDao(db: AppDatabase): AppSettingDao = db.appSettingDao()

    @Provides
    fun provideInvoicePdfMetadataDao(db: AppDatabase): InvoicePdfMetadataDao = db.invoicePdfMetadataDao()

    @Provides
    fun provideReportsDao(db: AppDatabase): ReportsDao = db.reportsDao()

    // Provides for new printing feature DAOs
    @Provides
    fun providePrintJobDao(db: AppDatabase): PrintJobDao = db.printJobDao()

    @Provides
    fun providePrinterProfileDao(db: AppDatabase): PrinterProfileDao = db.printerProfileDao()
}
