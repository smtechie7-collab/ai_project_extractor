package com.veristock.pro.di

import android.content.Context
import android.content.SharedPreferences
import androidx.work.WorkManager
import com.google.gson.Gson
import com.veristock.pro.core.email.EmailManager
import com.veristock.pro.core.pdf.InvoicePdfGenerator
import com.veristock.pro.core.util.InvoiceNumberGenerator
import com.veristock.pro.data.dao.BusinessProfileDao
import com.veristock.pro.data.repository.InvoiceHistoryRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideInvoiceNumberGenerator(
        businessProfileDao: BusinessProfileDao
    ): InvoiceNumberGenerator {
        return InvoiceNumberGenerator(businessProfileDao)
    }

    @Provides
    @Singleton
    fun provideInvoicePdfGenerator(
        @ApplicationContext context: Context,
        historyRepository: InvoiceHistoryRepository
    ): InvoicePdfGenerator {
        return InvoicePdfGenerator(context, historyRepository)
    }

    @Provides
    @Singleton
    fun provideEmailManager(
        @ApplicationContext context: Context
    ): EmailManager {
        return EmailManager(context)
    }

    @Provides
    @Singleton
    fun provideWorkManager(
        @ApplicationContext context: Context
    ): WorkManager {
        return WorkManager.getInstance(context)
    }

    @Provides
    @Singleton
    fun provideSharedPreferences(@ApplicationContext context: Context): SharedPreferences {
        return context.getSharedPreferences("veristock_prefs", Context.MODE_PRIVATE)
    }

    @Provides
    @Singleton
    fun provideGson(): Gson {
        return Gson()
    }
}
