import pyaudio
import numpy as np
from scipy.fft import fft, fftfreq
import time
from sqlalchemy.orm import Session
from database import SessionLocal
from managers.diver_manager import DiverManager
from models.diver import Diver as DiverModel
from models.group import Group


# --- Acoustic Communication Protocol Settings ---

CHAR_TO_FREQ = {
    '0': 3000, '1': 3200, '2': 3400, '3': 3600, '4': 3800,
    '5': 4000, '6': 4200, '7': 4400, '8': 4600, '9': 4800,
    'a': 5000, 'b': 5200, 'c': 5400, 'd': 5600, 'e': 5800,
    'f': 6000, 'g': 6200, 'h': 6400, 'i': 6600, 'j': 6800,
    'k': 7000, 'l': 7200, 'm': 7400, 'n': 7600, 'o': 7800,
    'p': 8000, 'q': 8200, 'r': 8400, 's': 8600, 't': 8800,
    'u': 9000, 'v': 9200, 'w': 9400, 'x': 9600, 'y': 9800,
    'z': 10000, '-': 2200, ',': 2000 
}
FREQ_TO_CHAR = {v: k for k, v in CHAR_TO_FREQ.items()}

RATE = 44100
BUFFER_CHUNK_SIZE = 1024  # Smaller chunks for continuous listening

START_FREQ = 1200  # Match watch app's start frequency
END_FREQ = 11000  # Match watch app's end frequency

# Timing parameters
FFT_WINDOW_SIZE = int(0.25 * RATE)  # Reduced for faster processing
MAX_SILENT_TIME = 15.0  
DIGIT_WAIT_TIME = 0  # Time to wait for additional digits after receiving a valid but potentially incomplete BPM

# Signal strength thresholds
CHAR_THRESHOLD = 5e2  # Reduced threshold for better sensitivity
START_END_THRESHOLD = 1.5e3  # Reduced threshold
END_FREQ_TOLERANCE = 500  # Tolerance for end frequency detection
SIGNAL_STRENGTH_SENSITIVITY_THRESHOLD = 100  # Reduced for better sensitivity  

# Message validation
MIN_MESSAGE_LENGTH = 4  # Minimum length for a valid message (e.g., "a,99")
MAX_MESSAGE_LENGTH = 10  # Maximum length for a valid message (e.g., "abcdef,123")

