package com.veristock.pro.core.pdf.utils

import android.graphics.Paint
import android.graphics.Rect

object TextMeasurement {

    /**
     * Calculates the width of a given text string using a specific Paint object.
     */
    fun getTextWidth(text: String, paint: Paint): Float {
        return paint.measureText(text)
    }

    /**
     * Calculates the height of a given text string using a specific Paint object.
     */
    fun getTextHeight(text: String, paint: Paint): Float {
        val bounds = Rect()
        paint.getTextBounds(text, 0, text.length, bounds)
        return bounds.height().toFloat()
    }

    /**
     * Calculates the bounds of a given text string.
     */
    fun getTextBounds(text: String, paint: Paint): Rect {
        val bounds = Rect()
        paint.getTextBounds(text, 0, text.length, bounds)
        return bounds
    }
}
