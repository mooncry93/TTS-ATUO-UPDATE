import os
import sys

# Fix macOS and Windows path environment to make sure ffmpeg is discoverable
for p in ["/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin"]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")

import gc
import time
import license_verify
import socket
import requests
import io
import wave
import math
import struct
import base64
import json
import subprocess
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI App
app = FastAPI(title="Digital_TTS by MR.THY API Gateway")
app.state.transcribe_progress = 0.0
app.state.transcribe_engine = "whisper"
app.state.transcribe_status = ""

def get_model_size_desc(model_size: str) -> str:
    sizes = {
        "tiny": "75MB",
        "base": "140MB",
        "small": "460MB",
        "medium": "1.5GB",
        "large-v3": "3.0GB"
    }
    return sizes.get(model_size, "unknown size")

@app.get("/api/transcribe/progress")
async def get_transcribe_progress():
    return {
        "progress": getattr(app.state, "transcribe_progress", 0.0),
        "engine": getattr(app.state, "transcribe_engine", "whisper"),
        "status": getattr(app.state, "transcribe_status", "")
    }

# Allow CORS for development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-detect local VoxCPM2 model path
def resolve_path(rel_path):
    base_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    cwd_path = os.path.abspath(rel_path)
    if os.path.exists(cwd_path):
        return cwd_path
    path1 = os.path.join(base_dir, rel_path)
    if os.path.exists(path1):
        return path1
    path2 = os.path.join(os.path.dirname(base_dir), rel_path)
    if os.path.exists(path2):
        return path2
    return path1

VOXCPM_LOCAL_PATH = resolve_path("VoxCPM2/models/openbmb__VoxCPM2")
has_voxcpm_local = os.path.exists(VOXCPM_LOCAL_PATH)
if has_voxcpm_local:
    print(f"[SYSTEM] VoxCPM2 local weights detected at {VOXCPM_LOCAL_PATH}. Auto-configured local model pathway.")
else:
    print("[SYSTEM] VoxCPM2 local weights not found. Defaulting to online repository (openbmb/VoxCPM2).")

# Request schema from GUI
class UIRequest(BaseModel):
    engine_selection: str  # "voxcpm", "omnivoice", "fish"
    text: str
    expressiveness: int = 50
    style_intensity: int = 50
    clone_fidelity: int = 75
    reference_audio: Optional[str] = None # base64 or path
    reference_text: Optional[str] = None
    mock_fallback: bool = True
    # New Screenshot fields
    language: str = "km-KH"
    voice: str = "default"
    emotion: str = "neutral"
    style: str = "default"
    speed: float = 1.0
    pitch: int = 0
    volume: int = 100
    format: str = "wav"
    custom_voice_prompt: Optional[str] = None
    low_spec_mode: bool = False

# Helper to check if a local port is listening
def check_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.connect(("127.0.0.1", port))
            return True
        except Exception:
            return False

def build_voxcpm_control(voice: str, emotion: str, style: str, ref_text: str = None, custom_voice_prompt: str = None, is_clone: bool = False) -> str:
    voice_desc = ""
    if is_clone:
        # Identity-neutral control to prevent speaker identity drift
        voice_desc = ""
    else:
        if voice.startswith("designed_") and custom_voice_prompt:
            voice_desc = custom_voice_prompt
        elif ref_text:
            if "Sinn Sisamouth" in ref_text:
                voice_desc = "Sinn Sisamouth style, adult Khmer male speaker, mature voice, retro 1960s vinyl tone, emotional singing cadence"
            elif "Ros Serey Sothea" in ref_text:
                voice_desc = "Ros Serey Sothea style, adult Khmer female speaker, high pitch sweet feminine voice, retro 1960s tone, expressive cadence"
            elif "ព័ត៌មានជាតិ" in ref_text:
                voice_desc = "adult Khmer male speaker, professional news anchor broadcast voice, clear confident formal articulation"
            elif "ព្រឹត្តិការណ៍" in ref_text:
                voice_desc = "adult Khmer female speaker, professional news anchor broadcast voice, clear confident formal articulation"
                
        if not voice_desc:
            if voice == "sokha":
                voice_desc = "adult Khmer male speaker, handsome pleasant masculine man voice, warm smooth deeper tone, clear natural Cambodian Khmer pronunciation, studio quality, confident and expressive"
            elif voice == "sreypich":
                voice_desc = "adult Khmer female speaker, beautiful pleasant feminine woman voice, warm smooth tone, clear natural Cambodian Khmer pronunciation, studio quality, gentle and expressive"
            elif voice == "sokly":
                voice_desc = "young Khmer female child speaker, cute pleasant girl voice, bright smooth feminine child tone, clear natural Cambodian Khmer pronunciation, studio quality"
            elif voice == "default":
                voice_desc = "adult Khmer female speaker, pleasant feminine voice, clear natural Cambodian Khmer pronunciation, studio quality, warm tone"

    emotion_desc = ""
    if is_clone:
        # Identity-neutral emotion prompts for cloned voices to prevent identity drift
        if emotion == "happy":
            emotion_desc = "happy voice"
        elif emotion == "excited":
            emotion_desc = "excited voice"
        elif emotion == "angry":
            emotion_desc = "angry voice"
        elif emotion == "calm":
            emotion_desc = "calm voice"
        elif emotion == "rough":
            emotion_desc = "rough voice"
        elif emotion == "soft":
            emotion_desc = "soft voice"
        elif emotion == "serious":
            emotion_desc = "serious voice"
    else:
        if emotion == "happy":
            emotion_desc = "happy, bright tone, joyful, smiling voice"
        elif emotion == "excited":
            emotion_desc = "excited, highly energetic, bright expressive tone"
        elif emotion == "angry":
            emotion_desc = "angry, intense, aggressive tone, serious"
        elif emotion == "calm":
            emotion_desc = "calm, peaceful, serene, relaxed"
        elif emotion == "rough":
            emotion_desc = "rough, deep tone, gritty"
        elif emotion == "soft":
            emotion_desc = "soft, gentle, whispery, low volume, quiet"
        elif emotion == "serious":
            emotion_desc = "serious, formal, strict, no emotion"

    style_desc = ""
    if is_clone:
        # Identity-neutral style prompts for cloned voices to prevent identity drift
        if style == "news":
            style_desc = "news voice"
        elif style in ["story", "storytelling"]:
            style_desc = "storytelling voice"
        elif style == "chat":
            style_desc = "conversational voice"
        elif style == "poetry":
            style_desc = "poetic voice"
        elif style == "clerk":
            style_desc = "clerk voice"
        elif style == "official":
            style_desc = "official voice"
        elif style == "customer":
            style_desc = "customer service voice"
        elif style == "commercial":
            style_desc = "commercial voice"
    else:
        if style == "news":
            style_desc = "professional news anchor broadcast style, formal narration, fast and punchy tempo"
        elif style in ["story", "storytelling"]:
            style_desc = "storytelling style, narrative, highly expressive, dramatic cadence"
        elif style == "chat":
            style_desc = "conversational style, casual, informal, friendly everyday speech"
        elif style == "poetry":
            style_desc = "poetic style, lyrical, slow cadence, theatrical emotional reading"
        elif style == "clerk":
            style_desc = "helpful assistant clerk style, clear, polite, warm welcoming tone"
        elif style == "official":
            style_desc = "official formal statement style, strict, serious, authoritative tone"
        elif style == "customer":
            style_desc = "customer service agent style, friendly, helpful, polite and reassuring"
        elif style == "commercial":
            style_desc = "commercial advertisement style, enthusiastic, catchy, energetic sales pitch"

    parts = [p for p in [voice_desc, emotion_desc, style_desc] if p]
    return ", ".join(parts)

def parse_bracketed_emotions(text: str, default_emotion: str) -> list[tuple[str, str]]:
    import re
    # Find all emotion brackets e.g. [happy], [serious], etc.
    pattern = r"(\[[a-zA-Z]+\])"
    parts = re.split(pattern, text)
    
    chunks = []
    current_emotion = default_emotion
    valid_emotions = {"neutral", "happy", "excited", "angry", "calm", "rough", "soft", "serious"}
    
    for part in parts:
        if not part:
            continue
        if part.startswith("[") and part.endswith("]"):
            emotion_candidate = part[1:-1].lower()
            if emotion_candidate in valid_emotions:
                current_emotion = emotion_candidate
        else:
            text_val = part.strip()
            if text_val:
                chunks.append((text_val, current_emotion))
                
    # Merge adjacent chunks with the same emotion
    merged_chunks = []
    for txt, emo in chunks:
        if merged_chunks and merged_chunks[-1][1] == emo:
            merged_chunks[-1] = (merged_chunks[-1][0] + " " + txt, emo)
        else:
            merged_chunks.append((txt, emo))
            
    return merged_chunks

def parse_ssml_and_emotions(text: str, default_emotion: str) -> list[dict]:
    import re
    # Match <break time="..."/> tags case-insensitively, supporting smart/curly quotes, various spacing and no quotes
    pattern = r'(?i)(<break\s+time\s*=\s*["\'\u201c\u201d\u2018\u2019]?[0-9]+(?:\.[0-9]+)?\s*(?:ms|s)?["\'\u201c\u201d\u2018\u2019]?\s*/?>)'
    raw_segments = re.split(pattern, text)
    
    segments = []
    current_emotion = default_emotion
    for raw_seg in raw_segments:
        if not raw_seg:
            continue
        
        stripped = raw_seg.strip()
        if stripped.lower().startswith("<break"):
            # Extract duration using a flexible regex search
            match = re.search(r'(?i)time\s*=\s*["\'\u201c\u201d\u2018\u2019]?([0-9]+(?:\.[0-9]+)?)\s*(ms|s)?', stripped)
            ms = 500
            if match:
                try:
                    val = float(match.group(1))
                    unit = match.group(2)
                    if unit and unit.lower() == 's':
                        ms = int(val * 1000)
                    else:
                        ms = int(val)
                except ValueError:
                    pass
            segments.append({
                "type": "break",
                "duration_ms": ms
            })
        else:
            emotion_pattern = r"(\[[a-zA-Z]+\])"
            sub_parts = re.split(emotion_pattern, raw_seg)
            valid_emotions = {"neutral", "happy", "excited", "angry", "calm", "rough", "soft", "serious"}
            
            for sub_part in sub_parts:
                if not sub_part:
                    continue
                if sub_part.startswith("[") and sub_part.endswith("]"):
                    emo_cand = sub_part[1:-1].lower()
                    if emo_cand in valid_emotions:
                        current_emotion = emo_cand
                else:
                    text_val = sub_part.strip()
                    if text_val:
                        segments.append({
                            "type": "text",
                            "text": text_val,
                            "emotion": current_emotion
                        })
    return segments

