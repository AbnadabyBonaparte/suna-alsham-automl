import wave
import math
import struct
import os

os.makedirs("public/sounds", exist_ok=True)

def create_tone(filename, duration, freq, vol=0.5):
    # Gera um arquivo WAV simples (Navegadores tocam WAV mesmo se a extensão for .mp3)
    path = f"public/sounds/{filename}"
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            # Onda Senoidal simples
            value = int(32767.0 * vol * math.sin(2.0 * math.pi * freq * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)
    print(f"✅ Gerado: {path}")

print("--- 🎹 SINTETIZANDO SONS DO SISTEMA ---")
create_tone("click.mp3", 0.1, 800)   # Beep agudo
create_tone("hover.mp3", 0.05, 400)  # Beep grave curto
create_tone("alert.mp3", 0.3, 200)   # Tom de alerta grave
create_tone("ambient.mp3", 1.0, 50)  # Hum grave (fundo)

print("\n🔊 Sons instalados com sucesso (Sintéticos).")
