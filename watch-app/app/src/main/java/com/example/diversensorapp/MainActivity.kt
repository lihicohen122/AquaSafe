package com.example.diversensorapp

import android.Manifest
import android.app.Activity
import android.content.pm.PackageManager
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import kotlinx.coroutines.*
import kotlin.math.sin

class MainActivity : Activity(), SensorEventListener {

    // --- הגדרות פרוטוקול התקשורת האקוסטי ---
    // !!! חייב להיות זהה לחלוטין לקוד בשרת הפייתון !!!
    private val charToFreq = mapOf(
        '0' to 10000.0, '1' to 10500.0, '2' to 11000.0, '3' to 11500.0, '4' to 12000.0,
        '5' to 12500.0, '6' to 13000.0, '7' to 13500.0, '8' to 14000.0, '9' to 14500.0,
        'a' to 15000.0, 'b' to 15500.0, 'c' to 16000.0, 'd' to 16500.0, 'e' to 17000.0,
        'f' to 17500.0, 'g' to 18000.0, 'h' to 18500.0, 'i' to 19000.0, 'j' to 19500.0,
        'k' to 20000.0, 'l' to 5000.0,  'm' to 5500.0,  'n' to 6000.0,  'o' to 6500.0,
        'p' to 7000.0,  'q' to 7500.0,  'r' to 8000.0,  's' to 8500.0,  't' to 9000.0,
        'u' to 9500.0,  'v' to 4000.0,  'w' to 4500.0,  'x' to 2500.0,  'y' to 3000.0,
        'z' to 3500.0,  '-' to 20500.0, ',' to 21000.0
    )
    private val startFreq = 21500.0
    private val endFreq = 22000.0
    private val sampleRate = 44100
    private val chunkDuration = 0.1 // משך ניגון כל תו (בשניות)

    // משתני מערכת וחיישנים
    private lateinit var sensorManager: SensorManager
    private var heartRateSensor: Sensor? = null
    private val scope = CoroutineScope(Dispatchers.Main + Job())
    private var isTransmitting = false

    // רכיבי ממשק משתמש
    private lateinit var statusTextView: TextView
    private lateinit var heartRateTextView: TextView
    private lateinit var transmitButton: Button
    private lateinit var diverIdEditText: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setupUI() // בניית הממשק

        if (checkSelfPermission(Manifest.permission.BODY_SENSORS) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.BODY_SENSORS), 101)
        }

        setupSensors()

        transmitButton.setOnClickListener {
            // הכפתור משמש רק להדגמה - שליחת נתון בודד
            val diverId = diverIdEditText.text.toString()
            val bpmText = heartRateTextView.text.toString().filter { it.isDigit() }

            if (diverId.isBlank()) {
                Toast.makeText(this, "Please enter Diver ID", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            if (bpmText.isBlank()) {
                Toast.makeText(this, "Waiting for BPM data", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val message = "$diverId,$bpmText"
            transmitMessage(message)
        }
    }

    private fun setupUI() {
        statusTextView = TextView(this).apply { text = "Status: Idle"; textSize = 16f }
        heartRateTextView = TextView(this).apply { text = "Heart Rate: --"; textSize = 20f }
        diverIdEditText = EditText(this).apply { hint = "Enter Diver ID here" }
        transmitButton = Button(this).apply { text = "Transmit Once" }

        // שימוש ב-LinearLayout כדי לסדר את הרכיבים אחד מתחת לשני
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(16, 16, 16, 16)
            addView(diverIdEditText)
            addView(transmitButton)
            addView(statusTextView)
            addView(heartRateTextView)
        }
        setContentView(layout)
    }

    private fun setupSensors() {
        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        heartRateSensor = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE)
        if (heartRateSensor == null) {
            heartRateTextView.text = "Heart rate sensor not available."
        }
    }

    /**
     * הפונקציה המרכזית: מקבלת הודעה ומנגנת אותה כרצף צלילים.
     */
    private fun transmitMessage(message: String) {
        if (isTransmitting) {
            Toast.makeText(this, "Already transmitting...", Toast.LENGTH_SHORT).show()
            return
        }

        // השידור חייב לרוץ ב-coroutine (בדומה ל-thread) כדי לא לתקוע את האפליקציה
        scope.launch(Dispatchers.Default) {
            isTransmitting = true
            runOnUiThread {
                statusTextView.text = "Status: Transmitting..."
                transmitButton.isEnabled = false
            }

            val audioTrack = createAudioTrack()
            audioTrack.play()

            // 1. נגן צליל התחלה
            playTone(audioTrack, startFreq, chunkDuration)
            delay((chunkDuration * 1000).toLong())

            // 2. נגן את ההודעה תו אחרי תו
            message.forEach { char ->
                charToFreq[char]?.let { freq ->
                    playTone(audioTrack, freq, chunkDuration)
                    // השהייה קטנה בין כל תו כדי לאפשר לשרת להבדיל ביניהם
                    delay((chunkDuration * 1000).toLong())
                }
            }

            // 3. נגן צליל סיום
            playTone(audioTrack, endFreq, chunkDuration)
            delay((chunkDuration * 1000).toLong())

            audioTrack.stop()
            audioTrack.release()

            isTransmitting = false
            runOnUiThread {
                statusTextView.text = "Status: Idle"
                transmitButton.isEnabled = true
            }
        }
    }

    /**
     * יוצר אובייקט AudioTrack מוכן לניגון.
     */
    private fun createAudioTrack(): AudioTrack {
        val bufferSize = (sampleRate * chunkDuration).toInt()
        return AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(sampleRate)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .build()
            )
            .setBufferSizeInBytes(bufferSize * 2) // *2 for 16-bit
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()
    }

    /**
     * מייצר ומנגן צליל טהור (גל סינוס) בתדר ובאורך הנתונים.
     */
    private fun playTone(audioTrack: AudioTrack, frequency: Double, duration: Double) {
        val numSamples = (duration * sampleRate).toInt()
        val buffer = ShortArray(numSamples)

        for (i in 0 until numSamples) {
            val angle = 2.0 * Math.PI * i / (sampleRate / frequency)
            buffer[i] = (sin(angle) * Short.MAX_VALUE).toInt().toShort()
        }

        try {
            audioTrack.write(buffer, 0, buffer.size)
        } catch (e: Exception) {
            Log.e("AudioTrack", "Error writing to audio track", e)
        }
    }

    // --- מחזור החיים של האפליקציה וחיישן הדופק ---

    override fun onResume() {
        super.onResume()
        if (checkSelfPermission(Manifest.permission.BODY_SENSORS) == PackageManager.PERMISSION_GRANTED) {
            sensorManager.registerListener(this, heartRateSensor, SensorManager.SENSOR_DELAY_NORMAL)
        }
    }

    override fun onPause() {
        super.onPause()
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (event?.sensor?.type == Sensor.TYPE_HEART_RATE) {
            val heartRate = event.values[0]
            if (heartRate > 0) {
                // רק מעדכנים את הטקסט. השידור עצמו יתבצע בלחיצת כפתור
                heartRateTextView.text = "Heart Rate: ${heartRate.toInt()} bpm"
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 101) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permission granted!", Toast.LENGTH_SHORT).show()
                sensorManager.registerListener(this, heartRateSensor, SensorManager.SENSOR_DELAY_NORMAL)
            } else {
                Toast.makeText(this, "Body sensor permission is required.", Toast.LENGTH_LONG).show()
            }
        }
    }
}