class AcousticServer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        # Open the audio stream for input (microphone)
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=BUFFER_CHUNK_SIZE,
                                  input_device_index=2) 
        
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
        self.max_silent_time = MAX_SILENT_TIME # Use the global constant for consistency

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
        
        # Reduced tolerance for frequency matching to improve accuracy
        if abs(closest_defined_freq - freq) > 150:  # Reduced from 200 Hz to 150 Hz
            return None
        
        return FREQ_TO_CHAR[closest_defined_freq]

    def process_message(self, message):
        """
        Processes the fully decoded message, attempts to parse ID and BPM,
        and updates the diver's data in the database.
        
        Args:
            message (str): The decoded string message (e.g., "li95" or "li,95").
        """
        print(f"\n=== Processing Message: '{message}' ===")

        try:
            # Find where numbers start
            number_start = -1
            for i, char in enumerate(message):
                if char.isdigit():
                    number_start = i
                    break
            
            if number_start == -1:
                print("❌ ERROR: No BPM found in message")
                return False
                
            # Split into ID and BPM
            diver_id = message[:number_start].replace(',', '')  # Remove any comma
            bpm_str = message[number_start:].replace(',', '')  # Remove any comma

            if bpm_str.isdigit():
                bpm = int(bpm_str)
                print(f"Parsed: Diver ID = {diver_id}, BPM = {bpm}")
                
                # Get the diver from database
                diver = self.db_session.query(DiverModel).filter(DiverModel.id == diver_id).first()
                if diver:
                    # Update BPM and status
                    old_bpm = diver.bpm
                    old_status = diver.status
                    
                    diver.bpm = bpm
                    if bpm > 150:
                        diver.status = "critical"
                    elif bpm > 120:
                        diver.status = "warning"
                    else:
                        diver.status = "normal"
                    
                    # Save changes
                    self.db_session.commit()
                    print(f"\nDiver {diver_id} updated:")
                    print(f"  BPM: {old_bpm} -> {bpm}")
                    print(f"  Status: {old_status} -> {diver.status}")
                    if diver.status != "normal":
                        print(f"\n⚠️ ALERT: Diver {diver_id} status is {diver.status.upper()}")
                    return True
                else:
                    print(f"❌ ERROR: Diver {diver_id} not found in database")
            else:
                print(f"❌ ERROR: Invalid BPM format: '{bpm_str}'")
        except Exception as e:
            print(f"❌ ERROR processing message: {e}")
            self.db_session.rollback()
        print("=" * 40)
        return False

    def listen(self):
        """
        Main listening loop for the acoustic server.
        Continuously reads audio, detects signals, and processes messages.
        """
        print("Acoustic server is listening... Press Ctrl+C to stop.")
        
        audio_buffer = np.array([], dtype=np.int16) # Buffer to accumulate audio data for FFT
        
        try:
            while True:
                # Read a small chunk of audio data
                data = self.stream.read(BUFFER_CHUNK_SIZE, exception_on_overflow=False)
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                
                # Get the maximum amplitude in the current chunk to detect significant sound
                max_amp_in_chunk = np.max(np.abs(audio_chunk))
                
                # If significant sound is detected, add it to the audio buffer
                if max_amp_in_chunk > SIGNAL_STRENGTH_SENSITIVITY_THRESHOLD:
                    audio_buffer = np.concatenate((audio_buffer, audio_chunk))
                    
                    # Process smaller buffers more frequently for better character detection
                    if len(audio_buffer) >= FFT_WINDOW_SIZE // 2:  # Process at half window size
                        self._process_audio_buffer(audio_buffer[:FFT_WINDOW_SIZE])
                        # Keep some overlap for continuity
                        audio_buffer = audio_buffer[FFT_WINDOW_SIZE // 4:] if len(audio_buffer) > FFT_WINDOW_SIZE // 4 else np.array([], dtype=np.int16)
                        
                else: # If silence is detected in the current chunk
                    if len(audio_buffer) > 0: # If there was accumulated sound but now it's silent
                        # Process any remaining substantial audio in the buffer
                        if len(audio_buffer) >= FFT_WINDOW_SIZE // 2: 
                             self._process_audio_buffer(audio_buffer)
                        audio_buffer = np.array([], dtype=np.int16) # Reset buffer

                    # If recording is active and silence persists for too long
                    if self.is_recording and (time.time() - self.last_char_time) > self.max_silent_time:
                        current_message = "".join(self.message_buffer)
                        # Only reset if we don't have a valid message format
                        if not self._is_valid_message(current_message):
                            print("Timeout during recording. No valid message received.")
                            self.is_recording = False
                            self.message_buffer = []
                        else:
                            # If we have a valid message, process it
                            print(f"Message complete: '{current_message}'")
                            self.process_message(current_message)
                            self.message_buffer = []
                            self.is_recording = False

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

        # Use the configured FFT window size that matches the watch's chunk duration
        if len(buffer_data) < FFT_WINDOW_SIZE:
            padded_data = np.pad(buffer_data, (0, FFT_WINDOW_SIZE - len(buffer_data)), 'constant')
            audio_for_fft = padded_data
        else:
            audio_for_fft = buffer_data[-FFT_WINDOW_SIZE:]  # Use the most recent part of the buffer

        # Detect Start Frequency
        start_freq_detected, start_amp = self._find_dominant_freq(audio_for_fft, 
                                                                START_FREQ - 150, START_FREQ + 150, 
                                                                apply_threshold=False)

        # Detect End Frequency
        end_freq_detected, end_amp = self._find_dominant_freq(audio_for_fft, 
                                                            END_FREQ - END_FREQ_TOLERANCE, 
                                                            END_FREQ + END_FREQ_TOLERANCE, 
                                                            apply_threshold=False)

        # Detect character frequencies (including comma)
        char_freq_detected, char_amp = self._find_dominant_freq(audio_for_fft, 
                                                              1900, 10100,  # Range for all characters including comma
                                                              apply_threshold=False)

        # Debug logging - add more detailed logging
        if start_freq_detected is not None and start_amp > START_END_THRESHOLD:
            current_time = time.time()
            if not hasattr(self, '_last_start_signal_time') or \
               (current_time - self._last_start_signal_time) > 0.5:  # Cooldown period of 0.5 seconds
                self._last_start_signal_time = current_time
                print(f"DEBUG: Start signal frequency: {start_freq_detected:.0f} Hz, Amplitude: {start_amp:.0f}")
                if not self.is_recording:
                    self.is_recording = True
                    self.message_buffer = [] # Clear buffer for new message
                    self.last_char_time = time.time()
                    if hasattr(self, '_valid_bpm_time'):
                        delattr(self, '_valid_bpm_time')  # Reset BPM timer on new message
                    print(f"\n>>> Start sequence detected. Start Amp: {start_amp:.0f}. Recording message...")

        if end_freq_detected is not None and end_amp > START_END_THRESHOLD:
            print(f"DEBUG: End signal frequency: {end_freq_detected:.0f} Hz, Amplitude: {end_amp:.0f}")

        if char_freq_detected is not None and char_amp > CHAR_THRESHOLD:
            char = self._get_closest_char(char_freq_detected)
            freq_type = "Comma" if char == ',' else "Character"
            print(f"DEBUG: {freq_type} frequency: {char_freq_detected:.0f} Hz, Amplitude: {char_amp:.0f}, Mapped to: '{char}'")

        # Additional logic for processing characters and end signals remains unchanged...
        if self.is_recording:
            # Enforce a delay after the start signal before processing characters
            if (time.time() - self.last_char_time) < 0.5:  # Match silentDuration from watch app
                return

            # Check for characters (including comma)
            if char_freq_detected is not None and char_amp > CHAR_THRESHOLD:
                char = self._get_closest_char(char_freq_detected)
                if char is not None:
                    if not self.message_buffer or \
                       self.message_buffer[-1] != char or \
                       (time.time() - self.last_char_time) > 0.5:  # Match silentDuration from watch app
                        # Auto-insert comma when transitioning from letters to numbers if no comma exists
                        current_message = "".join(self.message_buffer)
                        if char.isdigit() and ',' not in current_message and \
                           (len(self.message_buffer) > 0 and self.message_buffer[-1].isalpha()):
                            self.message_buffer.append(',')
                            print("Auto-inserted comma before number")
                            
                        self.message_buffer.append(char)
                        current_message = "".join(self.message_buffer)
                        print(f"Current buffer: '{current_message}'")
                        print(f"Character detected: '{char}' (freq: {char_freq_detected:.0f} Hz) (Amp: {char_amp:.0f})")

                        # Only process if we have waited long enough for a complete message
                        if self._is_valid_message(current_message):
                            print(f"Valid message format detected: '{current_message}'")
                            self.process_message(current_message)
                            self.message_buffer = []
                            self.is_recording = False
                            if hasattr(self, '_valid_bpm_time'):
                                delattr(self, '_valid_bpm_time')  # Reset BPM timer
                            print("\nReady for next message...")
                            return
                    self.last_char_time = time.time()

    def _is_valid_message(self, message):
        """Helper function to check if a message is valid (has ID and BPM)"""
        if ',' not in message:
            return False
        parts = message.split(',')
        # Check if we have exactly one comma and both parts are non-empty
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False
        # Check if the first part has at least one character
        if len(parts[0]) == 0:
            return False
        # Check if second part is all digits and within valid BPM range
        if not parts[1].isdigit():
            return False
        bpm = int(parts[1])
        # If BPM is too high, invalid
        if bpm > 200:
            return False
        # If BPM is valid (40-200), mark as potentially complete
        if bpm >= 40:
            # Store the time we first saw a valid BPM
            if not hasattr(self, '_valid_bpm_time'):
                self._valid_bpm_time = time.time()
            # If we've waited long enough for more digits, consider it complete
            if time.time() - self._valid_bpm_time >= DIGIT_WAIT_TIME:
                delattr(self, '_valid_bpm_time')  # Reset the timer
                return True
            return False  # Keep waiting for potential more digits
        # If BPM is too low, keep waiting
        return False

    def _format_message(self, message):
        """Format message by inserting comma between ID and BPM"""
        for i, char in enumerate(message):
            if char.isdigit():
                return message[:i] + ',' + message[i:]
        return message


if __name__ == "__main__":
    server = AcousticServer()
    server.listen()
