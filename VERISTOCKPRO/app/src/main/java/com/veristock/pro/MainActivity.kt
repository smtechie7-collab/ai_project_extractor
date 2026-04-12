package com.veristock.pro

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.veristock.pro.core.session.BusinessSession
import com.veristock.pro.ui.navigation.AppNavigation
import com.veristock.pro.ui.theme.VeriStockProTheme
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject
    lateinit var businessSession: BusinessSession

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            VeriStockProTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    // Reactive state: If profile is updated, this triggers navigation logic
                    val isSetupComplete by businessSession.isSetupComplete.collectAsState()

                    // Determine start destination
                    val startDestination = if (isSetupComplete) "home" else "setup"

                    AppNavigation(
                        startDestination = startDestination
                    )
                }
            }
        }
    }
}