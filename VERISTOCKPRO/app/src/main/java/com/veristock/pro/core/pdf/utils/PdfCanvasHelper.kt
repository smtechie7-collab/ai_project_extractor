package com.veristock.pro.core.pdf.utils

import android.graphics.Canvas
import android.graphics.DashPathEffect
import android.graphics.Paint
import android.graphics.RectF
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint

object PdfCanvasHelper {

    fun drawTextCentered(canvas: Canvas, text: String, x: Float, y: Float, paint: TextPaint) {
        val textWidth = paint.measureText(text)
        canvas.drawText(text, x - textWidth / 2, y, paint)
    }

    fun drawTextRight(canvas: Canvas, text: String, x: Float, y: Float, paint: TextPaint) {
        val textWidth = paint.measureText(text)
        canvas.drawText(text, x - textWidth, y, paint)
    }

    fun drawHorizontalLine(canvas: Canvas, startX: Float, endX: Float, y: Float, paint: Paint) {
        canvas.drawLine(startX, y, endX, y, paint)
    }

    fun drawDashedLine(canvas: Canvas, startX: Float, endX: Float, y: Float, paint: Paint) {
        val originalPathEffect = paint.pathEffect
        paint.pathEffect = DashPathEffect(floatArrayOf(10f, 5f), 0f)
        canvas.drawLine(startX, y, endX, y, paint)
        paint.pathEffect = originalPathEffect // Reset
    }

    fun drawRectWithBorder(canvas: Canvas, rect: RectF, fillPaint: Paint?, strokePaint: Paint) {
        if (fillPaint != null) {
            canvas.drawRect(rect, fillPaint)
        }
        canvas.drawRect(rect, strokePaint)
    }
    
    fun drawMultilineText(canvas: Canvas, text: String, x: Float, y: Float, width: Int, paint: TextPaint, alignment: Layout.Alignment) {
        val staticLayout = StaticLayout.Builder
            .obtain(text, 0, text.length, paint, width)
            .setAlignment(alignment)
            .build()
        
        canvas.save()
        canvas.translate(x, y)
        staticLayout.draw(canvas)
        canvas.restore()
    }
}
