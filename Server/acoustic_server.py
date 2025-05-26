# acoustic_server.py
import pyaudio
import numpy as np
from scipy.fft import fft, fftfreq
import time
from sqlalchemy.orm import Session
from database import SessionLocal
from managers.diver_manager import DiverManager

# --- הגדרות פרוטוקול התקשורת ---

# מילון הממפה כל תו לתדר ייחודי (ב-Hz)
# בחרנו תדרים גבוהים יחסית כדי להפחית רגישות לרעשי רקע נמוכים
CHAR_TO_FREQ = {
    '0': 10000, '1': 10500, '2': 11000, '3': 11500, '4': 12000,
    '5': 12500, '6': 13000, '7': 13500, '8': 14000, '9': 14500,
    'a': 15000, 'b': 15500, 'c': 16000, 'd': 16500, 'e': 17000, 'f': 17500,
    'g': 18000, 'h': 18500, 'i': 19000, 'j': 19500, 'k': 20000, 'l': 5000,
    'm': 5500, 'n': 6000, 'o': 6500, 'p': 7000, 'q': 7500, 'r': 8000,
    's': 8500, 't': 9000, 'u': 9500, 'v': 4000, 'w': 4500, 'x': 2500,
    'y': 3000, 'z': 3500,
    '-': 20500, ',': 21000
}
# יצירת מילון הפוך לפענוח קל
FREQ_TO_CHAR = {v: k for k, v in CHAR_TO_FREQ.items()}

# הגדרות טכניות להקלטה וניתוח
CHUNK_DURATION = 0.1  # משך כל "חתיכת" אודיו שננתח (בשניות)
RATE = 44100  # קצב דגימה סטנדרטי
CHUNK_SIZE = int(RATE * CHUNK_DURATION)
START_FREQ = 21500  # תדר מיוחד המסמן תחילת הודעה
END_FREQ = 22000    # תדר מיוחד המסמן סוף הודעה

# --- לוגיקת השרת ---

class AcousticServer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK_SIZE)
        self.db_session: Session = SessionLocal()
        self.diver_manager = DiverManager(self.db_session)
        self.is_recording = False
        self.message_buffer = []

    def _find_dominant_freq(self, data):
        """ מבצע FFT ומחזיר את התדר הדומיננטי ביותר """
        yf = fft(data)
        xf = fftfreq(CHUNK_SIZE, 1 / RATE)
        # מתמקדים רק בתדרים החיוביים
        positive_mask = np.where(xf > 0)
        freqs = xf[positive_mask]
        amps = np.abs(yf[positive_mask])
        
        # התעלמות מרעשים חלשים מאוד
        if np.max(amps) < 1e5: # ערך סף שניתן לכייל
            return None

        dominant_freq_index = np.argmax(amps)
        return freqs[dominant_freq_index]

    def _get_closest_char(self, freq):
        """ מוצא את התו שהתדר שלו הכי קרוב לתדר שנמצא """
        if freq is None:
            return None
        
        # מצא את התדר המוגדר שהכי קרוב לתדר שקלטנו
        closest_defined_freq = min(FREQ_TO_CHAR.keys(), key=lambda k: abs(k - freq))
        
        # אם ההפרש גדול מדי, כנראה שזה רעש
        if abs(closest_defined_freq - freq) > 200: # מרווח טעות של 200Hz
            return None
        
        return FREQ_TO_CHAR[closest_defined_freq]

    def process_message(self):
        """ מרכיב את ההודעה, מעבד אותה ומנקה את המאגר """
        if not self.message_buffer:
            return

        full_message = "".join(self.message_buffer)
        print(f"--- Decoded Full Message: '{full_message}' ---")

        try:
            diver_id, bpm_str = full_message.split(',')
            bpm = int(bpm_str)
            
            # עדכון מסד הנתונים
            diver_to_update = self.diver_manager.get_diver_by_id(diver_id)
            if diver_to_update:
                diver_to_update.bpm = bpm
                self.db_session.commit()
                print(f"SUCCESS: Updated diver '{diver_id}' BPM to {bpm}")
            else:
                print(f"ERROR: Diver with ID '{diver_id}' not found.")
        
        except ValueError:
            print(f"ERROR: Malformed message received: '{full_message}'")
        except Exception as e:
            print(f"ERROR: Could not process message. Error: {e}")
        
        finally:
            self.message_buffer = [] # ניקוי המאגר להודעה הבאה

    def listen(self):
        """ הלולאה הראשית שמאזינה למיקרופון """
        print("Acoustic server is listening... Press Ctrl+C to stop.")
        try:
            while True:
                data = np.frombuffer(self.stream.read(CHUNK_SIZE), dtype=np.int16)
                dominant_freq = self._find_dominant_freq(data)
                
                # בדיקה אם קיבלנו צליל של תחילת הודעה
                if dominant_freq and abs(dominant_freq - START_FREQ) < 200:
                    if not self.is_recording:
                        print("\n>>> Start sequence detected. Recording message...")
                        self.is_recording = True
                        self.message_buffer = [] # ניקוי מאגר ישן
                    continue # דלג להקלטה הבאה

                # בדיקה אם קיבלנו צליל של סוף הודעה
                if dominant_freq and abs(dominant_freq - END_FREQ) < 200:
                    if self.is_recording:
                        print("<<< End sequence detected. Processing message...")
                        self.is_recording = False
                        self.process_message()
                    continue

                # אם אנחנו במצב הקלטה, ננסה לפענח את התו
                if self.is_recording:
                    char = self._get_closest_char(dominant_freq)
                    if char:
                        print(f"Character detected: '{char}' (freq: {dominant_freq:.0f} Hz)")
                        self.message_buffer.append(char)

        except KeyboardInterrupt:
            print("\nStopping server.")
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.db_session.close()

if __name__ == "__main__":
    server = AcousticServer()
    server.listen()