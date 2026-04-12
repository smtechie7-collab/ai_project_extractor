
package com.veristock.pro.core.print.model

import android.bluetooth.BluetoothDevice

/**
 * Represents the current state of the connection to a Bluetooth printer.
 */
enum class BluetoothPrinterState {
    DISCONNECTED,       // No connection
    CONNECTING,         // Attempting to connect
    CONNECTED,          // Successfully connected
    PRINTING,           // Currently sending data
    ERROR,              // A connection or printing error occurred
    RECONNECTING        // Attempting to auto-reconnect
}

/**
 * Represents the status of a single print job in the queue.
 */
enum class PrintJobStatus {
    QUEUED,      // Waiting to print
    PREPARING,   // Formatting data into ESC/POS commands
    PRINTING,    // Sending to printer
    SUCCESS,     // Printed successfully
    FAILED,      // Print failed after retries
    CANCELLED    // User cancelled the job
}

/**
 * Defines the type of content for a print job.
 */
enum class PrintJobType {
    INVOICE,
    RECEIPT,
    REPORT,
    TEST_PAGE
}

/**
 * Defines the standard thermal paper widths and their character counts.
 */
enum class PaperWidth(val charsPerLine: Int) {
    MM_58(32),   // 32 characters for standard font
    MM_80(48)    // 48 characters for standard font
}

/**
 * Data class representing a single print job.
 *
 * @param id Unique identifier for the job.
 * @param type The type of content to be printed.
 * @param data The actual data to be formatted and printed (e.g., an Invoice object).
 * @param printerAddress The MAC address of the target printer.
 * @param status The current lifecycle status of the job.
 * @param createdAt Timestamp of when the job was created.
 * @param attempts Number of times this job has been attempted.
 * @param lastError The last error message if the job failed.
 */
data class PrintJob(
    val id: String,
    val type: PrintJobType,
    val data: Any, // This will be your specific Invoice/Sale object
    val printerAddress: String,
    var status: PrintJobStatus,
    val createdAt: Long = System.currentTimeMillis(),
    var attempts: Int = 0,
    var lastError: String? = null
)

/**
 * Data class for storing global printer settings.
 * This will be saved to and retrieved from DataStore.
 */
data class PrinterSettings(
    val defaultPrinterAddress: String? = null,
    val defaultPrinterName: String? = null,
    val paperWidth: PaperWidth = PaperWidth.MM_58,
    val autoPrint: Boolean = false,
    val printCopies: Int = 1,
    val autoReconnect: Boolean = true,
    val connectionTimeout: Int = 10, // in seconds
    val maxRetries: Int = 3,
    val footerMessage: String = "Thank you! Visit again"
)

/**
 * Represents a saved printer profile, allowing for multiple printer configurations.
 *
 * @param id A unique ID for the profile.
 * @param name A user-friendly name for the printer (e.g., "Counter 1 Printer").
 * @param deviceAddress The MAC address of the Bluetooth device.
 * @param deviceName The broadcast name of the Bluetooth device.
 * @param paperWidth The paper size for this specific printer.
 * @param isDefault Whether this is the default printer for the app.
 */
data class PrinterProfile(
    val id: String,
    val name: String,
    val deviceAddress: String,
    val deviceName: String,
    val paperWidth: PaperWidth,
    val isDefault: Boolean = false
)