def generate_silence_wav(duration_ms: int, sample_rate: int = 24000, num_channels: int = 1, bits_per_sample: int = 16) -> bytes:
    import wave
    import io
    duration_sec = duration_ms / 1000.0
    num_frames = int(sample_rate * duration_sec)
    bytes_per_sample = bits_per_sample // 8
    silence_data = b'\x00' * (num_frames * num_channels * bytes_per_sample)
    
    out_io = io.BytesIO()
    with wave.open(out_io, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(bytes_per_sample)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(silence_data)
    return out_io.getvalue()

def merge_wavs_natively(wav_chunks: list[bytes]) -> bytes:
    import wave
    import io
    valid_chunks = []
    sr = None
    channels = None
    width = None
    
    for chunk in wav_chunks:
        if not chunk or not chunk.startswith(b"RIFF"):
            continue
        try:
            with wave.open(io.BytesIO(chunk), "rb") as w:
                chunk_sr = w.getframerate()
                chunk_ch = w.getnchannels()
                chunk_wd = w.getsampwidth()
                if sr is None:
                    sr = chunk_sr
                    channels = chunk_ch
                    width = chunk_wd
                if chunk_sr == sr and chunk_ch == channels and chunk_wd == width:
                    valid_chunks.append(chunk)
                else:
                    print(f"[SYSTEM] Native merge format mismatch. Expected sr={sr}, ch={channels}, w={width}. Got sr={chunk_sr}, ch={chunk_ch}, w={chunk_wd}")
        except Exception as e:
            print(f"[SYSTEM] Error reading chunk headers for native merge: {e}")
            
    if not valid_chunks:
        return wav_chunks[0] if wav_chunks else b""
        
    out_io = io.BytesIO()
    with wave.open(out_io, "wb") as out_wav:
        out_wav.setnchannels(channels)
        out_wav.setsampwidth(width)
        out_wav.setframerate(sr)
        for chunk in valid_chunks:
            try:
                with wave.open(io.BytesIO(chunk), "rb") as w:
                    frames = w.readframes(w.getnframes())
                    out_wav.writeframes(frames)
            except Exception as e:
                print(f"[SYSTEM] Error appending frames in native merge: {e}")
    return out_io.getvalue()



def concatenate_wav_bytes(wav_chunks: list[bytes]) -> bytes:
    if not wav_chunks:
        return b""
    if len(wav_chunks) == 1:
        return wav_chunks[0]
    
    import io
    try:
        import soundfile as sf
        import numpy as np
        
        arrays = []
        sr = None
        for chunk in wav_chunks:
            try:
                data, sample_rate = sf.read(io.BytesIO(chunk))
                arrays.append(data)
                if sr is None:
                    sr = sample_rate
            except Exception as e:
                print(f"[SYSTEM] Skipping chunk due to read error: {e}")
                continue
                
        if not arrays:
            return wav_chunks[0]
            
        combined = np.concatenate(arrays, axis=0)
        out_io = io.BytesIO()
        sf.write(out_io, combined, sr, format='WAV', subtype='PCM_16')
        return out_io.getvalue()
    except Exception as e:
        print(f"[SYSTEM] WAV concatenation failed: {e}. Falling back to native merge.")
        try:
            return merge_wavs_natively(wav_chunks)
        except Exception as e2:
            print(f"[SYSTEM] Native WAV merge failed too: {e2}. Returning first chunk.")
            return wav_chunks[0]

def analyze_reference_audio(audio_path: str):
    """
    Extracts key voice parameters from the reference audio:
    - pitch_factor: ratio compared to standard voice (approx 170Hz)
    - equalizer_filters: list of FFmpeg equalizer filter strings
    - reverb_detected: whether to apply room echo/reverb
    """
    if not audio_path:
        return 1.0, [], False
        
    import os
    if not os.path.exists(audio_path):
        return 1.0, [], False
        
    try:
        import numpy as np
        import soundfile as sf
        import librosa
        
        # Load audio with librosa
        y, sr = librosa.load(audio_path, sr=24000)
        if len(y) == 0:
            return 1.0, [], False
            
        # 1. Pitch analysis
        median_f0 = 170.0
        try:
            # Estimate fundamental frequency (F0) using YIN
            # Voice pitch ranges from 60Hz to 400Hz typically
            f0 = librosa.yin(y, fmin=60, fmax=400, sr=sr)
            voiced_f0 = f0[f0 > 0]
            voiced_f0 = voiced_f0[~np.isnan(voiced_f0)]
            if len(voiced_f0) > 0:
                median_f0 = float(np.median(voiced_f0))
        except Exception as yin_err:
            print(f"[AUDIO ANALYSIS] YIN pitch estimation error: {yin_err}")
            
        # Standard base pitch for normal speaking voice is around 170Hz
        pitch_factor = median_f0 / 170.0
        # Constrain pitch factor to reasonable bounds [0.65, 1.45]
        pitch_factor = float(np.clip(pitch_factor, 0.65, 1.45))
        
        # 2. Spectral analysis for equalizer matching
        extra_filters = []
        try:
            # Get STFT to analyze frequency bands
            stft = np.abs(librosa.stft(y))
            frequencies = librosa.fft_frequencies(sr=sr)
            mean_spectrum = np.mean(stft, axis=1)
            
            # Define 4 bands: Bass (<250Hz), Mid-Low (250-1000Hz), Mid-High (1000-4000Hz), Treble (>4000Hz)
            bands = [
                (frequencies < 250, 100),
                ((frequencies >= 250) & (frequencies < 1000), 500),
                ((frequencies >= 1000) & (frequencies < 4000), 2000),
                (frequencies >= 4000, 8000)
            ]
            
            band_energies = []
            for mask, center_freq in bands:
                energy = np.sum(mean_spectrum[mask]) if np.any(mask) else 0.001
                band_energies.append(energy)
                
            # Normalize energies relative to total energy
            total_energy = sum(band_energies) or 1.0
            normalized_energies = [e / total_energy for e in band_energies]
            
            # Standard flat speech spectrum energies (typical distribution)
            flat_reference = [0.40, 0.35, 0.20, 0.05]
            
            # Calculate gain in dB for each band
            for norm, ref_energy, (mask, center_f) in zip(normalized_energies, flat_reference, bands):
                ratio = norm / ref_energy
                # Convert ratio to dB, cap at [-10, 10] dB
                gain_db = 10 * np.log10(ratio) if ratio > 0 else 0
                gain_db = float(np.clip(gain_db, -10.0, 10.0))
                if abs(gain_db) > 1.5:
                    extra_filters.append(f"equalizer=f={center_f}:width_type=o:width=1.5:g={gain_db:.2f}")
        except Exception as spec_err:
            print(f"[AUDIO ANALYSIS] Spectral analysis error: {spec_err}")
            
        # 3. Simple room reverb / echo detection
        reverb_detected = False
        try:
            rms = librosa.feature.rms(y=y)[0]
            percentile_10 = np.percentile(rms, 10)
            percentile_90 = np.percentile(rms, 90)
            reverb_ratio = percentile_10 / (percentile_90 + 1e-6)
            reverb_detected = bool(reverb_ratio > 0.15)
        except Exception as rev_err:
            print(f"[AUDIO ANALYSIS] Reverb detection error: {rev_err}")
            
        return pitch_factor, extra_filters, reverb_detected
    except Exception as e:
        print(f"[AUDIO ANALYSIS] General exception: {e}")
        return 1.0, [], False

def apply_prompt_based_filters(prompt: str, pitch_factor: float, extra_filters: list, echo: bool, speed: float) -> tuple[float, list, bool, float]:
    if not prompt:
        return pitch_factor, extra_filters, echo, speed
    p = prompt.lower()
    if "child" in p or "young" in p or "kids" in p:
        pitch_factor *= 1.32
    elif "female" in p or "woman" in p or "girl" in p or "lady" in p:
        pitch_factor *= 1.18
    elif "male" in p or "man" in p or "boy" in p or "gentleman" in p:
        pitch_factor *= 0.82
    if "deep" in p or "bass" in p or "mature" in p:
        pitch_factor *= 0.88
        extra_filters.append("equalizer=f=100:width_type=o:width=1.5:g=6.0")
    if "bright" in p or "high" in p or "sweet" in p or "crisp" in p:
        pitch_factor *= 1.08
        extra_filters.append("equalizer=f=6000:width_type=o:width=1.5:g=6.0")
    if "whisper" in p or "soft" in p or "gentle" in p or "quiet" in p:
        pitch_factor *= 0.95
        extra_filters.append("lowpass=f=4000")
        speed *= 0.92
    if "robot" in p or "metallic" in p or "synth" in p:
        extra_filters.append("flanger=delay=8:depth=0.8:regen=80:width=80")
    if "echo" in p or "reverb" in p or "hall" in p or "room" in p:
        echo = True
    if "fast" in p or "speedy" in p or "rapid" in p:
        speed *= 1.15
    if "slow" in p or "calm" in p or "relaxed" in p:
        speed *= 0.88
    return pitch_factor, extra_filters, echo, speed

def generate_say_wav(text: str, language: str, sample_rate: int) -> bytes:
    import subprocess
    import tempfile
    import os
    aiff_fd, aiff_path = tempfile.mkstemp(suffix=".aiff")
    wav_fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(aiff_fd)
    os.close(wav_fd)
    try:
        lang = language.lower()
        cmd_say = ["say", "-o", aiff_path]
        if "km" in lang:
            cmd_say += ["-v", "Kanya"]
        cmd_say.append(text)
        subprocess.run(cmd_say, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        cmd_conv = [
            "ffmpeg", "-y", "-i", aiff_path,
            "-ar", str(sample_rate), "-acodec", "pcm_s16le", wav_path
        ]
        subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        with open(wav_path, "rb") as f:
            return f.read()
    except Exception as err:
        try:
            cmd_say = ["say", "-o", aiff_path, text]
            subprocess.run(cmd_say, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            cmd_conv = [
                "ffmpeg", "-y", "-i", aiff_path,
                "-ar", str(sample_rate), "-acodec", "pcm_s16le", wav_path
            ]
            subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            with open(wav_path, "rb") as f:
                return f.read()
        except Exception:
            return b""
    finally:
        for p in [aiff_path, wav_path]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except:
                    pass

def generate_pyttsx3_wav(text: str, language: str, sample_rate: int) -> bytes:
    import tempfile
    import os
    try:
        import pyttsx3
        wav_fd, wav_path = tempfile.mkstemp(suffix=".wav")
        os.close(wav_fd)
        
        # Initialize engine
        engine = pyttsx3.init()
        
        # Try to find a matching voice for the language
        voices = engine.getProperty('voices')
        lang_code = language.split("-")[0].lower()
        
        selected_voice = None
        for voice in voices:
            if hasattr(voice, 'languages') and voice.languages:
                for v_lang in voice.languages:
                    if lang_code in v_lang.lower():
                        selected_voice = voice.id
                        break
            if not selected_voice and lang_code in voice.name.lower():
                selected_voice = voice.id
            if selected_voice:
                break
                
        if selected_voice:
            engine.setProperty('voice', selected_voice)
            
        engine.setProperty('rate', 150)
        engine.save_to_file(text, wav_path)
        engine.runAndWait()
        
        if os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
            import subprocess
            resample_path = wav_path + "_resampled.wav"
            cmd = [
                "ffmpeg", "-y", "-i", wav_path,
                "-ar", str(sample_rate), "-acodec", "pcm_s16le", resample_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(resample_path):
                with open(resample_path, "rb") as f:
                    data = f.read()
                try:
                    os.remove(resample_path)
                except:
                    pass
                try:
                    os.remove(wav_path)
                except:
                    pass
                return data
            else:
                with open(wav_path, "rb") as f:
                    data = f.read()
                try:
                    os.remove(wav_path)
                except:
                    pass
                return data
    except Exception as e:
        print(f"[FALLBACK] pyttsx3 generation failed: {e}")
    return b""

# Synthesis helper to generate a wave file in-memory using gTTS or a procedural hum fallback
def generate_mock_wav(
    text: str,
    engine: str,
    expressiveness: int,
    style_intensity: int,
    fidelity: int,
    speed: float = 1.0,
    language: str = "km-KH",
    voice: str = "default",
    emotion: str = "neutral",
    style: str = "default",
    pitch: int = 0,
    volume: int = 100,
    reference_text: str = None,
    has_reference_audio: bool = False,
    custom_voice_prompt: str = None,
    reference_audio_path: str = None
) -> bytes:
    sample_rate = 48000 if engine == "voxcpm" else 24000
    try:
        from gtts import gTTS
        import io
        import os
        import subprocess
        import hashlib
        
        # Determine language code: km-KH -> km, en-US -> en
        lang = language.split("-")[0]
        tts = gTTS(text=text, lang=lang)
        
        mp3_io = io.BytesIO()
        tts.write_to_fp(mp3_io)
        mp3_bytes = mp3_io.getvalue()
        
        # 1. Determine base voice pitch adjustment
        pitch_factor = 1.0
        echo = False
        extra_filters = []
        
        # Check preset cloned voices or custom reference audio
        if has_reference_audio or reference_audio_path:
            ref_txt = reference_text or ""
            if "Sinn Sisamouth" in ref_txt:
                pitch_factor, echo = 0.72, True
            elif "Ros Serey Sothea" in ref_txt:
                pitch_factor, echo = 1.28, True
            elif "ព័ត៌មានជាតិ" in ref_txt:
                pitch_factor, echo = 0.82, False
            elif "ព្រឹត្តិការណ៍" in ref_txt:
                pitch_factor, echo = 1.18, False
            else:
                # Advanced audio feature analysis using librosa if path exists
                if reference_audio_path and os.path.exists(reference_audio_path):
                    pf_ana, eq_filters, reverb_ana = analyze_reference_audio(reference_audio_path)
                    pitch_factor = pf_ana
                    if eq_filters:
                        extra_filters.extend(eq_filters)
                    if reverb_ana:
                        echo = True
                else:
                    # Custom clone hashing for voice stability using MD5 of the audio file contents
                    h = 42
                    if reference_audio_path and os.path.exists(reference_audio_path):
                        try:
                            with open(reference_audio_path, "rb") as rf:
                                audio_data = rf.read()
                            h = int(hashlib.md5(audio_data).hexdigest(), 16)
                        except Exception as e:
                            print(f"[SYSTEM] Failed to read/hash reference audio file for clone: {e}")
                    if h == 42:
                        h = int(hashlib.md5(ref_txt.encode('utf-8')).hexdigest(), 16) if ref_txt else 42
                    
                    # Expand pitch factor range for more distinct voice timbres (0.65 to 1.35)
                    pitch_factor = 0.65 + (h % 70) * 0.01
                    
                    # Apply extra audio effects based on hash to simulate distinct vocal traits
                    if h % 4 == 0:
                        echo = True
                    elif h % 4 == 1:
                        extra_filters.append("flanger=delay=8:depth=0.5:regen=60:width=80")
                    elif h % 4 == 2:
                        extra_filters.append("tremolo=f=5:d=0.7")
                    elif h % 4 == 3:
                        extra_filters.append("vibrato=f=4:d=0.5")
                    
        elif voice.startswith("designed_"):
            val_to_hash = custom_voice_prompt or voice
            h = int(hashlib.md5(val_to_hash.encode('utf-8')).hexdigest(), 16)
            pitch_factor = 0.85 + (h % 30) * 0.01
            if custom_voice_prompt:
                pitch_factor, extra_filters, echo, speed = apply_prompt_based_filters(
                    custom_voice_prompt, pitch_factor, extra_filters, echo, speed
                )
        elif voice == "sokha":
            pitch_factor = 0.78
        elif voice == "sreypich":
            pitch_factor = 1.15
        elif voice == "sokly":
            pitch_factor = 1.32
        elif voice == "default" and lang == "km":
            pitch_factor = 1.05
            
        # 2. Emotion adjustments
        emotion_speed = 1.0
        emotion_volume = 1.0
        if emotion == "happy" or emotion == "excited":
            pitch_factor *= 1.12
            emotion_speed = 1.10
            emotion_volume = 1.10
        elif emotion == "angry" or emotion == "rough":
            pitch_factor *= 0.88
            emotion_speed = 1.05
            emotion_volume = 1.25
        elif emotion == "calm" or emotion == "soft":
            pitch_factor *= 0.95
            emotion_speed = 0.82
            emotion_volume = 0.80
            echo = True
        elif emotion == "serious":
            pitch_factor *= 0.92
            emotion_speed = 0.95
            
        # 3. Style adjustments
        style_speed = 1.0
        style_volume = 1.0
        if style == "news":
            style_speed = 1.05
            style_volume = 1.10
        elif style == "story":
            style_speed = 0.90
            pitch_factor *= 0.95
        elif style == "poetry":
            style_speed = 0.78
            pitch_factor *= 0.92
            echo = True
        elif style == "commercial":
            style_speed = 1.10
            pitch_factor *= 1.05
            style_volume = 1.15
            
        # Combine user speed/pitch slider offsets
        slider_factor = 1.0 + (pitch * 0.04) # -10 to +10 maps to 0.6 to 1.4
        final_pitch = pitch_factor * slider_factor
        
        # Calculate combined tempo
        tempo_comp = 1.0 / final_pitch
        combined_tempo = tempo_comp * speed * emotion_speed * style_speed
        
        # 4. Build ffmpeg filters
        filters = []
        if final_pitch != 1.0:
            filters.append(f"asetrate={sample_rate}*{final_pitch:.4f}")
            
        if combined_tempo != 1.0:
            t = combined_tempo
            while t > 2.0:
                filters.append("atempo=2.0")
                t /= 2.0
            while t < 0.5:
                filters.append("atempo=0.5")
                t /= 0.5
            if abs(t - 1.0) > 0.01:
                filters.append(f"atempo={t:.4f}")
                
        if echo:
            filters.append("aecho=0.8:0.88:60:0.4")
            
        if extra_filters:
            filters.extend(extra_filters)
            
        final_volume = (volume / 100.0) * emotion_volume * style_volume
        if final_volume != 1.0:
            filters.append(f"volume={final_volume:.2f}")
            
        filter_str = ",".join(filters)
        
        # Convert MP3 to WAV with filters
        cmd = ["ffmpeg", "-y", "-i", "pipe:0", "-f", "wav", "-ar", str(sample_rate)]
        if filter_str:
            cmd += ["-af", filter_str]
        cmd += ["-acodec", "pcm_s16le", "pipe:1"]
        
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        wav_bytes, stderr = proc.communicate(input=mp3_bytes)
        if proc.returncode == 0 and len(wav_bytes) > 0:
            return wav_bytes
    except Exception as e:
        print(f"[SYSTEM] gTTS fallback generation failed: {e}. Trying macOS offline say command...")
        try:
            say_bytes = generate_say_wav(text, language, sample_rate)
            if len(say_bytes) > 0:
                cmd = ["ffmpeg", "-y", "-i", "pipe:0", "-f", "wav", "-ar", str(sample_rate)]
                if filter_str:
                    cmd += ["-af", filter_str]
                cmd += ["-acodec", "pcm_s16le", "pipe:1"]
                proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                wav_bytes, stderr = proc.communicate(input=say_bytes)
                if proc.returncode == 0 and len(wav_bytes) > 0:
                    return wav_bytes
            raise Exception("macOS say returned empty or failed")
        except Exception as say_err:
            print(f"[SYSTEM] macOS say command failed: {say_err}. Trying pyttsx3 fallback...")
            try:
                pyttsx_bytes = generate_pyttsx3_wav(text, language, sample_rate)
                if len(pyttsx_bytes) > 0:
                    cmd = ["ffmpeg", "-y", "-i", "pipe:0", "-f", "wav", "-ar", str(sample_rate)]
                    if filter_str:
                        cmd += ["-af", filter_str]
                    cmd += ["-acodec", "pcm_s16le", "pipe:1"]
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    wav_bytes, stderr = proc.communicate(input=pyttsx_bytes)
                    if proc.returncode == 0 and len(wav_bytes) > 0:
                        return wav_bytes
            except Exception as pyttsx_err:
                print(f"[SYSTEM] pyttsx3 fallback failed: {pyttsx_err}. Falling back to procedural hum.")

    # Procedural wave fallback
    base_freq = 130
    if has_reference_audio or reference_audio_path:
        base_freq = int(130 * pitch_factor)
    elif voice.startswith("designed_"):
        val_to_hash = custom_voice_prompt or voice
        import hashlib
        h = int(hashlib.md5(val_to_hash.encode('utf-8')).hexdigest(), 16)
        base_freq = 100 + (h % 120)
    elif voice == "sokha":
        base_freq = 90
    elif voice == "sreypich":
        base_freq = 200
    elif voice == "sokly":
        base_freq = 240
        
    text_len = len(text) if text else 10
    duration_sec = min(max(text_len * 0.08, 1.5), 6.0)
    if speed > 0.1:
        duration_sec /= speed
        
    num_samples = int(duration_sec * sample_rate)
    
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        
        frames = []
        for i in range(num_samples):
            t = float(i) / sample_rate
            pitch_mod = 1.0 + (0.08 * math.sin(2 * math.pi * 1.3 * t))
            freq = base_freq * pitch_mod * (1.0 + pitch * 0.05)
            
            val = math.sin(2 * math.pi * freq * t)
            val += 0.5 * math.sin(2 * math.pi * (freq * 2) * t)
            val += 0.25 * math.sin(2 * math.pi * (freq * 3) * t)
            val /= 1.75
            
            envelope = math.sin(math.pi * t / duration_sec)
            envelope *= (0.65 + 0.35 * math.sin(2 * math.pi * 5.0 * t))
            
            sample = int(val * envelope * 28000 * (volume / 100))
            frames.append(struct.pack('<h', sample))
            
        w.writeframes(b''.join(frames))
    return wav_io.getvalue()


TEMP_UPLOADS_DIR = os.path.abspath("temp_uploads")
os.makedirs(TEMP_UPLOADS_DIR, exist_ok=True)

def process_base64_audio(base64_str: str) -> str:
    """Decodes base64 reference audio, saves to file, converts to WAV if needed.

    Returns the local path of the WAV file.
    """
    import uuid
    if not base64_str:
        return ""
    
    ext = ".webm"  # Default to .webm for safety, so non-wav files always trigger ffmpeg conversion
    try:
        if base64_str.startswith("data:"):
            header, base64_data = base64_str.split(",", 1)
            mime = header.split(";")[0].split(":")[1].lower()
            if "wav" in mime:
                ext = ".wav"
            elif "mp3" in mime or "mpeg" in mime:
                ext = ".mp3"
            elif "m4a" in mime:
                ext = ".m4a"
            elif "mp4" in mime:
                ext = ".mp4"
            elif "aac" in mime:
                ext = ".aac"
            elif "webm" in mime:
                ext = ".webm"
            elif "ogg" in mime:
                ext = ".ogg"
            audio_bytes = base64.b64decode(base64_data)
        else:
            audio_bytes = base64.b64decode(base64_str)
            # If no base64 header is present, we try to detect if it's WAV by signature
            if audio_bytes.startswith(b"RIFF"):
                ext = ".wav"
    except Exception as e:
        print(f"[SYSTEM] Failed to decode base64 audio: {e}")
        return ""
        
    file_id = uuid.uuid4().hex
    input_path = os.path.join(TEMP_UPLOADS_DIR, f"ref_{file_id}{ext}")
    with open(input_path, "wb") as f:
        f.write(audio_bytes)
        
    wav_path = os.path.join(TEMP_UPLOADS_DIR, f"ref_{file_id}.wav")
    if ext == ".wav":
        temp_wav_path = os.path.join(TEMP_UPLOADS_DIR, f"temp_{file_id}.wav")
        cmd = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", temp_wav_path]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            os.replace(temp_wav_path, input_path)
            return input_path
        except Exception as e:
            print(f"[SYSTEM] FFmpeg resampling failed: {e}. Falling back to original path.")
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
            return input_path
    else:
        cmd = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", wav_path]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(input_path):
                os.remove(input_path)
            return wav_path
        except Exception as e:
            print(f"[SYSTEM] FFmpeg conversion failed: {e}. Falling back to original path.")
            return input_path

def convert_wav_to_mp3(wav_bytes: bytes) -> bytes:
    """Converts WAV bytes to MP3 bytes using FFmpeg."""
    try:
        cmd = ["ffmpeg", "-y", "-i", "pipe:0", "-f", "mp3", "-b:a", "192k", "pipe:1"]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        mp3_bytes, stderr = proc.communicate(input=wav_bytes)
        if proc.returncode == 0 and len(mp3_bytes) > 0:
            return mp3_bytes
    except Exception as e:
        print(f"[SYSTEM] FFmpeg MP3 conversion error: {e}")
    return wav_bytes

def normalize_wav_volume(wav_bytes: bytes, emotion: str) -> bytes:
    """Peak-normalizes WAV bytes to a target level based on the emotion to ensure loudness consistency."""
    if not wav_bytes or not wav_bytes.startswith(b"RIFF"):
        return wav_bytes
        
    try:
        import soundfile as sf
        import numpy as np
        import io
        
        # Read the WAV frames
        data, sample_rate = sf.read(io.BytesIO(wav_bytes))
        peak = np.max(np.abs(data))
        if peak < 0.001:
            return wav_bytes
            
        # Target peak depending on emotion style
        target_peak = 0.92
        if emotion in ["soft", "calm"]:
            target_peak = 0.55
        elif emotion in ["angry", "rough"]:
            target_peak = 0.96
            
        # Rescale the samples
        normalized_data = data * (target_peak / peak)
        
        # Write back to WAV format bytes
        out_io = io.BytesIO()
        sf.write(out_io, normalized_data, sample_rate, format='WAV', subtype='PCM_16')
        return out_io.getvalue()
    except Exception as e:
        print(f"[SYSTEM] Peak normalization failed: {e}")
        return wav_bytes

def apply_audio_postprocessing(
    wav_bytes: bytes,
    speed: float = 1.0,
    pitch: int = 0,
    volume: int = 100,
    emotion: str = "neutral",
    style: str = "default",
    sample_rate: int = 48000,
    is_clone: bool = False
) -> bytes:
    """Applies speed, pitch, volume, emotion, and style adjustments to WAV bytes using FFmpeg."""
    if speed == 1.0 and pitch == 0 and volume == 100 and emotion == "neutral" and style in ["default", "none", ""]:
        return wav_bytes
        
    try:
        import subprocess
        # Calculate pitch factor from slider (-10 to +10 maps to 0.6 to 1.4)
        pitch_factor = 1.0 + (pitch * 0.04)
        
        # 2. Emotion adjustments
        emotion_speed = 1.0
        emotion_volume = 1.0
        echo = False
        if emotion == "happy" or emotion == "excited":
            pitch_factor *= 1.05 if is_clone else 1.12
            emotion_speed = 1.05 if is_clone else 1.10
            emotion_volume = 1.05 if is_clone else 1.10
        elif emotion == "angry" or emotion == "rough":
            pitch_factor *= 0.94 if is_clone else 0.88
            emotion_speed = 1.02 if is_clone else 1.05
            emotion_volume = 1.12 if is_clone else 1.25
        elif emotion == "calm" or emotion == "soft":
            pitch_factor *= 0.97 if is_clone else 0.95
            emotion_speed = 0.90 if is_clone else 0.82
            emotion_volume = 0.90 if is_clone else 0.80
            echo = False if is_clone else True
        elif emotion == "serious":
            pitch_factor *= 0.96 if is_clone else 0.92
            emotion_speed = 0.98 if is_clone else 0.95
            
        # 3. Style adjustments
        style_speed = 1.0
        style_volume = 1.0
        if style == "news":
            style_speed = 1.03 if is_clone else 1.05
            style_volume = 1.05 if is_clone else 1.10
        elif style == "story":
            style_speed = 0.95 if is_clone else 0.90
            pitch_factor *= 0.97 if is_clone else 0.95
        elif style == "poetry":
            style_speed = 0.88 if is_clone else 0.78
            pitch_factor *= 0.96 if is_clone else 0.92
            echo = False if is_clone else True
        elif style == "commercial":
            style_speed = 1.05 if is_clone else 1.10
            pitch_factor *= 1.03 if is_clone else 1.05
            style_volume = 1.08 if is_clone else 1.15
        
        # Calculate combined tempo adjustment
        tempo_comp = 1.0 / pitch_factor
        combined_tempo = tempo_comp * speed * emotion_speed * style_speed
        
        filters = []
        if pitch_factor != 1.0:
            filters.append(f"asetrate={sample_rate}*{pitch_factor:.4f}")
            
        if combined_tempo != 1.0:
            t = combined_tempo
            while t > 2.0:
                filters.append("atempo=2.0")
                t /= 2.0
            while t < 0.5:
                filters.append("atempo=0.5")
                t /= 0.5
            if abs(t - 1.0) > 0.01:
                filters.append(f"atempo={t:.4f}")
                
        if echo:
            filters.append("aecho=0.8:0.88:60:0.4")
                
        final_volume = (volume / 100.0) * emotion_volume * style_volume
        if final_volume != 1.0:
            filters.append(f"volume={final_volume:.2f}")
            
        filter_str = ",".join(filters)
        if not filter_str:
            return wav_bytes
            
        cmd = ["ffmpeg", "-y", "-i", "pipe:0", "-f", "wav", "-ar", str(sample_rate)]
        cmd += ["-af", filter_str]
        cmd += ["-acodec", "pcm_s16le", "pipe:1"]
        
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_bytes, stderr = proc.communicate(input=wav_bytes)
        if proc.returncode == 0 and len(out_bytes) > 0:
            return out_bytes
    except Exception as e:
        print(f"[SYSTEM] Post-processing audio filter failed: {e}")
    return wav_bytes

@app.get("/api/status")
async def get_system_status():
    """Probes all three microservice ports and returns status."""
    ports = {
        "fish": 8080,
        "voxcpm": 8081,
        "omnivoice": 8082
    }
    status = {}
    for engine, port in ports.items():
        status[engine] = {
            "port": port,
            "online": check_port(port)
        }
    status["gateway"] = {
        "port": 8000,
        "online": True
    }
    status["voxcpm_local_config"] = {
        "detected": has_voxcpm_local,
        "path": VOXCPM_LOCAL_PATH if has_voxcpm_local else None
    }
    return status

@app.post("/api/cleanup")
async def trigger_cleanup():
    """Triggers GC, PyTorch CUDA cache clearing, and forwards to VoxCPM2 daemon."""
    start_time = time.time()
    freed_torch = False
    
    gc.collect()
    
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            freed_torch = True
        if hasattr(torch, "mps") and torch.backends.mps.is_available():
            torch.mps.empty_cache()
    except ImportError:
        pass
        
    # Forward to real VoxCPM2 model daemon if online
    voxcpm_online = check_port(8081)
    voxcpm_cleared = False
    if voxcpm_online:
        try:
            import requests
            res = requests.post("http://127.0.0.1:8081/cleanup", timeout=5.0)
            if res.status_code == 200:
                voxcpm_cleared = True
        except Exception as e:
            print(f"[SYSTEM] Failed to forward cleanup to VoxCPM2: {e}")
            
    # Also delete temporary generated output WAV files older than 60 seconds to save space
    temp_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(temp_dir, "static")
    purged_files = 0
    if os.path.exists(static_dir):
        for f in os.listdir(static_dir):
            if f.startswith("output_") and (f.endswith(".wav") or f.endswith(".mp3")):
                fpath = os.path.join(static_dir, f)
                # Check if older than 60s
                if time.time() - os.path.getmtime(fpath) > 60.0:
                    try:
                        os.remove(fpath)
                        purged_files += 1
                    except:
                        pass

    duration = time.time() - start_time
    return {
        "status": "success",
        "message": f"Memory cleanup successfully executed in {duration:.4f}s. Purged {purged_files} temp output files.",
        "cuda_cleared": freed_torch,
        "voxcpm_cleared": voxcpm_cleared,
        "purged_temp_files": purged_files
    }

@app.post("/api/download")
async def trigger_download():
    """Triggers the background model downloader script."""
    progress_file = "download_progress.json"
    
    # Check if download is already active
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r") as f:
                data = json.load(f)
                if data.get("downloading", False):
                    return {"status": "already_running", "message": "Model downloader is already active."}
        except:
            pass
            
    # Initialize download_progress.json
    initial_data = {
        "downloading": True,
        "filename": "Warming up...",
        "percent": 0.0,
        "speed_mbps": 0.0,
        "bytes_downloaded": 0,
        "total_bytes": 0,
        "status": "starting"
    }
    with open(progress_file, "w") as f:
        json.dump(initial_data, f)
        
    # Launch downloader in background
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        subprocess.Popen([sys.executable, "--server", "downloader"])
    else:
        subprocess.Popen([sys.executable, "download_models.py"])
    return {"status": "started", "message": "Model downloader initialized in background."}

@app.get("/api/download-status")
async def get_download_status():
    """Polls download_progress.json to check active progress."""
    progress_file = "download_progress.json"
    if not os.path.exists(progress_file):
        return {"downloading": False, "percent": 0, "status": "idle"}
    try:
        with open(progress_file, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"downloading": False, "percent": 0, "status": "error", "error": str(e)}

@app.post("/api/setup")
async def trigger_super_setup():
    """Triggers the background 1-Click Super Setup & Calibrator."""
    progress_file = "setup_progress.json"
    
    # Check if setup is already active
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r") as f:
                data = json.load(f)
                if data.get("active", False):
                    return {"status": "already_running", "message": "Super Setup is already active."}
        except:
            pass
            
    # Initialize setup_progress.json
    initial_data = {
        "active": True,
        "phase": "starting",
        "message": "Initializing 1-Click Environment & Model Setup...",
        "percent": 2.0,
        "status": "running"
    }
    with open(progress_file, "w") as f:
        json.dump(initial_data, f)
        
    # Launch setup script in background
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        subprocess.Popen([sys.executable, "--server", "setup"])
    else:
        subprocess.Popen([sys.executable, os.path.join("UPDATE RELEASE", "setup_env.py")])
    return {"status": "started", "message": "1-Click Super Setup initialized in background."}

@app.get("/api/setup-status")
async def get_setup_status():
    """Polls setup_progress.json to check active progress."""
    progress_file = "setup_progress.json"
    if not os.path.exists(progress_file):
        return {"active": False, "percent": 0, "status": "idle", "message": "Setup has not been run yet."}
    try:
        with open(progress_file, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"active": False, "percent": 0, "status": "error", "message": f"Error loading progress: {str(e)}"}

def load_presets_registry():
    import shutil
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    presets_dir = os.path.join(static_dir, "presets")
    registry_path = os.path.join(presets_dir, "presets_registry.json")
    
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets_backup")
    backup_registry_path = os.path.join(backup_dir, "presets_registry.json")
    
    registry = []
    loaded_from = None
    
    # 1. Try to load from active registry
    if os.path.exists(registry_path):
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
                if isinstance(registry, list) and len(registry) > 0:
                    loaded_from = "active"
        except Exception as e:
            print(f"[SYSTEM] Error reading presets registry: {e}")
            
    # 2. If active registry is empty or missing, try loading from backup registry
    if not loaded_from and os.path.exists(backup_registry_path):
        try:
            with open(backup_registry_path, "r", encoding="utf-8") as f:
                backup_registry = json.load(f)
                if isinstance(backup_registry, list) and len(backup_registry) > 0:
                    registry = backup_registry
                    loaded_from = "backup"
                    print("[SYSTEM] Loaded presets registry from backup file.")
        except Exception as e:
            print(f"[SYSTEM] Error reading backup presets registry: {e}")
            
    # 3. Ensure all audio files in the registry are in place
    dirty = False
    os.makedirs(presets_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    
    for item in registry:
        audio_url = item.get("audio")
        if not audio_url:
            continue
        filename = os.path.basename(audio_url)
        active_file_path = os.path.join(presets_dir, filename)
        backup_file_path = os.path.join(backup_dir, filename)
        
        # If file is missing in active presets but exists in backup, restore it
        if not os.path.exists(active_file_path) and os.path.exists(backup_file_path):
            try:
                shutil.copy2(backup_file_path, active_file_path)
                print(f"[SYSTEM] Restored lost preset audio file from backup: {filename}")
                dirty = True
            except Exception as e:
                print(f"[SYSTEM] Failed to restore file {filename}: {e}")
        # If file exists in active presets but not in backup, make a backup of it
        elif os.path.exists(active_file_path) and not os.path.exists(backup_file_path):
            try:
                shutil.copy2(active_file_path, backup_file_path)
                print(f"[SYSTEM] Backed up preset audio file: {filename}")
            except Exception as e:
                print(f"[SYSTEM] Failed to backup file {filename}: {e}")
                
    # 4. Auto-recovery scanning: detect and register orphan preset files on disk (either in active or backup dirs)
    preset_files = set()
    if os.path.exists(presets_dir):
        preset_files.update([f for f in os.listdir(presets_dir) if f.startswith("preset_") and f.endswith(".wav")])
    if os.path.exists(backup_dir):
        preset_files.update([f for f in os.listdir(backup_dir) if f.startswith("preset_") and f.endswith(".wav")])
        
    registered_urls = {item.get("audio") for item in registry if item.get("audio")}
    
    for pf in preset_files:
        audio_url = f"/presets/{pf}"
        if audio_url not in registered_urls:
            # Sync files
            active_file_path = os.path.join(presets_dir, pf)
            backup_file_path = os.path.join(backup_dir, pf)
            if os.path.exists(backup_file_path) and not os.path.exists(active_file_path):
                try:
                    shutil.copy2(backup_file_path, active_file_path)
                except:
                    pass
            elif os.path.exists(active_file_path) and not os.path.exists(backup_file_path):
                try:
                    shutil.copy2(active_file_path, backup_file_path)
                except:
                    pass
                    
            file_uuid = pf.replace("preset_", "").replace(".wav", "")
            short_id = file_uuid[:8] if len(file_uuid) >= 8 else file_uuid
            recovered_name = f"Recovered Clone ({short_id})"
            
            registry.append({
                "name": recovered_name,
                "audio": audio_url,
                "transcript": ""
            })
            print(f"[SYSTEM] Auto-recovered orphan preset: {pf} as '{recovered_name}'")
            dirty = True
            
    if dirty or loaded_from == "backup":
        save_presets_registry(registry)
        
    return registry

def save_presets_registry(registry):
    import shutil
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    presets_dir = os.path.join(static_dir, "presets")
    os.makedirs(presets_dir, exist_ok=True)
    registry_path = os.path.join(presets_dir, "presets_registry.json")
    
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets_backup")
    os.makedirs(backup_dir, exist_ok=True)
    backup_registry_path = os.path.join(backup_dir, "presets_registry.json")
    
    # 1. Save active registry
    try:
        with open(registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[SYSTEM] Error writing presets registry: {e}")
        
    # 2. Save backup registry
    try:
        with open(backup_registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[SYSTEM] Error writing backup presets registry: {e}")
        
    # 3. Ensure files are backed up
    for item in registry:
        audio_url = item.get("audio")
        if not audio_url:
            continue
        filename = os.path.basename(audio_url)
        active_file_path = os.path.join(presets_dir, filename)
        backup_file_path = os.path.join(backup_dir, filename)
        if os.path.exists(active_file_path) and not os.path.exists(backup_file_path):
            try:
                shutil.copy2(active_file_path, backup_file_path)
            except Exception as e:
                print(f"[SYSTEM] Failed to backup file {filename}: {e}")

class UploadCloneRequest(BaseModel):
    name: str
    audio_base64: str
    transcript: Optional[str] = None

class TranscribeRequest(BaseModel):
    audio_base64: str
    filename: str
    model_size: str = "base"
    output_format: str = "srt"
    language: Optional[str] = None
    engine: str = "whisper"
    api_key: Optional[str] = None



class DeleteCloneRequest(BaseModel):
    audio_url: str

class UpdateCloneRequest(BaseModel):
    audio_url: str
    new_name: str
    new_transcript: Optional[str] = None

@app.get("/api/clones/list")
async def list_cloned_presets():
    try:
        registry = load_presets_registry()
        return {"success": True, "presets": registry}
    except Exception as e:
        return {"success": False, "presets": [], "message": str(e)}

@app.post("/api/clones/update")
async def update_clone_preset(req: UpdateCloneRequest):
    try:
        registry = load_presets_registry()
        updated = False
        for item in registry:
            if item.get("audio") == req.audio_url:
                item["name"] = req.new_name
                if req.new_transcript is not None:
                    item["transcript"] = req.new_transcript
                updated = True
                break
        if updated:
            save_presets_registry(registry)
            return {"success": True}
        return {"success": False, "message": "Preset not found in registry"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.post("/api/clones/upload")
async def upload_clone_preset(req: UploadCloneRequest):
    try:
        import uuid
        ext = ".webm"  # Default to webm for safety, non-wav triggers conversion
        base64_str = req.audio_base64
        if base64_str.startswith("data:"):
            header, base64_data = base64_str.split(",", 1)
            mime = header.split(";")[0].split(":")[1].lower()
            if "wav" in mime:
                ext = ".wav"
            elif "mp3" in mime or "mpeg" in mime:
                ext = ".mp3"
            elif "m4a" in mime:
                ext = ".m4a"
            elif "mp4" in mime:
                ext = ".mp4"
            elif "aac" in mime:
                ext = ".aac"
            elif "webm" in mime:
                ext = ".webm"
            elif "ogg" in mime:
                ext = ".ogg"
            audio_bytes = base64.b64decode(base64_data)
        else:
            audio_bytes = base64.b64decode(base64_str)
            if audio_bytes.startswith(b"RIFF"):
                ext = ".wav"
            
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        presets_dir = os.path.join(static_dir, "presets")
        os.makedirs(presets_dir, exist_ok=True)
        
        file_id = uuid.uuid4().hex
        filename = f"preset_{file_id}{ext}"
        filepath = os.path.join(presets_dir, filename)
        with open(filepath, "wb") as f:
            f.write(audio_bytes)
            
        wav_filename = f"preset_{file_id}.wav"
        wav_filepath = os.path.join(presets_dir, wav_filename)
        
        # If it's already .wav, convert to a temporary path first, then overwrite
        if ext == ".wav":
            temp_wav_path = os.path.join(presets_dir, f"temp_{file_id}.wav")
            cmd = ["ffmpeg", "-y", "-i", filepath, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", temp_wav_path]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                os.replace(temp_wav_path, filepath)
            except Exception as e:
                print(f"[SYSTEM] Failed FFmpeg resampling for preset: {e}")
                if os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)
        else:
            cmd = ["ffmpeg", "-y", "-i", filepath, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", wav_filepath]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                os.remove(filepath)
                filename = wav_filename
                filepath = wav_filepath
            except Exception as e:
                print(f"[SYSTEM] Failed FFmpeg conversion for preset: {e}")
                
        audio_url = f"/presets/{filename}"
        
        # Save to registry
        registry = load_presets_registry()
        # Remove any existing with the same name or url
        registry = [v for v in registry if v.get("name") != req.name and v.get("audio") != audio_url]
        registry.append({
            "name": req.name,
            "audio": audio_url,
            "transcript": req.transcript or ""
        })
        save_presets_registry(registry)
                
        return {
            "success": True,
            "audio_url": audio_url,
            "filepath": filepath
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload preset: {str(e)}")

@app.post("/api/clones/delete")
async def delete_clone_preset(req: DeleteCloneRequest):
    try:
        if not req.audio_url or "presets" not in req.audio_url:
            return {"success": False, "message": "Invalid URL"}
            
        filename = os.path.basename(req.audio_url)
        
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        active_filepath = os.path.join(static_dir, "presets", filename)
        backup_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets_backup", filename)
        
        if os.path.exists(active_filepath):
            os.remove(active_filepath)
        if os.path.exists(backup_filepath):
            os.remove(backup_filepath)
            
        # Remove from registry
        registry = load_presets_registry()
        registry = [v for v in registry if v.get("audio") != req.audio_url]
        save_presets_registry(registry)
        
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.post("/api/generate")
async def route_tts_request(req: UIRequest):
    """Main routing entrypoint. Scales sliders to backend payloads and routes requests."""
    is_valid, _, _, msg = license_verify.check_local_license()
    if not is_valid:
        raise HTTPException(status_code=403, detail=f"Unlicensed Application: {msg}")
    start_time = time.time()
    
    # Scale sliders (0-100) to corresponding engine parameters
    # Cap CFG to 2.0 maximum (or 2.2 max) because VoxCPM produces heavy noise/waves if CFG > 2.0.
    # 50 -> 1.5, 100 -> 2.0
    scaled_cfg = 1.0 + (float(req.style_intensity) / 100.0) * 1.0       # VoxCPM2 CFG: safe range
    
    # Map Fidelity slider to inference steps optimized for speed (8 to 18 steps)
    inference_steps = 8 + int(req.clone_fidelity / 10.0)                # VoxCPM2 steps: 75 -> 15
    
    fidelity_float = float(req.clone_fidelity / 100.0)    # OmniVoice fidelity: 75 -> 0.75
    expressiveness_float = float(req.expressiveness / 100.0) # Fish expressiveness: 50 -> 0.50
    
    engine = req.engine_selection.lower()
    routing_engine = engine
    
    ports = {
        "voxcpm": 8081,
        "omnivoice": 8082,
        "fish": 8080
    }
    
    port = ports.get(engine)
    if not port:
        raise HTTPException(status_code=400, detail=f"Invalid engine: {req.engine_selection}")
        
    is_online = check_port(port)
    
    # Check if reference audio is the dummy preset
    is_dummy_preset = False
    if req.reference_audio:
        try:
            if req.reference_audio.startswith("data:"):
                _, base64_data = req.reference_audio.split(",", 1)
                decoded_len = len(base64.b64decode(base64_data))
            else:
                decoded_len = len(base64.b64decode(req.reference_audio))
            if decoded_len < 1000:
                is_dummy_preset = True
        except Exception:
            pass
            
    reference_wav_path = None
    try:
        if req.reference_audio:
            if is_dummy_preset:
                reference_wav_path = os.path.abspath("VoxCPM2/VoxCPM-main/examples/reference_speaker.wav")
            elif req.reference_audio.startswith("/presets/") or "presets/" in req.reference_audio or req.reference_audio.startswith("/output_"):
                # Resolve relative to static folder on disk
                static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
                potential_path = os.path.join(static_dir, req.reference_audio.lstrip("/"))
                if os.path.exists(potential_path):
                    reference_wav_path = potential_path
                else:
                    reference_wav_path = process_base64_audio(req.reference_audio)
            elif os.path.exists(req.reference_audio):
                reference_wav_path = req.reference_audio
            else:
                reference_wav_path = process_base64_audio(req.reference_audio)
                
        # Parse text into emotion segments and break tags
        segments = parse_ssml_and_emotions(req.text, req.emotion)
        if not segments:
            raise HTTPException(status_code=400, detail="Requested synthesis text is empty or invalid.")
            
        # Optimize segments by merging contiguous text blocks with identical emotions
        optimized_segments = []
        for seg in segments:
            if not optimized_segments:
                optimized_segments.append(seg)
                continue
            last = optimized_segments[-1]
            if last["type"] == "text" and seg["type"] == "text" and last["emotion"] == seg["emotion"]:
                last["text"] = last["text"].rstrip() + " " + seg["text"].lstrip()
            else:
                optimized_segments.append(seg)
        segments = optimized_segments
            
        num_text_segments = len([s for s in segments if s["type"] == "text"])
            
        segment_audios = []
        is_mock_run = not is_online and req.mock_fallback
        text_wav_for_header = None
        
        # Define worker function for parallel segment generation
        def process_text_segment(seg):
            chunk_text = seg["text"]
            chunk_emotion = seg["emotion"]
            
            # Generate mock audio if offline and fallback enabled
            if is_mock_run:
                audio_bytes = generate_mock_wav(
                    text=chunk_text,
                    engine=engine,
                    expressiveness=req.expressiveness,
                    style_intensity=req.style_intensity,
                    fidelity=req.clone_fidelity,
                    speed=req.speed,
                    language=req.language,
                    voice=req.voice,
                    emotion=chunk_emotion,
                    style=req.style,
                    pitch=req.pitch,
                    volume=req.volume,
                    reference_text=req.reference_text,
                    has_reference_audio=bool(req.reference_audio),
                    custom_voice_prompt=req.custom_voice_prompt,
                    reference_audio_path=reference_wav_path
                )
                chunk_bytes = audio_bytes
            else:
                target_port = port
                routing_engine = engine
                
                # Determine if text contains English/Latin letters or explicit en-US select
                is_english = (req.language == "en-US")
                
                # Route request
                if routing_engine == "voxcpm":
                    control = build_voxcpm_control(
                        req.voice, 
                        chunk_emotion, 
                        req.style, 
                        req.reference_text if is_dummy_preset else None, 
                        req.custom_voice_prompt, 
                        is_clone=bool(req.reference_audio)
                    )
                    import re
                    control = re.sub(r"[()（）]", "", control).strip()
                    final_text = f"({control}){chunk_text}" if control else chunk_text
                    
                    model_path = VOXCPM_LOCAL_PATH if has_voxcpm_local else "openbmb/VoxCPM2"
                    use_continuation = (not is_dummy_preset) and bool(req.reference_text) and (num_text_segments == 1)
                    actual_prompt_text = req.reference_text if use_continuation else None
                    actual_prompt_wav = reference_wav_path if use_continuation else None
                    
                    payload = {
                        "text": final_text,
                        "cfg_value": scaled_cfg,
                        "inference_timesteps": inference_steps,
                        "reference_wav_path": reference_wav_path,
                        "prompt_text": actual_prompt_text,
                        "prompt_wav_path": actual_prompt_wav,
                        "model_path": model_path,
                        "emotion": chunk_emotion,
                        "language": req.language,
                        "speed": req.speed,
                        "pitch": req.pitch,
                        "volume": req.volume,
                        "voice": req.voice,
                        "low_spec_mode": req.low_spec_mode
                    }
                    res = requests.post(f"http://127.0.0.1:{target_port}/synthesize", json=payload, timeout=600.0)
                    
                elif routing_engine == "omnivoice":
                    payload = {
                        "model": "omnivoice-cpp",
                        "input": chunk_text,
                        "voice": req.voice,
                        "language": "en-US" if is_english else req.language,
                        "custom_voice_prompt": req.custom_voice_prompt,
                        "params": {
                            "seed": 42,
                            "fidelity": fidelity_float,
                            "speed": req.speed,
                            "pitch": req.pitch,
                            "volume": req.volume,
                            "emotion": chunk_emotion,
                            "style": req.style
                        }
                    }
                    res = requests.post(f"http://127.0.0.1:{target_port}/v1/audio/speech", json=payload, timeout=600.0)
                    
                elif routing_engine == "fish":
                    payload = {
                        "text": chunk_text,
                        "reference_audio": reference_wav_path,
                        "expressiveness": expressiveness_float,
                        "language": "en-US" if is_english else req.language,
                        "emotion": chunk_emotion,
                        "style": req.style,
                        "speed": req.speed,
                        "pitch": req.pitch,
                        "voice": req.voice,
                        "reference_text": req.reference_text,
                        "volume": req.volume,
                        "custom_voice_prompt": req.custom_voice_prompt
                    }
                    res = requests.post(f"http://127.0.0.1:{target_port}/v1/audio/speech", json=payload, timeout=600.0)

                if res.status_code != 200:
                    raise HTTPException(
                        status_code=res.status_code, 
                        detail=f"Downstream service error: {res.text}"
                    )
                    
                if routing_engine == "voxcpm":
                    res_data = res.json()
                    file_path = res_data.get("file_path")
                    if not file_path or not os.path.exists(file_path):
                        raise HTTPException(status_code=500, detail="VoxCPM2 did not return a valid output file path.")
                    with open(file_path, 'rb') as f:
                        chunk_bytes = f.read()
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                else:
                    chunk_bytes = res.content
                    
                # Apply per-chunk emotion post-processing for real VoxCPM2 model
                if routing_engine == "voxcpm" and not is_mock_run:
                    chunk_bytes = apply_audio_postprocessing(
                        chunk_bytes,
                        speed=req.speed,
                        pitch=req.pitch,
                        volume=req.volume,
                        emotion=chunk_emotion,
                        style=req.style,
                        sample_rate=48000,
                        is_clone=bool(req.reference_audio)
                    )
            
            # Apply peak normalization to balance volumes across segments
            chunk_bytes = normalize_wav_volume(chunk_bytes, chunk_emotion)
            return chunk_bytes

        # Check target port once before parallel runs if not in mock mode
        if is_online or not req.mock_fallback:
            if not check_port(port):
                raise HTTPException(
                    status_code=503, 
                    detail=f"Local engine {req.engine_selection.upper()} is offline on port {port}."
                )

        from concurrent.futures import ThreadPoolExecutor
        
        # We only want to run the text segments in the ThreadPool
        text_indices = [i for i, s in enumerate(segments) if s["type"] == "text"]
        
        results = {}
        if text_indices:
            def worker(idx):
                return idx, process_text_segment(segments[idx])
                
            with ThreadPoolExecutor(max_workers=min(len(text_indices), 8)) as executor:
                futures = [executor.submit(worker, idx) for idx in text_indices]
                for fut in futures:
                    idx, chunk_bytes = fut.result()
                    results[idx] = chunk_bytes

        for i, seg in enumerate(segments):
            if seg["type"] == "text":
                chunk_bytes = results[i]
                segment_audios.append({
                    "type": "text",
                    "bytes": chunk_bytes
                })
                if not text_wav_for_header and chunk_bytes and chunk_bytes.startswith(b"RIFF"):
                    text_wav_for_header = chunk_bytes
            else:
                segment_audios.append({
                    "type": "break",
                    "duration_ms": seg["duration_ms"]
                })
                
        # Align silence audio attributes with generated audio characteristics
        sr = 48000 if engine == "voxcpm" else 24000
        channels = 1
        width = 2
        if text_wav_for_header:
            try:
                with wave.open(io.BytesIO(text_wav_for_header), "rb") as w:
                    sr = w.getframerate()
                    channels = w.getnchannels()
                    width = w.getsampwidth()
            except Exception as e:
                print(f"[SYSTEM] Error reading wave file header for silence alignment: {e}")
                
        wav_chunks = []
        for seg in segment_audios:
            if seg["type"] == "text":
                wav_chunks.append(seg["bytes"])
            else:
                silence_bytes = generate_silence_wav(seg["duration_ms"], sample_rate=sr, num_channels=channels, bits_per_sample=width*8)
                wav_chunks.append(silence_bytes)
                
        # Losslessly concatenate synthesized WAV chunks
        combined_wav_bytes = concatenate_wav_bytes(wav_chunks)
            
        # Convert to MP3 if required
        if req.format == "mp3":
            final_bytes = convert_wav_to_mp3(combined_wav_bytes)
            mime_type = "audio/mp3"
        else:
            final_bytes = combined_wav_bytes
            mime_type = "audio/wav"
  
        base64_audio = base64.b64encode(final_bytes).decode('utf-8')
        latency = (time.time() - start_time) * 1000
        
        if is_mock_run:
            info_msg = "Mock Fallback (Offline)"
            if routing_engine == "voxcpm" and has_voxcpm_local:
                info_msg += " [Autoconfigured VoxCPM2 local paths]"
            msg = f"Server on port {port} offline. {info_msg}"
        else:
            if routing_engine == "voxcpm" and engine != "voxcpm":
                msg = f"Synthesized via live VoxCPM2 model (routed from {engine.upper()})."
            else:
                msg = f"Synthesized via live {engine.upper()} model."
            if routing_engine == "voxcpm" and has_voxcpm_local:
                msg += " (Auto-configured using local model folder)"
            
        # Write to static folder so frontend can play same-origin audio file
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        output_filename = f"output_{engine}_{int(time.time())}.{req.format}"
        output_filepath = os.path.join(static_dir, output_filename)
        try:
            # Clean up old output files, keeping the last 50
            output_files = []
            for filename in os.listdir(static_dir):
                if filename.startswith("output_") and (filename.endswith(".wav") or filename.endswith(".mp3")):
                    filepath = os.path.join(static_dir, filename)
                    output_files.append((filepath, os.path.getmtime(filepath)))
            output_files.sort(key=lambda x: x[1])
            if len(output_files) >= 50:
                for i in range(len(output_files) - 49):
                    try:
                        os.remove(output_files[i][0])
                    except Exception:
                        pass

            with open(output_filepath, "wb") as f:
                f.write(final_bytes)
            audio_url = f"/{output_filename}"
        except Exception as e:
            print(f"[SYSTEM] Failed to write static audio file: {e}")
            audio_url = None
            
        return {
            "success": True,
            "audio": f"data:{mime_type};base64,{base64_audio}",
            "audio_url": audio_url,
            "engine": engine,
            "latency_ms": round(latency, 2),
            "mock": is_mock_run,
            "message": msg
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502, 
            detail=f"Failed to communicate with local {engine.upper()} engine on port {port}: {str(e)}"
        )
    finally:
        # Clean up temporary file to prevent disk fill-up, keeping permanent preset voice reference assets
        if reference_wav_path and os.path.exists(reference_wav_path) and not is_dummy_preset:
            # Do NOT delete if it is a permanent preset or output file (stored in presets/ or output_...)
            if "static/presets" not in reference_wav_path and "presets/" not in reference_wav_path and "output_" not in reference_wav_path:
                try:
                    os.remove(reference_wav_path)
                except Exception as e:
                    print(f"[SYSTEM] Failed to clean up temp reference file: {e}")

# Pydantic Schemas for new endpoints
class ActivateRequest(BaseModel):
    license_key: str



class MergeRequest(BaseModel):
    files: list[str]



@app.get("/api/license/status")
async def get_license_status():
    is_valid, hwid, expiry, msg = license_verify.check_local_license()
    
    # If the local license is cryptographically valid, check if it was revoked online
    if is_valid:
        try:
            lic_file = license_verify.get_license_file_path()
            with open(lic_file, "r") as f:
                lic_key = f.read().strip()
            
            # Query Google Sheets
            is_blocked, online_msg = license_verify.check_online_status(lic_key)
            if is_blocked:
                # Local license has been blacklisted online! Delete it
                print(f"[LICENSING] Key revoked online. Deleting local license: {online_msg}")
                if os.path.exists(lic_file):
                    os.remove(lic_file)
                # Also delete legacy license file if exists in current directory
                if os.path.exists("license.lic"):
                    os.remove("license.lic")
                return {
                    "status": "inactive",
                    "hwid": hwid,
                    "expiry": expiry,
                    "message": online_msg
                }
        except Exception as e:
            print(f"[LICENSING] Online status verification warning: {e}")
            
    return {
        "status": "active" if is_valid else "inactive",
        "hwid": hwid,
        "expiry": expiry,
        "message": msg
    }

@app.post("/api/license/activate")
async def activate_license(req: ActivateRequest):
    is_valid, expiry, msg = license_verify.verify_license(req.license_key)
    if is_valid:
        lic_file = license_verify.get_license_file_path()
        with open(lic_file, "w") as f:
            f.write(req.license_key.strip())
        return {"success": True, "message": "Activation successful!", "expiry": expiry}
    else:
        return {"success": False, "message": f"Activation failed: {msg}"}



@app.post("/api/merge")
async def merge_audio_files(req: MergeRequest):
    is_valid, _, _, msg = license_verify.check_local_license()
    if not is_valid:
        raise HTTPException(status_code=403, detail=f"Unlicensed Application: {msg}")
    try:
        if not req.files:
            raise HTTPException(status_code=400, detail="No files selected for merging.")
            
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        wav_chunks = []
        
        for file_url in req.files:
            filename = os.path.basename(file_url)
            filepath = os.path.join(static_dir, filename)
            if not os.path.exists(filepath):
                presets_path = os.path.join(static_dir, "presets", filename)
                if os.path.exists(presets_path):
                    filepath = presets_path
                else:
                    raise HTTPException(status_code=404, detail=f"Audio file not found: {filename}")
            with open(filepath, "rb") as f:
                wav_chunks.append(f.read())
                
        if not wav_chunks:
            raise HTTPException(status_code=400, detail="No audio data was loaded to merge.")
            
        merged_bytes = concatenate_wav_bytes(wav_chunks)
        
        output_filename = f"output_merged_{int(time.time())}.wav"
        output_filepath = os.path.join(static_dir, output_filename)
        
        with open(output_filepath, "wb") as f:
            f.write(merged_bytes)
            
        return {
            "success": True,
            "audio_url": f"/{output_filename}",
            "message": "Merged successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
def api_transcribe(req: TranscribeRequest):
    is_valid, _, _, msg = license_verify.check_local_license()
    if not is_valid:
        raise HTTPException(status_code=403, detail=f"Unlicensed Application: {msg}")
    # Check ffmpeg availability
    import shutil
    if not shutil.which("ffmpeg"):
        msg_en = "ffmpeg binary is not found on your system PATH. Please install ffmpeg first (on macOS: run 'brew install ffmpeg' in Terminal; on Windows: download from ffmpeg.org and add to PATH)."
        msg_km = "រកមិនឃើញកម្មវិធី ffmpeg នៅក្នុងម៉ាស៊ីនរបស់អ្នកឡើយ។ សូមដំឡើង ffmpeg ជាមុនសិន (នៅលើ macOS: វាយពាក្យ 'brew install ffmpeg' ក្នុង Terminal; នៅលើ Windows: ទាញយកពី ffmpeg.org រួចបញ្ចូលទៅក្នុង PATH)។"
        raise HTTPException(status_code=400, detail=f"{msg_en} || {msg_km}")

    try:
        if req.engine == "qwen":
            app.state.transcribe_engine = "qwen"
            app.state.transcribe_progress = 0.0
            app.state.transcribe_status = "Verifying dependencies..."
            
            # 1. Verify/install qwen-asr
            try:
                import torch
                from qwen_asr import Qwen3ASRModel
            except ImportError:
                app.state.transcribe_status = "Installing missing qwen-asr package..."
                print("[SYSTEM] qwen-asr package missing. Installing...")
                import subprocess
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "qwen-asr"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                import torch
                from qwen_asr import Qwen3ASRModel

            # 2. Decode base64 audio and save to temporary file
            import uuid
            ext = os.path.splitext(req.filename)[1] or ".wav"
            temp_filename = f"temp_transcribe_{uuid.uuid4().hex}{ext}"
            temp_path = os.path.abspath(temp_filename)
            
            base64_str = req.audio_base64
            if base64_str.startswith("data:"):
                header, base64_data = base64_str.split(",", 1)
            else:
                base64_data = base64_str
            audio_bytes = base64.b64decode(base64_data)
            
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)

            try:
                # Check cache for model
                hf_cache = os.path.expanduser("~/.cache/huggingface/hub")
                model_cache_folder = os.path.join(hf_cache, "models--seanghay--Qwen3-ASR-0.6B-Khmer")
                if not os.path.exists(model_cache_folder):
                    app.state.transcribe_status = "Downloading Khmer Transcrip model (~1.2GB)... Please wait."
                else:
                    app.state.transcribe_status = "Loading Khmer Transcrip model into memory..."

                print(f"[SYSTEM] Transcribing {req.filename} using local Khmer Transcrip model...")
                
                device = "cpu"
                if torch.cuda.is_available():
                    device = "cuda:0"
                elif torch.backends.mps.is_available():
                    device = "mps"

                model = Qwen3ASRModel.from_pretrained(
                    "seanghay/Qwen3-ASR-0.6B-Khmer",
                    dtype=torch.float16 if device == "mps" else torch.bfloat16,
                    device_map=device,
                    max_new_tokens=512
                )
                app.state.transcribe_status = "Transcribing audio chunks..."
                
                import soundfile as sf
                import numpy as np
                
                # Read audio data
                data, samplerate = sf.read(temp_path)
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)
                    
                duration = len(data) / samplerate
                print(f"[SYSTEM] Total duration: {duration:.2f} seconds. Chunking...")
                
                chunk_duration = 20.0 # 20 seconds chunks
                chunk_samples = int(chunk_duration * samplerate)
                total_samples = len(data)
                
                total_chunks = int(np.ceil(total_samples / chunk_samples))
                if total_chunks == 0:
                    total_chunks = 1
                    
                segments = []
                
                for idx in range(total_chunks):
                    start_idx = idx * chunk_samples
                    end_idx = min(start_idx + chunk_samples, total_samples)
                    
                    chunk_data = data[start_idx:end_idx]
                    
                    # Save chunk to temp file
                    chunk_filename = f"temp_chunk_{uuid.uuid4().hex}.wav"
                    chunk_path = os.path.abspath(chunk_filename)
                    sf.write(chunk_path, chunk_data, samplerate)
                    
                    try:
                        results = model.transcribe(audio=chunk_path)
                        chunk_text = results[0].text if results else ""
                        if chunk_text.strip():
                            segments.append({
                                "start": idx * chunk_duration,
                                "end": min((idx + 1) * chunk_duration, duration),
                                "text": chunk_text.strip()
                            })
                    finally:
                        if os.path.exists(chunk_path):
                            os.remove(chunk_path)
                            
                    # Update progress
                    app.state.transcribe_progress = float(int(((idx + 1) / total_chunks) * 100))
                    print(f"[SYSTEM] Transcribing: {app.state.transcribe_progress:.0f}% complete ({idx+1}/{total_chunks} chunks)")
                
                # Format conversion
                formatted_result = ""
                if req.output_format == "srt":
                    lines = []
                    for s_idx, seg in enumerate(segments, start=1):
                        start = format_srt_time(seg["start"])
                        end = format_srt_time(seg["end"])
                        text = seg["text"]
                        lines.append(f"{s_idx}\n{start} --> {end}\n{text}\n")
                    formatted_result = "\n".join(lines)
                elif req.output_format == "lrc":
                    lines = []
                    for seg in segments:
                        time_tag = format_lrc_time(seg["start"])
                        text = seg["text"]
                        lines.append(f"{time_tag} {text}")
                    formatted_result = "\n".join(lines)
                else: # txt
                    formatted_result = " ".join([seg["text"] for seg in segments])
                    
            finally:
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
                app.state.transcribe_progress = 100.0

            return JSONResponse(content={
                "status": "success",
                "text": formatted_result,
                "filename": f"{os.path.splitext(req.filename)[0]}.{req.output_format}",
                "engine_used": "qwen"
            })

        app.state.transcribe_engine = "whisper"
        app.state.transcribe_progress = 0.0
        
        # 1. Verify/install whisper
        try:
            import whisper
        except ImportError:
            print("[SYSTEM] Whisper package missing. Installing local openai-whisper...")
            import subprocess
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "openai-whisper"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            import whisper

        # 2. Decode base64 audio and save to temporary file
        import uuid
        ext = os.path.splitext(req.filename)[1] or ".wav"
        temp_filename = f"temp_transcribe_{uuid.uuid4().hex}{ext}"
        temp_path = os.path.abspath(temp_filename)
        
        base64_str = req.audio_base64
        if base64_str.startswith("data:"):
            header, base64_data = base64_str.split(",", 1)
        else:
            base64_data = base64_str
        audio_bytes = base64.b64decode(base64_data)
        
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)

        # 3. Load local model and transcribe
        import torch
        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
            
        # Check cache for model
        cache_dir = os.path.expanduser("~/.cache/whisper")
        model_file = os.path.join(cache_dir, f"{req.model_size}.pt")
        if req.model_size == "large-v3":
            model_file = os.path.join(cache_dir, "large-v3.pt")
            
        if not os.path.exists(model_file):
            app.state.transcribe_status = f"Downloading Whisper {req.model_size} model (~{get_model_size_desc(req.model_size)})... Please wait."
        else:
            app.state.transcribe_status = f"Loading Whisper {req.model_size} model into memory..."

        print(f"[SYSTEM] Transcribing {req.filename} using local Whisper {req.model_size} model on {device} (language: {req.language})...")
        model = whisper.load_model(req.model_size, device=device)
        app.state.transcribe_status = "Transcribing audio..."
        
        transcribe_opts = {
            "temperature": 0.0,
            "beam_size": 5,
            "best_of": 5,
            "fp16": False  # Disable FP16 to prevent crashes/stuck loops on CPU/MPS
        }
        if req.language and req.language != "auto":
            transcribe_opts["language"] = req.language
            if req.language == "km":
                transcribe_opts["initial_prompt"] = "សូមសរសេរជាអក្សរខ្មែរ និងភាសាខ្មែរ៖ ខ្ញុំបាទ នាងខ្ញុំ សួស្តី បងប្អូន អាជីវកម្ម ដៃគូ"
            elif req.language == "en":
                transcribe_opts["initial_prompt"] = "Hello, welcome. This is a transcription in English."
        
        result = model.transcribe(temp_path, **transcribe_opts)
        segments = result.get("segments", [])

        # 4. Clean up temp audio file
        try:
            os.remove(temp_path)
        except Exception:
            pass

        # 5. Format conversion
        formatted_result = ""
        if req.output_format == "srt":
            lines = []
            for idx, seg in enumerate(segments, start=1):
                start = format_srt_time(seg["start"])
                end = format_srt_time(seg["end"])
                text = seg["text"].strip()
                lines.append(f"{idx}\n{start} --> {end}\n{text}\n")
            formatted_result = "\n".join(lines)
        elif req.output_format == "lrc":
            lines = []
            for seg in segments:
                time_tag = format_lrc_time(seg["start"])
                text = seg["text"].strip()
                lines.append(f"{time_tag} {text}")
            formatted_result = "\n".join(lines)
        else: # txt
            formatted_result = "\n".join([seg["text"].strip() for seg in segments])

        return JSONResponse(content={
            "status": "success",
            "text": formatted_result,
            "filename": f"{os.path.splitext(req.filename)[0]}.{req.output_format}",
            "engine_used": "whisper"
        })

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[SYSTEM] Transcribe exception: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def format_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_lrc_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    centis = int((seconds % 1) * 100)
    return f"[{minutes:02d}:{secs:02d}.{centis:02d}]"

CURRENT_VERSION = "1.2.2"
VERSION_CHECK_URL = "https://raw.githubusercontent.com/mooncry93/TTS-ATUO-UPDATE/main/UPDATE%20RELEASE/version.json"

@app.get("/api/check-update")
async def check_update_endpoint():
    try:
        import requests
        res = requests.get(VERSION_CHECK_URL, timeout=5.0)
        if res.status_code == 200:
            data = res.json()
            online_version = data.get("version", "1.0.0")
            download_url = data.get("download_url", "")
            changelog = data.get("changelog", "")
            
            # Simple version comparison helper
            def parse_ver(v):
                return [int(x) for x in v.split(".") if x.isdigit()]
                
            local_parsed = parse_ver(CURRENT_VERSION)
            online_parsed = parse_ver(online_version)
            
            update_available = online_parsed > local_parsed
            
            return {
                "update_available": update_available,
                "current_version": CURRENT_VERSION,
                "online_version": online_version,
                "download_url": download_url,
                "changelog": changelog
            }
        else:
            return {"update_available": False, "message": "Failed to fetch version info from server."}
    except Exception as e:
        return {"update_available": False, "message": str(e)}

static_dir = resolve_path("static")
os.makedirs(static_dir, exist_ok=True)

# Mount Static Files (after routing definitions)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
