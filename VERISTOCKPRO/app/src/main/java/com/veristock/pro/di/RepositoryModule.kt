package com.veristock.pro.di

import com.veristock.pro.data.repository.PreferencesRepository
import com.veristock.pro.data.repository.ReportsRepository
import com.veristock.pro.data.repository.ReportsRepositoryImpl
import com.veristock.pro.data.repository.impl.DefaultPreferencesRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindReportsRepository(impl: ReportsRepositoryImpl): ReportsRepository

    @Binds
    @Singleton
    abstract fun bindPreferencesRepository(impl: DefaultPreferencesRepository): PreferencesRepository
}
