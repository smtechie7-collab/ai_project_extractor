package com.veristock.pro.feature.reports.components

import android.graphics.Color
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet

@Composable
fun SalesLineChart(
    data: List<Pair<Float, Float>>,
    modifier: Modifier = Modifier
) {
    AndroidView(
        modifier = modifier,
        factory = { context ->
            LineChart(context).apply {
                // Basic chart setup
                description.isEnabled = false
                setDrawGridBackground(false)
                xAxis.setDrawGridLines(false)
                axisLeft.setDrawGridLines(true)
                axisRight.isEnabled = false
            }
        },
        update = { chart ->
            val entries = data.map { Entry(it.first, it.second) }
            val dataSet = LineDataSet(entries, "Sales Data").apply {
                // Line styling
                lineWidth = 2.5f
                setCircleColor(Color.BLUE)
                color = Color.BLUE
            }
            chart.data = LineData(dataSet)
            chart.invalidate() // Refresh the chart
        }
    )
}
