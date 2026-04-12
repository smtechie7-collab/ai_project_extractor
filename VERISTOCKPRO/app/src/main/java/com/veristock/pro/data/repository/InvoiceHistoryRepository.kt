package com.veristock.pro.data.repository

import com.veristock.pro.data.dao.InvoicePdfMetadataDao
import com.veristock.pro.data.entity.InvoicePdfMetadataEntity
import com.veristock.pro.domain.model.InvoicePdfMetadata
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class InvoiceHistoryRepository @Inject constructor(
    private val metadataDao: InvoicePdfMetadataDao
) {

    suspend fun saveMetadata(metadata: InvoicePdfMetadata): Result<Unit> {
        return try {
            val entity = metadata.toEntity()
            metadataDao.insert(entity)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    fun getHistoryForSale(saleId: Long): Flow<List<InvoicePdfMetadata>> {
        return metadataDao.getHistoryForSale(saleId).map {
            it.map { entity -> entity.toDomainModel() }
        }
    }
}

private fun InvoicePdfMetadata.toEntity(): InvoicePdfMetadataEntity {
    return InvoicePdfMetadataEntity(
        id = id,
        saleId = saleId,
        generatedAt = generatedAt,
        templateType = templateType,
        paperSize = paperSize,
        copyTypes = copyTypes,
        fileSize = fileSize,
        filePath = filePath,
        regenerationCount = regenerationCount
    )
}

private fun InvoicePdfMetadataEntity.toDomainModel(): InvoicePdfMetadata {
    return InvoicePdfMetadata(
        id = id,
        saleId = saleId,
        generatedAt = generatedAt,
        templateType = templateType,
        paperSize = paperSize,
        copyTypes = copyTypes,
        fileSize = fileSize,
        filePath = filePath,
        regenerationCount = regenerationCount
    )
}
