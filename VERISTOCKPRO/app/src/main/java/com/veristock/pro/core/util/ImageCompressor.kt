package com.veristock.pro.core.util

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import androidx.core.graphics.scale
import java.io.File
import java.io.FileOutputStream
import kotlin.math.min

object ImageCompressor {

    fun compressLogo(context: Context, imageUri: Uri, quality: Int = 85, maxSize: Int = 200): File? {
        return try {
            val inputStream = context.contentResolver.openInputStream(imageUri) ?: return null
            val originalBitmap = BitmapFactory.decodeStream(inputStream)
            inputStream.close()

            // Resize if too large
            val scaledBitmap = if (originalBitmap.width > maxSize || originalBitmap.height > maxSize) {
                val ratio = min(maxSize.toFloat() / originalBitmap.width, maxSize.toFloat() / originalBitmap.height)
                originalBitmap.scale((originalBitmap.width * ratio).toInt(), (originalBitmap.height * ratio).toInt())
            } else {
                originalBitmap
            }

            // Create a file in the app's cache directory
            val outputFile = File(context.cacheDir, "logo_compressed.jpg")
            FileOutputStream(outputFile).use { out ->
                scaledBitmap.compress(Bitmap.CompressFormat.JPEG, quality, out)
            }

            // Recycle bitmaps to free up memory
            originalBitmap.recycle()
            if (scaledBitmap != originalBitmap) {
                scaledBitmap.recycle()
            }

            outputFile
        } catch (e: Exception) {
            // Log the error in a real app
            null
        }
    }
}
