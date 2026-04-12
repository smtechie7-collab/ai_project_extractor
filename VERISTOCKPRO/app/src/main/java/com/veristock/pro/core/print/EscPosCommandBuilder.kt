
package com.veristock.pro.core.print

import android.graphics.Bitmap
import java.io.ByteArrayOutputStream

/**
 * A builder class for creating ESC/POS command byte arrays for thermal printers.
 *
 * This class provides a fluent API to construct a sequence of commands for text formatting,
 * alignment, graphics, and printer control.
 *
 * Reference: Most commands are based on the Epson ESC/POS standard command set.
 */
class EscPosCommandBuilder {

    private val outputStream = ByteArrayOutputStream()

    // Command constants
    companion object {
        // ASCII control characters
        const val HT: Byte = 0x09
        const val LF: Byte = 0x0A
        const val FF: Byte = 0x0C
        const val CR: Byte = 0x0D
        const val EOT: Byte = 0x04
        const val DLE: Byte = 0x10
        const val CAN: Byte = 0x18

        // ESC (Escape) commands
        const val ESC: Byte = 0x1B
        // GS (Group Separator) commands
        const val GS: Byte = 0x1D
    }

    enum class Alignment(val value: Byte) {
        LEFT(0),
        CENTER(1),
        RIGHT(2)
    }

    enum class FontSize(val value: Byte) {
        NORMAL(0), // 1x height, 1x width
        DOUBLE_HEIGHT(16), // 2x height
        DOUBLE_WIDTH(32), // 2x width
        QUADRUPLE(48) // 2x height, 2x width
    }

    enum class BarcodeType(val value: Byte) {
        UPC_A(0),
        UPC_E(1),
        EAN13(2),
        EAN8(3),
        CODE39(4),
        ITF(5),
        CODABAR(6),
        CODE93(72),
        CODE128(73)
    }

    init {
        initialize()
    }

    /**
     * Initializes the printer.
     * Clears print buffer, resets formatting to default.
     * Should be called at the start of every print job.
     */
    fun initialize(): EscPosCommandBuilder {
        outputStream.write(byteArrayOf(ESC, '@'.code.toByte()))
        return this
    }

    /**
     * Resets all formatting to printer defaults.
     */
    fun reset(): EscPosCommandBuilder {
        setBold(false)
        setUnderline(false)
        setFontSize(FontSize.NORMAL)
        setAlignment(Alignment.LEFT)
        return this
    }

    /**
     * Prints text without a new line at the end.
     *
     * @param text The text to print.
     */
    fun printText(text: String): EscPosCommandBuilder {
        // TODO: Add support for different character encodings
        outputStream.write(text.toByteArray(Charsets.UTF_8))
        return this
    }

    /**
     * Prints text followed by a new line character (LF).
     *
     * @param text The text to print on a line.
     */
    fun printLine(text: String): EscPosCommandBuilder {
        printText(text)
        feedLine()
        return this
    }
    
    fun printTextCentered(text: String): EscPosCommandBuilder {
        setAlignment(Alignment.CENTER)
        printLine(text)
        setAlignment(Alignment.LEFT)
        return this
    }

    /**
     * Feeds one line.
     */
    fun feedLine(): EscPosCommandBuilder {
        outputStream.write(byteArrayOf(LF))
        return this
    }

    /**
     * Feeds a specified number of lines.
     *
     * @param count The number of lines to feed.
     */
    fun feedLines(count: Int): EscPosCommandBuilder {
        if (count > 0) {
            outputStream.write(byteArrayOf(ESC, 'd'.code.toByte(), count.toByte()))
        }
        return this
    }

    /**
     * Sets the text alignment.
     *
     * @param align The desired alignment.
     */
    fun setAlignment(align: Alignment): EscPosCommandBuilder {
        outputStream.write(byteArrayOf(ESC, 'a'.code.toByte(), align.value))
        return this
    }

    /**
     * Enables or disables bold text mode.
     *
     * @param enabled True to enable bold, false to disable.
     */
    fun setBold(enabled: Boolean): EscPosCommandBuilder {
        outputStream.write(byteArrayOf(ESC, 'E'.code.toByte(), if (enabled) 1 else 0))
        return this
    }

    /**
     * Enables or disables underline mode.
     *
     * @param enabled True to enable underline, false to disable. 0 for off, 1 for 1-dot, 2 for 2-dot
     */
    fun setUnderline(enabled: Boolean): EscPosCommandBuilder {
        outputStream.write(byteArrayOf(ESC, '-'.code.toByte(), if (enabled) 1 else 0))
        return this
    }

    /**
     * Sets the font size (height and width).
     *
     * @param size The desired font size.
     */
    fun setFontSize(size: FontSize): EscPosCommandBuilder {
        outputStream.write(byteArrayOf(GS, '!'.code.toByte(), size.value))
        return this
    }
    
    /**
     * Prints a separator line of a given character.
     * @param char The character to use for the line.
     * @param length The number of characters in the line.
     */
    fun printSeparatorLine(length: Int, char: Char = '-'): EscPosCommandBuilder {
        printLine(char.toString().repeat(length))
        return this
    }


    /**
     * Performs a full or partial paper cut.
     * Most thermal printers perform a partial cut to prevent the receipt from falling.
     */
    fun cutPaper(): EscPosCommandBuilder {
        // GS V 1 - Feeds paper and cuts
        outputStream.write(byteArrayOf(GS, 'V'.code.toByte(), 1))
        return this
    }

    /**
     * Builds the final byte array to be sent to the printer.
     *
     * @return A ByteArray containing all the commands and data.
     */
    fun build(): ByteArray {
        return outputStream.toByteArray()
    }
}
