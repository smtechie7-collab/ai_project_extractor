
package com.veristock.pro.feature.customers

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.veristock.pro.domain.model.Customer

@Composable
fun QuickCustomerDialog(
    onDismiss: () -> Unit,
    onCreateCustomer: (
        name: String,
        mobile: String,
        (Customer) -> Unit,
        (String) -> Unit
    ) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var mobile by remember { mutableStateOf("") }
    var nameError by remember { mutableStateOf<String?>(null) }
    var mobileError by remember { mutableStateOf<String?>(null) }
    var submissionError by remember { mutableStateOf<String?>(null) }
    var isLoading by remember { mutableStateOf(false) }

    val keyboardController = LocalSoftwareKeyboardController.current
    val mobileFocusRequester = remember { FocusRequester() }

    fun validateName(input: String): Boolean {
        nameError = when {
            input.isBlank() -> "Name is required"
            input.length < 2 -> "Name must be at least 2 characters"
            input.length > 50 -> "Name cannot exceed 50 characters"
            else -> null
        }
        return nameError == null
    }

    fun validateMobile(input: String): Boolean {
        mobileError = when {
            input.isBlank() -> "Mobile is required"
            input.length != 10 -> "Mobile must be 10 digits"
            else -> null
        }
        return mobileError == null
    }

    val isFormValid = nameError == null && mobileError == null && name.isNotBlank() && mobile.isNotBlank()

    val submitAction = {
        if (validateName(name) && validateMobile(mobile)) {
            isLoading = true
            submissionError = null
            onCreateCustomer(name, mobile,
                { customer -> // onSuccess
                    isLoading = false
                    onDismiss()
                },
                { error -> // onError
                    isLoading = false
                    submissionError = error
                }
            )
        }
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add Quick Customer") },
        text = {
            Column {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it; validateName(it) },
                    label = { Text("Customer Name*") },
                    isError = nameError != null,
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                    keyboardActions = KeyboardActions(onNext = { mobileFocusRequester.requestFocus() })
                )
                nameError?.let { ErrorText(it) }

                Spacer(Modifier.height(16.dp))

                OutlinedTextField(
                    value = mobile,
                    onValueChange = {
                        if (it.length <= 10 && it.all { char -> char.isDigit() }) {
                            mobile = it
                            validateMobile(it)
                        }
                    },
                    label = { Text("Mobile Number*") },
                    isError = mobileError != null || submissionError != null,
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Number,
                        imeAction = ImeAction.Done
                    ),
                    keyboardActions = KeyboardActions(onDone = { if (isFormValid) submitAction() else keyboardController?.hide() }),
                    modifier = Modifier.focusRequester(mobileFocusRequester)
                )
                mobileError?.let { ErrorText(it) }
                submissionError?.let { ErrorText(it) }
            }
        },
        confirmButton = {
            Button(onClick = submitAction, enabled = isFormValid && !isLoading) {
                if (isLoading) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.dp)
                } else {
                    Text("Save")
                }
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
private fun ErrorText(text: String) {
    Text(text, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
}
