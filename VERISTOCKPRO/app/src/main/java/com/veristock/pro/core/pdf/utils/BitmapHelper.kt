package com.veristock.pro.core.pdf.utils

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import java.io.File
import kotlin.math.min

object BitmapHelper {

    /**
     * Loads a bitmap from a file and scales it to fit within a max width and height,
     * while maintaining the original aspect ratio.
     */
    fun getScaledBitmap(file: File, maxWidth: Int, maxHeight: Int): Bitmap? {
        if (!file.exists()) return null

        return try {
            val options = BitmapFactory.Options().apply {
                inJustDecodeBounds = true
            }
            BitmapFactory.decodeFile(file.absolutePath, options)

            val srcWidth = options.outWidth
            val srcHeight = options.outHeight

            val scaleFactor = min(
                if (srcWidth > 0) maxWidth.toFloat() / srcWidth else 1.0f,
                if (srcHeight > 0) maxHeight.toFloat() / srcHeight else 1.0f
            )

            val finalWidth = (srcWidth * scaleFactor).toInt()
            val finalHeight = (srcHeight * scaleFactor).toInt()

            val decodeOptions = BitmapFactory.Options().apply {
                // Calculate inSampleSize for efficiency
                inSampleSize = calculateInSampleSize(options, finalWidth, finalHeight)
            }
            
            val bitmap = BitmapFactory.decodeFile(file.absolutePath, decodeOptions)
            Bitmap.createScaledBitmap(bitmap, finalWidth, finalHeight, true)
        } catch (e: Exception) {
            // Log the exception
            null
        }
    }

    private fun calculateInSampleSize(options: BitmapFactory.Options, reqWidth: Int, reqHeight: Int): Int {
        val (height: Int, width: Int) = options.run { outHeight to outWidth }
        var inSampleSize = 1

        if (height > reqHeight || width > reqWidth) {
            val halfHeight: Int = height / 2
            val halfWidth: Int = width / 2
            while (halfHeight / inSampleSize >= reqHeight && halfWidth / inSampleSize >= reqWidth) {
                inSampleSize *= 2
            }
        }
        return inSampleSize
    }
}
