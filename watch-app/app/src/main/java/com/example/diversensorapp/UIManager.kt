package com.example.diversensorapp

import android.content.Context
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView

class UIManager(context: Context) {
    val statusTextView: TextView = TextView(context).apply {
        text = "Status: Idle"
        textSize = 10f
        textAlignment = TextView.TEXT_ALIGNMENT_CENTER
    }
    val heartRateTextView: TextView = TextView(context).apply {
        text = "Heart Rate: --"
        textSize = 12f
        textAlignment = TextView.TEXT_ALIGNMENT_CENTER
    }
    val diverIdEditText: EditText = EditText(context).apply {
        hint = "Enter Diver ID here"
        textSize = 12f
        setPadding(0, 8, 0, 8)
    }
    val transmitButton: Button = Button(context).apply {
        text = "Start Transmission"
        textSize = 12f
    }
    val layout: LinearLayout = LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL
        setPadding(8, 16, 8, 8)
        layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.MATCH_PARENT
        )
        gravity = android.view.Gravity.CENTER
        addView(diverIdEditText, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { setMargins(0, 0, 0, 8) })
        addView(transmitButton, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { setMargins(0, 0, 0, 8) })
        addView(statusTextView, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { setMargins(0, 0, 0, 8) })
        addView(heartRateTextView, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ))
    }

    fun setStatus(text: String) {
        statusTextView.text = text
    }

    fun setHeartRate(text: String) {
        heartRateTextView.text = text
    }
}

