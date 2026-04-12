package com.veristock.pro.data.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Key-value store for app configuration.
 */
@Entity(tableName = "app_settings")
data class AppSettingEntity(
    @PrimaryKey
    @ColumnInfo(name = "setting_key")
    val settingKey: String,

    @ColumnInfo(name = "setting_value")
    val settingValue: String?,

    @ColumnInfo(name = "setting_type", defaultValue = "STRING")
    val settingType: String = "STRING", // STRING, INTEGER, BOOLEAN, JSON

    val description: String?,

    @ColumnInfo(name = "updated_at")
    val updatedAt: Long
)