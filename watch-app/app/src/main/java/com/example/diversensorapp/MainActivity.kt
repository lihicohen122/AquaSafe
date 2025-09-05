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

    // --- Acoustic Communication Protocol Settings ---
    // !!! MUST BE IDENTICAL TO THE PYTHON SERVER CODE !!!
    private val charToFreq = mapOf( // NEW FREQUENCY MAP (V4) - No collisions, focused range
        '0' to 3000.0, '1' to 3200.0, '2' to 3400.0, '3' to 3600.0, '4' to 3800.0,
        '5' to 4000.0, '6' to 4200.0, '7' to 4400.0, '8' to 4600.0, '9' to 4800.0,
        'a' to 5000.0, 'b' to 5200.0, 'c' to 5400.0, 'd' to 5600.0, 'e' to 5800.0,
        'f' to 6000.0, 'g' to 6200.0, 'h' to 6400.0, 'i' to 6600.0, 'j' to 6800.0,
        'k' to 7000.0, 'l' to 7200.0, 'm' to 7400.0, 'n' to 7600.0, 'o' to 7800.0,
        'p' to 8000.0, 'q' to 8200.0, 'r' to 8400.0, 's' to 8600.0, 't' to 8800.0,
        'u' to 9000.0, 'v' to 9200.0, 'w' to 9400.0, 'x' to 9600.0, 'y' to 9800.0,
        'z' to 10000.0,  '-' to 2200.0, ',' to 2000.0 // Hyphen and Comma frequencies
    )
    private val startFreq = 1200.0
    private val endFreq = 11000.0 // *** NEW END FREQUENCY - MUST MATCH SERVER! ***
    private val sampleRate = 44100
    private val chunkDuration = 0.3 // *** ADJUSTED DURATION OF EACH TONE (in seconds) - MATCHES SERVER FFT WINDOW ***
    private val silentDuration = 0.5 // *** ADJUSTED SHORT SILENCE BETWEEN CHARACTERS - GREATER THAN SERVER DEBOUNCE ***

    // System and Sensor Variables
    private lateinit var sensorManager: SensorManager
    private var heartRateSensor: Sensor? = null
    private val scope = CoroutineScope(Dispatchers.Main + Job())
    private var isTransmitting = false
    private var transmissionJob: Job? = null // Job for periodic transmission

    // UI Elements
    private lateinit var statusTextView: TextView
    private lateinit var heartRateTextView: TextView
    private lateinit var transmitButton: Button
    private lateinit var diverIdEditText: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setupUI() // Build the UI

        // Request BODY_SENSORS permission for heart rate sensor
        if (checkSelfPermission(Manifest.permission.BODY_SENSORS) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.BODY_SENSORS), 101)
        }

        setupSensors() // Initialize sensors

        transmitButton.setOnClickListener {
            if (transmissionJob == null) {
                // Start periodic transmission
                val diverId = diverIdEditText.text.toString()
                val bpmText = heartRateTextView.text.toString().filter { it.isDigit() }

                // Basic validation
                if (diverId.isBlank()) {
                    Toast.makeText(this, "Please enter Diver ID", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                if (bpmText.isBlank()) {
                    Toast.makeText(this, "Waiting for BPM data", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                transmitButton.text = "Stop Transmission"
                statusTextView.text = "Status: Transmitting..."
                transmissionJob = scope.launch {
                    while (isActive) {
                        val currentBpm = heartRateTextView.text.toString().filter { it.isDigit() }
                        val message = "$diverId,$currentBpm"
                        transmitMessage(message)
                        delay(20_000) // 20 seconds
                    }
                }
            } else {
                // Stop periodic transmission
                transmissionJob?.cancel()
                transmissionJob = null
                transmitButton.text = "Start Transmission"
                statusTextView.text = "Status: Idle"
            }
        }
    }

    private fun setupUI() {
        // Initialize UI elements
        statusTextView = TextView(this).apply {
            text = "Status: Idle"
            textSize = 10f // Even smaller text
            textAlignment = TextView.TEXT_ALIGNMENT_CENTER // Center align
        }
        heartRateTextView = TextView(this).apply {
            text = "Heart Rate: --"
            textSize = 12f // Even smaller text
            textAlignment = TextView.TEXT_ALIGNMENT_CENTER // Center align
        }
        diverIdEditText = EditText(this).apply {
            hint = "Enter Diver ID here"
            textSize = 12f // Even smaller text
            setPadding(0, 8, 0, 8) // Minimal vertical padding
        }
        transmitButton = Button(this).apply {
            text = "Start Transmission"
            textSize = 12f // Even smaller text
        }

        // Use LinearLayout to arrange components vertically on the screen
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(8, 16, 8, 8) // Minimal padding
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT
            )
            gravity = android.view.Gravity.CENTER // Center all items
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
        setContentView(layout) // Set the layout as the content view
    }

    private fun setupSensors() {
        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        heartRateSensor = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE)
        if (heartRateSensor == null) {
            heartRateTextView.text = "Heart rate sensor not available."
        }
    }

    /**
     * Main function: receives a message string and plays it as a sequence of acoustic tones.
     * The sequence is: START tone -> Character tones -> END tone.
     */
    private fun transmitMessage(message: String) {
        if (isTransmitting) {
            Toast.makeText(this, "Already transmitting...", Toast.LENGTH_SHORT).show()
            return
        }

        // Transmission must run in a coroutine (similar to a background thread)
        // to avoid blocking the main UI thread and freezing the app.
        scope.launch(Dispatchers.Default) {
            isTransmitting = true
            runOnUiThread { // Update UI on the main thread
                statusTextView.text = "Status: Transmitting..."
                transmitButton.isEnabled = false
            }

            val audioTrack = createAudioTrack() // Create AudioTrack for playing tones
            audioTrack.play() // Start the audio playback stream

            // 1. Play START tone
            playTone(audioTrack, startFreq, chunkDuration)
            delay((chunkDuration * 1000).toLong()) // Wait for tone to finish
            delay((silentDuration * 1000).toLong()) // Wait for silence duration

            // 2. Play message character by character
            // This loop ensures characters are played in order, including the comma.
            message.forEach { char ->
                charToFreq[char]?.let { freq ->
                    playTone(audioTrack, freq, chunkDuration)
                    delay((chunkDuration * 1000).toLong()) // Wait for tone to finish
                    delay((silentDuration * 1000).toLong()) // Wait for silence duration
                } ?: run {
                    Log.w("AcousticComm", "Character '$char' not found in frequency map.")
                }
            }

            // 3. Play END tone - This must be the very last tone for the server to detect message end!
            // NOTE: With time-based server, the END tone is less critical for message termination,
            // but it's good practice to keep it for completeness and potential future use.
            playTone(audioTrack, endFreq, chunkDuration)
            delay((chunkDuration * 1000).toLong()) // Wait for tone to finish
            delay((silentDuration * 1000).toLong()) // Final silence after end tone

            // Stop and release AudioTrack resources
            audioTrack.stop()
            audioTrack.release()

            isTransmitting = false
            runOnUiThread { // Update UI on the main thread
                statusTextView.text = "Status: Idle"
                transmitButton.isEnabled = true
            }
        }
    }

    /**
     * Creates and configures an AudioTrack object for playing 16-bit mono PCM audio.
     */
    private fun createAudioTrack(): AudioTrack {
        val bufferSize = (sampleRate * chunkDuration).toInt() // Calculate buffer size based on tone duration
        return AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT) // 16-bit PCM format
                    .setSampleRate(sampleRate) // Set sample rate
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO) // Mono audio
                    .build()
            )
            .setBufferSizeInBytes(bufferSize * 2) // Buffer size in bytes (2 bytes per 16-bit sample)
            .setTransferMode(AudioTrack.MODE_STREAM) // Stream mode for continuous writing
            .build()
    }

    /**
     * Generates a pure sine wave tone and writes it to the AudioTrack for playback.
     *
     * @param audioTrack The AudioTrack instance to write audio data to.
     * @param frequency The frequency of the tone in Hz.
     * @param duration The duration of the tone in seconds.
     */
    private fun playTone(audioTrack: AudioTrack, frequency: Double, duration: Double) {
        val numSamples = (duration * sampleRate).toInt() // Calculate number of samples needed for the duration
        val buffer = ShortArray(numSamples) // Create a buffer to hold the audio samples

        // Generate sine wave samples
        for (i in 0 until numSamples) {
            val angle = 2.0 * Math.PI * i / (sampleRate / frequency)
            buffer[i] = (sin(angle) * Short.MAX_VALUE).toInt().toShort() // Scale to 16-bit PCM range
        }

        try {
            audioTrack.write(buffer, 0, buffer.size) // Write the generated samples to the audio track
        } catch (e: Exception) {
            Log.e("AudioTrack", "Error writing to audio track", e)
        }
    }

    // --- App Lifecycle and Heart Rate Sensor Callbacks ---

    override fun onResume() {
        super.onResume()
        // Register sensor listener when app is resumed, if permission is granted
        if (checkSelfPermission(Manifest.permission.BODY_SENSORS) == PackageManager.PERMISSION_GRANTED) {
            sensorManager.registerListener(this, heartRateSensor, SensorManager.SENSOR_DELAY_NORMAL)
        }
    }

    override fun onPause() {
        super.onPause()
        // Unregister sensor listener when app is paused to save battery
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        // Update heart rate display if heart rate sensor data changes
        if (event?.sensor?.type == Sensor.TYPE_HEART_RATE) {
            val heartRate = event.values[0]
            if (heartRate > 0) { // Only display valid heart rate values
                heartRateTextView.text = "Heart Rate: ${heartRate.toInt()} bpm"
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Not typically used for simple heart rate monitoring
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        // Handle permission request results
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
