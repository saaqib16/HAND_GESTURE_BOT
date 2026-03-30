import platform
import queue
import shutil
import subprocess
import threading
import time


class SpeechAnnouncer:
    def __init__(self, cooldown_seconds=1.5):
        self.cooldown_seconds = cooldown_seconds
        self.last_spoken_text = None
        self.last_spoken_at = 0.0
        self.messages = queue.Queue()
        self.running = True
        self.worker = threading.Thread(target=self._run, daemon=True)
        self.worker.start()

    def announce(self, text):
        now = time.time()
        if text == "None":
            return
        if text == self.last_spoken_text and now - self.last_spoken_at < self.cooldown_seconds:
            return

        self.last_spoken_text = text
        self.last_spoken_at = now
        self.messages.put(self._speech_text(text))

    def stop(self):
        self.running = False
        self.messages.put(None)
        self.worker.join(timeout=1)

    def _run(self):
        while self.running:
            message = self.messages.get()
            if message is None:
                break
            self._speak(message)

    def _speech_text(self, text):
        spoken_labels = {
            "Fist ✊": "Sorry",
            "Open Hand ✋": "Stop It",
            "Thumbs Up 👍": "Good Job",
            "Thumbs Down 👎": "Thumbs Down",
            "Peace ✌️": "Peace",
            "OK 👌": "Okay Sir",
            "Pointing Up ☝️": "Pointing Up",
            "Call Me 🤙": "Call Me",
            "I Love You 🤟": "I Love You",
            "Rock On 🤘": "Rock On",
            "Three 3️⃣": "Three",
            "Four 4️⃣": "Four",
        }
        return spoken_labels.get(text, text)

    def _speak(self, text):
        system = platform.system()

        if system == "Darwin" and shutil.which("say"):
            subprocess.run(["say", text], check=False)
            return

        if system == "Linux":
            if shutil.which("spd-say"):
                subprocess.run(["spd-say", text], check=False)
                return
            if shutil.which("espeak"):
                subprocess.run(["espeak", text], check=False)
                return

        if system == "Windows":
            powershell = shutil.which("powershell")
            if powershell:
                command = (
                    "Add-Type -AssemblyName System.Speech; "
                    "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("
                    f"'{text}')"
                )
                subprocess.run([powershell, "-Command", command], check=False)
