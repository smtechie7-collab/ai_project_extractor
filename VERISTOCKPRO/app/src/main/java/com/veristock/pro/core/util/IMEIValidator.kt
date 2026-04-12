package com.veristock.pro.core.util

object IMEIValidator {
    fun validate(imei: String): ValidationResult {
        if (imei.isBlank()) {
            return ValidationResult.Error("IMEI cannot be empty")
        }

        if (imei.length != 15) {
            return ValidationResult.Error("IMEI must be 15 digits")
        }

        if (!imei.all { it.isDigit() }) {
            return ValidationResult.Error("IMEI must contain only digits")
        }

        if (!luhnCheck(imei)) {
            return ValidationResult.Error("Invalid IMEI checksum")
        }

        return ValidationResult.Success
    }

    private fun luhnCheck(number: String): Boolean {
        val digits = number.map { it.toString().toInt() }
        val sum = digits.reversed().mapIndexed { index, digit ->
            if (index % 2 == 1) {
                val doubled = digit * 2
                if (doubled > 9) doubled - 9 else doubled
            } else {
                digit
            }
        }.sum()
        return sum % 10 == 0
    }
}

sealed class ValidationResult {
    object Success : ValidationResult()
    data class Error(val message: String) : ValidationResult()
}