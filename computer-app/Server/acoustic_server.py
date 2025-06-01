import pyaudio
import numpy as np
from scipy.fft import fft, fftfreq
import time
from sqlalchemy.orm import Session
from database import SessionLocal
from managers.diver_manager import DiverManager


# --- Acoustic Communication Protocol Settings ---

# NEW ACOUSTIC PROTOCOL FREQUENCIES (V4) - No collisions, focused range
CHAR_TO_FREQ = {
    '0': 3000, '1': 3200, '2': 3400, '3': 3600, '4': 3800,
    '5': 4000, '6': 4200, '7': 4400, '8': 4600, '9': 4800,
    'a': 5000, 'b': 5200, 'c': 5400, 'd': 5600, 'e': 5800,
    'f': 6000, 'g': 6200, 'h': 6400, 'i': 6600, 'j': 6800,
    'k': 7000, 'l': 7200, 'm': 7400, 'n': 7600, 'o': 7800,
    'p': 8000, 'q': 8200, 'r': 8400, 's': 8600, 't': 8800,
    'u': 9000, 'v': 9200, 'w': 9400, 'x': 9600, 'y': 9800,
    'z': 10000,  '-': 2200, ',': 2000 
}
FREQ_TO_CHAR = {v: k for k, v in CHAR_TO_FREQ.items()}

RATE = 44100
BUFFER_CHUNK_SIZE = 1024 # Smaller chunks for continuous listening

START_FREQ = 1200
END_FREQ = 11000 

# Amplitude thresholds
CHAR_THRESHOLD = 1e4 # Min amplitude for character detection (10,000)
START_END_THRESHOLD = 5e3 # Min amplitude for start/end signal detection (5,000)

AMPLITUDE_SENSITIVITY_THRESHOLD = 500 # Overall amplitude to trigger processing a chunk

