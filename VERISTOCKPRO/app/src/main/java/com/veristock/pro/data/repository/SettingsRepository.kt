package com.veristock.pro.data.repository

import com.veristock.pro.data.dao.AppSettingDao
import com.veristock.pro.data.entity.AppSettingEntity
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SettingsRepository @Inject constructor(
    private val appSettingDao: AppSettingDao
) {

    suspend fun getSetting(key: String): String? {
        return appSettingDao.getSetting(key)?.settingValue
    }

    suspend fun getSettingAsBoolean(key: String, default: Boolean = false): Boolean {
        val value = getSetting(key) ?: return default
        return value == "1" || value.equals("true", ignoreCase = true)
    }

    suspend fun getSettingAsInt(key: String, default: Int = 0): Int {
        val value = getSetting(key) ?: return default
        return value.toIntOrNull() ?: default
    }

    suspend fun getSettingAsDouble(key: String, default: Double = 0.0): Double {
        val value = getSetting(key) ?: return default
        return value.toDoubleOrNull() ?: default
    }

    suspend fun saveSetting(key: String, value: String, type: String = "STRING", description: String? = null) {
        val setting = AppSettingEntity(
            settingKey = key,
            settingValue = value,
            settingType = type,
            description = description,
            updatedAt = System.currentTimeMillis()
        )
        appSettingDao.setSetting(setting) // Fixed: changed from upsert to setSetting based on DAO
    }

    suspend fun saveBoolean(key: String, value: Boolean) {
        saveSetting(key, if (value) "1" else "0", "BOOLEAN")
    }

    suspend fun saveInt(key: String, value: Int) {
        saveSetting(key, value.toString(), "INTEGER")
    }

    suspend fun saveDouble(key: String, value: Double) {
        saveSetting(key, value.toString(), "DECIMAL")
    }

    // Specific settings
    suspend fun isAppSetupComplete(): Boolean {
        return getSettingAsBoolean("app_setup_complete", false)
    }

    suspend fun setAppSetupComplete(complete: Boolean) {
        saveBoolean("app_setup_complete", complete)
    }

    suspend fun getDefaultGSTRate(): Double {
        return getSettingAsDouble("default_gst_rate", 18.0)
    }

    suspend fun isSameStateBilling(): Boolean {
        return getSettingAsBoolean("same_state_billing", true)
    }
}