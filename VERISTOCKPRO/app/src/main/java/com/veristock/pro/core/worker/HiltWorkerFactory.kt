package com.veristock.pro.core.worker

import android.content.Context
import androidx.hilt.work.HiltWorkerFactory
import androidx.work.ListenableWorker
import androidx.work.WorkerFactory
import androidx.work.WorkerParameters
import javax.inject.Inject

class VeriStockWorkerFactory @Inject constructor(
    private val workerFactory: HiltWorkerFactory
) : WorkerFactory() {
    override fun createWorker(
        appContext: Context,
        workerClassName: String,
        workerParameters: WorkerParameters
    ): ListenableWorker? {
        return workerFactory.createWorker(appContext, workerClassName, workerParameters)
    }
}