class AcousticServer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        # Open the audio stream for input (microphone)
        # input_device_index=1 is a common default, but verify for your system.
        # You can uncomment the device listing loop below to find your microphone's index.
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=BUFFER_CHUNK_SIZE,
                                  input_device_index=1) 
        
        # --- Uncomment to list audio devices and find your microphone's index ---
        # info = self.p.get_host_api_info_by_index(0)
        # numdevices = info.get('deviceCount')
        # for i in range(0, numdevices):
        #     if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        #         print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))
        # -----------------------------------------------------------------------

        self.db_session: Session = SessionLocal() # Initialize database session
        self.diver_manager = DiverManager(self.db_session) # Initialize DiverManager
        self.is_recording = False # Flag to indicate if a message is currently being recorded
        self.message_buffer = [] # Stores detected characters for the current message
        self.last_char_time = time.time() # Timestamp of the last detected character
        self.max_silent_time = 5.0 # Max time (in seconds) allowed between characters before resetting recording

    def _find_dominant_freq(self, data, min_freq, max_freq, apply_threshold=True):
        """
        Performs FFT on audio data to find the dominant frequency within a specified range.
        
        Args:
            data (np.array): Audio data (numpy array of int16 samples).
            min_freq (int): Minimum frequency of interest.
            max_freq (int): Maximum frequency of interest.
            apply_threshold (bool): If True, apply CHAR_THRESHOLD to max_amplitude.
            
        Returns:
            tuple: (dominant_frequency, max_amplitude) or (None, 0) if no dominant freq found
                   or if amplitude is below threshold (if apply_threshold is True).
        """
        fft_size = len(data)
        if fft_size == 0:
            return None, 0

        yf = fft(data) # Perform Fast Fourier Transform
        xf = fftfreq(fft_size, 1 / RATE) # Get frequency bins

        # Create a mask to select frequencies within the desired range
        interest_mask = np.where((xf > min_freq) & (xf < max_freq))
        
        if len(interest_mask[0]) == 0: # No frequencies found in the interest range
            return None, 0

        freqs = xf[interest_mask] # Frequencies within the range
        amps = np.abs(yf[interest_mask]) # Corresponding amplitudes

        max_amplitude = np.max(amps) # Get the maximum amplitude in the range
        
        # Apply amplitude threshold if required (for character detection)
        if apply_threshold and max_amplitude < CHAR_THRESHOLD:
            return None, max_amplitude

        dominant_freq_index = np.argmax(amps) # Index of the dominant frequency
        return freqs[dominant_freq_index], max_amplitude

    def _get_closest_char(self, freq):
        """
        Maps a detected frequency to its closest character in the protocol.
        
        Args:
            freq (float): The detected frequency.
            
        Returns:
            str: The character corresponding to the closest frequency, or None if too far.
        """
        if freq is None:
            return None
        
        # Find the defined protocol frequency closest to the detected frequency
        closest_defined_freq = min(FREQ_TO_CHAR.keys(), key=lambda k: abs(k - freq))
        
        # If the detected frequency is too far from any defined protocol frequency, ignore it
        if abs(closest_defined_freq - freq) > 100: # Tolerance of +/- 100 Hz
            return None
        
        return FREQ_TO_CHAR[closest_defined_freq]

    def process_message(self, message):
        """
        Processes the fully decoded message, attempts to parse ID and BPM,
        and saves to the database.
        
        Args:
            message (str): The decoded string message (e.g., "li,84").
        """
        print(f"--- Decoded Full Message: '{message}' ---")
        try:
            parts = message.split(',')
            if len(parts) == 2:
                diver_id = parts[0]
                bpm_str = parts[1]

                if bpm_str.isdigit():
                    bpm = int(bpm_str)
                    print(f"Decoded: Diver ID = {diver_id}, BPM = {bpm}")
                    # Call the DiverManager to save data to the database
                    #self.diver_manager.create_diver_data(diver_id=diver_id, bpm=bpm)
                    #print("Message successfully saved to database.")
                else:
                    print(f"ERROR: Invalid BPM format in message: '{message}'")
            else:
                print(f"ERROR: Malformed message received: '{message}' (Expected 'ID,BPM')")
        except Exception as e:
            print(f"ERROR processing message '{message}': {e}")

    def listen(self):
        """
        Main listening loop for the acoustic server.
        Continuously reads audio, detects signals, and processes messages.
        """
        print("Acoustic server is listening... Press Ctrl+C to stop.")
        
        # FFT window size should match the watch's tone duration for optimal frequency resolution
        FFT_WINDOW_SIZE = int(0.3 * RATE) 

        audio_buffer = np.array([], dtype=np.int16) # Buffer to accumulate audio data for FFT
        
        try:
            while True:
                # Read a small chunk of audio data
                data = self.stream.read(BUFFER_CHUNK_SIZE, exception_on_overflow=False)
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                
                # Get the maximum amplitude in the current chunk to detect significant sound
                max_amp_in_chunk = np.max(np.abs(audio_chunk))
                
                # If significant sound is detected, add it to the audio buffer
                if max_amp_in_chunk > AMPLITUDE_SENSITIVITY_THRESHOLD:
                    audio_buffer = np.concatenate((audio_buffer, audio_chunk))
                    
                    # If enough data is accumulated for an FFT window, process it
                    if len(audio_buffer) >= FFT_WINDOW_SIZE:
                        self._process_audio_buffer(audio_buffer[:FFT_WINDOW_SIZE])
                        audio_buffer = np.array([], dtype=np.int16) # Clear buffer after processing
                        
                else: # If silence is detected in the current chunk
                    if len(audio_buffer) > 0: # If there was accumulated sound but now it's silent
                        # Process any remaining substantial audio in the buffer
                        if len(audio_buffer) >= FFT_WINDOW_SIZE // 2: 
                             self._process_audio_buffer(audio_buffer)
                        audio_buffer = np.array([], dtype=np.int16) # Reset buffer

                    # If recording is active and silence persists for too long, reset the message
                    if self.is_recording and (time.time() - self.last_char_time) > self.max_silent_time:
                        print("Timeout during recording. Resetting message buffer.")
                        self.is_recording = False
                        self.message_buffer = []

        except KeyboardInterrupt:
            print("\nStopping server.")
        except Exception as e:
            print(f"An error occurred in listen loop: {e}")
        finally:
            # Ensure audio stream and PyAudio resources are properly closed
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.db_session.close() # Close database session

    def _process_audio_buffer(self, buffer_data):
        """ 
        Helper function to analyze a larger audio buffer for start, end, 
        and character frequencies.
        """
        if len(buffer_data) == 0:
            return

        FFT_WINDOW_SIZE = int(0.3 * RATE)
        
        # Pad the data if it's shorter than the FFT window size for consistent FFT results
        if len(buffer_data) < FFT_WINDOW_SIZE:
            padded_data = np.pad(buffer_data, (0, FFT_WINDOW_SIZE - len(buffer_data)), 'constant')
            audio_for_fft = padded_data
        else:
            audio_for_fft = buffer_data[-FFT_WINDOW_SIZE:] # Use the most recent part of the buffer

        # Detect Start Frequency
        start_freq_detected, start_amp = self._find_dominant_freq(audio_for_fft, 
                                                                   START_FREQ - 50, START_FREQ + 50, 
                                                                   apply_threshold=False) # No amplitude threshold for raw detection

        # Detect End Frequency
        end_freq_detected, end_amp = self._find_dominant_freq(audio_for_fft, 
                                                               END_FREQ - 50, END_FREQ + 50, 
                                                               apply_threshold=False) # No amplitude threshold for raw detection

        # Detect Character Frequencies (temporarily apply_threshold=False for debugging,
        # but the check `char_amp > CHAR_THRESHOLD` below still applies for adding to buffer)
        char_freq_detected, char_amp = self._find_dominant_freq(audio_for_fft, 
                                                                1900, 10100, 
                                                                apply_threshold=False) 

        # --- Debug prints (uncomment if you need more detailed insight) ---
        # if start_freq_detected is not None and start_amp > 1000:
        #     print(f"DEBUG: Potential Start Freq: {start_freq_detected:.0f} Hz, Amp: {start_amp:.0f}")
        # if end_freq_detected is not None and end_amp > 1000:
        #     print(f"DEBUG: Potential End Freq: {end_freq_detected:.0f} Hz, Amp: {end_amp:.0f}")
        # if char_freq_detected is not None:
        #     if char_amp > 500 and not (START_FREQ - 50 <= char_freq_detected <= START_FREQ + 50) and \
        #                           not (END_FREQ - 50 <= char_freq_detected <= END_FREQ + 50):
        #         print(f"DEBUG: Potential Char Freq: {char_freq_detected:.0f} Hz, Amp: {char_amp:.0f}")
        # -------------------------------------------------------------------


        if not self.is_recording:
            # If not recording, check for a start signal
            if start_freq_detected is not None and start_amp > START_END_THRESHOLD:
                self.is_recording = True
                self.message_buffer = [] # Clear buffer for new message
                self.last_char_time = time.time()
                print(f"\n>>> Start sequence detected. Start Amp: {start_amp:.0f}. Recording message...")
        else: # self.is_recording is True
            # If recording, check for an end signal
            if end_freq_detected is not None and end_amp > START_END_THRESHOLD:
                self.is_recording = False
                print(f"<<< End sequence detected. End Amp: {end_amp:.0f}. Processing message...")
                full_message = "".join(self.message_buffer)
                self.process_message(full_message) # Process the complete message
                self.message_buffer = [] # Reset buffer after processing
            # If not an end signal, check for a character tone
            elif char_freq_detected is not None and char_amp > CHAR_THRESHOLD: # Only add if amplitude is high enough
                char = self._get_closest_char(char_freq_detected)
                if char is not None:
                    # Debounce: Add character only if it's different from the last one,
                    # or if enough time has passed (to avoid duplicate detections from a single long tone)
                    if not self.message_buffer or \
                       self.message_buffer[-1] != char or \
                       (time.time() - self.last_char_time) > 0.4: 
                        self.message_buffer.append(char)
                        print(f"Character detected: '{char}' (freq: {char_freq_detected:.0f} Hz) (Amp: {char_amp:.0f})")
                    self.last_char_time = time.time() # Update timestamp of last detected char


if __name__ == "__main__":
    server = AcousticServer()
    server.listen()
