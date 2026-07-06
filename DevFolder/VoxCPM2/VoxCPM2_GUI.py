# -*- coding: utf-8 -*-
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

APP_TITLE = "VoxCPM2 (Portable GUI - PyQt5)"
APP_VERSION = "1.0.1"
GITHUB_REPO = "YOUR_USERNAME/YOUR_REPO"  # Change to your actual repository path
VERSION_JSON_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/version.json"

DEFAULT_CFG = "2.0"
DEFAULT_TIMESTEPS = "10"

PROMPT_PRESETS = {
    "Female (Khmer)": "adult Khmer female speaker, beautiful pleasant feminine woman voice, warm smooth tone, clear natural Cambodian Khmer pronunciation, studio quality, gentle and expressive",
    "Male (Khmer)": "adult Khmer male speaker, handsome pleasant masculine man voice, warm smooth deeper tone, clear natural Cambodian Khmer pronunciation, studio quality, confident and expressive",
    "Girl (Khmer)": "young Khmer female child speaker, cute pleasant girl voice, bright smooth feminine child tone, clear natural Cambodian Khmer pronunciation, studio quality",
    "Boy (Khmer)": "young Khmer male child speaker, cute pleasant boy voice, bright smooth masculine child tone, clear natural Cambodian Khmer pronunciation, studio quality",
    "Old Woman (Khmer)": "elderly Khmer female speaker, pleasant old woman voice, warm mature feminine tone, clear natural Cambodian Khmer pronunciation, studio quality, gentle and expressive",
    "Old Man (Khmer)": "elderly Khmer male speaker, pleasant old man voice, warm mature deeper masculine tone, clear natural Cambodian Khmer pronunciation, studio quality, calm and expressive",
    "Custom": "",
}


def _app_dir():
    return os.path.dirname(os.path.abspath(__file__))


def _paths():
    root = _app_dir()
    return {
        "root": root,
        "source_src": os.path.join(root, "VoxCPM-main", "src"),
        "model_dir": os.path.join(root, "models", "openbmb__VoxCPM2"),
        "python_exe": os.path.join(root, "voxcpm_runtime", "python.exe"),
        "ffmpeg_exe": os.path.join(root, "ffmpeg.exe"),
    }


def _validate_install():
    p = _paths()
    missing = []
    if not os.path.isdir(p["source_src"]):
        missing.append(p["source_src"])
    if not os.path.isdir(p["model_dir"]):
        missing.append(p["model_dir"])
    if not os.path.exists(p["python_exe"]):
        missing.append(p["python_exe"])
    if not os.path.exists(p["ffmpeg_exe"]):
        missing.append(p["ffmpeg_exe"])
    return missing


def _safe_int(value, default_value):
    try:
        return int(str(value).strip())
    except Exception:
        return default_value


def _safe_float(value, default_value):
    try:
        return float(str(value).strip())
    except Exception:
        return default_value


def _build_external_script():
    return (
        "import json, os, sys, random; "
        "p=json.load(open(sys.argv[1], encoding='utf-8')); "
        "seed=int(p.get('seed', 0)) & 0x7fffffff; "
        "random.seed(seed); "
        "sys.path.insert(0, p['source_src']); "
        "import numpy as np; np.random.seed(seed); "
        "import torch; torch.manual_seed(seed); "
        "torch.cuda.manual_seed_all(seed) if torch.cuda.is_available() else None; "
        "from voxcpm import VoxCPM; "
        "import soundfile as sf; "
        "m=VoxCPM.from_pretrained(p['model_id'], load_denoiser=False, "
        "local_files_only=os.path.isdir(p['model_id']), optimize=True, device=p.get('device', 'auto')); "
        "kw={'text':p['text'],'cfg_value':p['cfg_value'],"
        "'inference_timesteps':p['inference_timesteps'],'normalize':False}; "
        "ref=p.get('reference_audio_path') or ''; "
        "pt=(p.get('prompt_text') or '').strip(); "
        "kw.update({'reference_wav_path':ref}) if ref and os.path.exists(ref) else None; "
        "kw.update({'prompt_wav_path':ref,'prompt_text':pt}) if ref and os.path.exists(ref) and pt else None; "
        "w=m.generate(**kw); "
        "sf.write(p['output'], w, m.tts_model.sample_rate)"
    )


try:
    from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore
except Exception:
    # Keep this file importable even when PyQt5 is not installed.
    raise RuntimeError(
        "PyQt5 is not installed in this portable runtime.\n\n"
        "To enable this GUI, install PyQt5 into voxcpm_runtime, for example:\n"
        "  voxcpm_runtime\\python.exe -m pip install PyQt5\n"
        "(Requires internet or offline wheels.)"
    )


class Worker(QtCore.QThread):
    log = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    done = QtCore.pyqtSignal(str)

    def __init__(
        self,
        text,
        output_path,
        cfg_value,
        timesteps,
        seed_value,
        device,
        reference_audio,
        prompt_text,
        parent=None,
    ):
        super().__init__(parent)
        self.text = text
        self.output_path = output_path
        self.cfg_value = cfg_value
        self.timesteps = timesteps
        self.seed_value = seed_value
        self.device = device
        self.reference_audio = reference_audio
        self.prompt_text = prompt_text
        self._stop_requested = False
        self._proc = None

    def request_stop(self):
        self._stop_requested = True
        try:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
        except Exception:
            pass

    def _emit(self, msg):
        self.log.emit(msg)

    def run(self):
        try:
            missing = _validate_install()
            if missing:
                raise RuntimeError("Missing required files/folders:\n" + "\n".join(missing))

            out_ext = os.path.splitext(self.output_path)[1].lower()
            if out_ext not in {".wav", ".mp3"}:
                raise RuntimeError("Output must be .wav or .mp3")

            p = _paths()
            request_fd, request_path = tempfile.mkstemp(suffix=".json")
            os.close(request_fd)

            tmp_fd, tmp_wav = tempfile.mkstemp(suffix=".wav")
            os.close(tmp_fd)
            final_wav = self.output_path if out_ext == ".wav" else tmp_wav

            try:
                payload = {
                    "source_src": p["source_src"],
                    "model_id": p["model_dir"],
                    "text": self.text,
                    "output": final_wav,
                    "cfg_value": float(self.cfg_value),
                    "inference_timesteps": int(self.timesteps),
                    "device": self.device,
                    "seed": int(self.seed_value) if self.seed_value is not None else int(time.time()) & 0x7FFFFFFF,
                    "reference_audio_path": self.reference_audio,
                    "prompt_text": self.prompt_text,
                }
                with open(request_path, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False)

                env = os.environ.copy()
                env["PYTHONPATH"] = os.pathsep.join([p["source_src"], env.get("PYTHONPATH", "")]).strip(os.pathsep)
                script = _build_external_script()

                self._emit("Starting VoxCPM2 generation...")
                start = time.time()
                self._proc = subprocess.Popen(
                    [p["python_exe"], "-c", script, request_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )

                last_ping = 0
                while self._proc.poll() is None:
                    if self._stop_requested:
                        self._emit("Stop requested. Terminating subprocess (best effort)...")
                        try:
                            self._proc.terminate()
                        except Exception:
                            pass
                        break
                    elapsed = int(time.time() - start)
                    if elapsed - last_ping >= 5:
                        last_ping = elapsed
                        self._emit(f"Working... ({elapsed}s)")
                    time.sleep(0.25)

                out = ""
                try:
                    out = self._proc.stdout.read() if self._proc.stdout else ""
                except Exception:
                    out = ""

                if self._proc.returncode != 0:
                    raise RuntimeError((out or "").strip() or f"VoxCPM2 failed with code {self._proc.returncode}")

                if not os.path.exists(final_wav) or os.path.getsize(final_wav) < 100:
                    raise RuntimeError("VoxCPM2 did not create a usable wav file.")

                if out_ext == ".mp3":
                    self._emit("Converting WAV -> MP3...")
                    ffmpeg = p["ffmpeg_exe"]
                    cmd = [ffmpeg, "-y", "-i", final_wav, "-vn", "-b:a", "192k", self.output_path]
                    r = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                    )
                    if r.returncode != 0 or not os.path.exists(self.output_path):
                        raise RuntimeError((r.stdout or "").strip() or "ffmpeg conversion failed")

                self._emit("Done.")
                self.done.emit(self.output_path)
            finally:
                try:
                    if os.path.exists(request_path):
                        os.remove(request_path)
                except Exception:
                    pass
                try:
                    if os.path.exists(tmp_wav):
                        os.remove(tmp_wav)
                except Exception:
                    pass
        except Exception as exc:
            self.error.emit(str(exc))


class DownloadThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)

    def __init__(self, url, dest_path):
        super().__init__()
        self.url = url
        self.dest_path = dest_path

    def run(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                total_size = int(response.info().get('Content-Length', 0))
                bytes_downloaded = 0
                block_size = 8192
                with open(self.dest_path, 'wb') as f:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        f.write(buffer)
                        bytes_downloaded += len(buffer)
                        if total_size > 0:
                            percent = int((bytes_downloaded / total_size) * 100)
                            self.progress.emit(percent)
            self.finished.emit(self.dest_path)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1000, 700)

        self.worker = None

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)

        layout.addWidget(QtWidgets.QLabel("Text to Speak (Khmer/English):"))
        self.text_box = QtWidgets.QPlainTextEdit()
        self.text_box.setPlaceholderText("Enter text...")
        layout.addWidget(self.text_box)

        form = QtWidgets.QFormLayout()
        layout.addLayout(form)

        # Output
        out_row = QtWidgets.QHBoxLayout()
        self.output_edit = QtWidgets.QLineEdit(os.path.join(_app_dir(), "output.wav"))
        out_btn = QtWidgets.QPushButton("Browse...")
        out_btn.clicked.connect(self.browse_output)
        out_row.addWidget(self.output_edit, 1)
        out_row.addWidget(out_btn)
        form.addRow("Output file:", out_row)

        # Preset
        preset_row = QtWidgets.QHBoxLayout()
        self.preset_combo = QtWidgets.QComboBox()
        self.preset_combo.addItems(list(PROMPT_PRESETS.keys()))
        self.preset_combo.setCurrentText("Female (Khmer)")
        self.preset_combo.currentTextChanged.connect(self.apply_preset)
        preset_row.addWidget(self.preset_combo)
        form.addRow("Prompt preset:", preset_row)

        self.prompt_edit = QtWidgets.QLineEdit(PROMPT_PRESETS.get("Female (Khmer)", ""))
        form.addRow("Prompt text (optional):", self.prompt_edit)

        # Reference
        ref_row = QtWidgets.QHBoxLayout()
        self.ref_edit = QtWidgets.QLineEdit("")
        ref_btn = QtWidgets.QPushButton("Browse...")
        ref_btn.clicked.connect(self.browse_reference)
        ref_row.addWidget(self.ref_edit, 1)
        ref_row.addWidget(ref_btn)
        form.addRow("Reference audio (optional):", ref_row)

        # Settings
        settings_row = QtWidgets.QHBoxLayout()
        self.cfg_edit = QtWidgets.QLineEdit(DEFAULT_CFG)
        self.cfg_edit.setFixedWidth(90)
        self.timesteps_edit = QtWidgets.QLineEdit(DEFAULT_TIMESTEPS)
        self.timesteps_edit.setFixedWidth(90)
        self.seed_edit = QtWidgets.QLineEdit("")
        self.seed_edit.setFixedWidth(120)
        self.device_combo = QtWidgets.QComboBox()
        self.device_combo.addItems(["auto", "cuda", "cpu"])
        settings_row.addWidget(QtWidgets.QLabel("CFG:"))
        settings_row.addWidget(self.cfg_edit)
        settings_row.addSpacing(12)
        settings_row.addWidget(QtWidgets.QLabel("Timesteps:"))
        settings_row.addWidget(self.timesteps_edit)
        settings_row.addSpacing(12)
        settings_row.addWidget(QtWidgets.QLabel("Seed:"))
        settings_row.addWidget(self.seed_edit)
        settings_row.addSpacing(12)
        settings_row.addWidget(QtWidgets.QLabel("Device:"))
        settings_row.addWidget(self.device_combo)
        settings_row.addStretch(1)
        form.addRow("Settings:", settings_row)

        # Buttons
        btn_row = QtWidgets.QHBoxLayout()
        self.gen_btn = QtWidgets.QPushButton("Generate")
        self.gen_btn.clicked.connect(self.start_generate)
        self.stop_btn = QtWidgets.QPushButton("Stop (best effort)")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_generate)
        open_btn = QtWidgets.QPushButton("Open Output Folder")
        open_btn.clicked.connect(self.open_output_folder)
        self.update_btn = QtWidgets.QPushButton("Check for Updates")
        self.update_btn.clicked.connect(self.check_for_updates)
        btn_row.addWidget(self.gen_btn)
        btn_row.addWidget(open_btn)
        btn_row.addWidget(self.update_btn)
        btn_row.addWidget(self.stop_btn)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

        layout.addWidget(QtWidgets.QLabel("Log:"))
        self.log_box = QtWidgets.QPlainTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box, 1)

        missing = _validate_install()
        if missing:
            self.log("Missing required files/folders:")
            for m in missing:
                self.log(f" - {m}")
            QtWidgets.QMessageBox.critical(
                self,
                APP_TITLE,
                "This portable folder is incomplete.\n\nMissing:\n" + "\n".join(missing),
            )

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log_box.appendPlainText(f"[{ts}] {msg}")

    def apply_preset(self, preset):
        if preset != "Custom":
            self.prompt_edit.setText(PROMPT_PRESETS.get(preset, ""))

    def browse_reference(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choose reference audio",
            "",
            "Audio files (*.wav *.mp3 *.m4a *.flac *.ogg);;All files (*.*)",
        )
        if path:
            self.ref_edit.setText(path)

    def browse_output(self):
        initial = self.output_edit.text().strip() or os.path.join(_app_dir(), "output.wav")
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save output audio",
            initial,
            "WAV audio (*.wav);;MP3 audio (*.mp3)",
        )
        if path:
            self.output_edit.setText(path)

    def open_output_folder(self):
        out_path = self.output_edit.text().strip()
        folder = os.path.dirname(out_path) if out_path else _app_dir()
        if folder and os.path.isdir(folder):
            try:
                os.startfile(folder)  # type: ignore[attr-defined]
            except Exception as exc:
                QtWidgets.QMessageBox.critical(self, APP_TITLE, f"Failed to open folder:\n{exc}")

    def _set_busy(self, busy):
        self.gen_btn.setEnabled(not busy)
        self.stop_btn.setEnabled(busy)

    def start_generate(self):
        if self.worker and self.worker.isRunning():
            QtWidgets.QMessageBox.warning(self, APP_TITLE, "Generation is already running.")
            return

        text = self.text_box.toPlainText().strip()
        if not text:
            QtWidgets.QMessageBox.warning(self, APP_TITLE, "Text is empty.")
            return

        output_path = self.output_edit.text().strip()
        if not output_path:
            QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please choose an output file.")
            return

        cfg_value = _safe_float(self.cfg_edit.text(), 2.0)
        timesteps = _safe_int(self.timesteps_edit.text(), 10)
        seed_text = self.seed_edit.text().strip()
        seed_value = _safe_int(seed_text, 0) if seed_text else None
        device = self.device_combo.currentText().strip() or "auto"
        reference_audio = self.ref_edit.text().strip()
        prompt_text = self.prompt_edit.text().strip()

        self.worker = Worker(
            text=text,
            output_path=output_path,
            cfg_value=cfg_value,
            timesteps=timesteps,
            seed_value=seed_value,
            device=device,
            reference_audio=reference_audio,
            prompt_text=prompt_text,
        )
        self.worker.log.connect(self.log)
        self.worker.error.connect(self.on_error)
        self.worker.done.connect(self.on_done)
        self._set_busy(True)
        self.log("Ready. Starting...")
        self.worker.start()

    def stop_generate(self):
        if self.worker and self.worker.isRunning():
            self.log("Stop requested.")
            self.worker.request_stop()

    def on_error(self, msg):
        self._set_busy(False)
        self.log(f"ERROR: {msg}")
        QtWidgets.QMessageBox.critical(self, APP_TITLE, msg)

    def on_done(self, out_path):
        self._set_busy(False)
        self.log("Success.")
        QtWidgets.QMessageBox.information(self, APP_TITLE, f"Audio generated:\n{out_path}")

    def check_for_updates(self):
        self.log("Checking for updates...")
        try:
            req = urllib.request.Request(VERSION_JSON_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            online_version = data.get("version", "1.0.0")
            download_url = data.get("download_url", "")
            changelog = data.get("changelog", "")
            
            if isinstance(changelog, list):
                changelog_text = "\n".join([f"- {item}" for item in changelog])
            else:
                changelog_text = str(changelog)
                
            def parse_ver(v):
                return [int(x) for x in v.strip().split('.') if x.isdigit()]
                
            if parse_ver(online_version) > parse_ver(APP_VERSION):
                self.log(f"New update available: Version {online_version}")
                reply = QtWidgets.QMessageBox.question(
                    self,
                    "Update Available",
                    f"A new version ({online_version}) is available!\n\n"
                    f"Changelog:\n{changelog_text}\n\n"
                    "Would you like to download and install it now?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )
                if reply == QtWidgets.QMessageBox.Yes:
                    self.download_and_install_update(download_url, online_version)
            else:
                self.log("You are running the latest version.")
                QtWidgets.QMessageBox.information(
                    self,
                    "No Update Available",
                    f"You are running the latest version (v{APP_VERSION})."
                )
        except Exception as e:
            self.log(f"Failed to check for updates: {e}")
            QtWidgets.QMessageBox.warning(
                self,
                "Update Check Failed",
                f"Failed to check for updates:\n{e}"
            )

    def download_and_install_update(self, download_url, new_version):
        if not download_url:
            QtWidgets.QMessageBox.warning(self, "Error", "Download URL is invalid.")
            return

        temp_dir = tempfile.gettempdir()
        dest_filename = f"setup_v{new_version}.exe"
        self.update_installer_path = os.path.join(temp_dir, dest_filename)

        self.progress_dialog = QtWidgets.QProgressDialog(
            "Downloading update...", "Cancel", 0, 100, self
        )
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(0)

        self.download_thread = DownloadThread(download_url, self.update_installer_path)
        self.download_thread.progress.connect(self.progress_dialog.setValue)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        
        self.progress_dialog.canceled.connect(self.download_thread.terminate)
        
        self.log(f"Downloading update from {download_url}...")
        self.download_thread.start()

    def on_download_finished(self, dest_path):
        self.log("Download completed successfully.")
        
        app_dir = os.path.abspath(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__))
        
        batch_content = (
            "@echo off\n"
            "timeout /t 2 /nobreak >nul\n"
            f"taskkill /f /im Digital_TTS_Studio.exe >nul 2>&1\n"
            f"taskkill /f /im gateway.exe >nul 2>&1\n"
            f'"{dest_path}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="{app_dir}"\n'
            "timeout /t 2 /nobreak >nul\n"
            f'start "" "{os.path.join(app_dir, "Digital_TTS_Studio.exe")}"\n'
            f"del %0\n"
        )
        
        batch_path = os.path.join(tempfile.gettempdir(), "update_installer.bat")
        try:
            with open(batch_path, "w", encoding="utf-8") as f:
                f.write(batch_content)
                
            self.log(f"Starting update installer: {batch_path}")
            subprocess.Popen(
                ["cmd.exe", "/c", batch_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.DETACHED_PROCESS
            )
            QtWidgets.QApplication.quit()
        except Exception as e:
            self.log(f"Failed to initiate update install: {e}")
            QtWidgets.QMessageBox.critical(self, "Update Error", f"Failed to start installer:\n{e}")

    def on_download_error(self, err_msg):
        self.log(f"Download failed: {err_msg}")
        QtWidgets.QMessageBox.critical(
            self,
            "Download Error",
            f"Failed to download the update:\n{err_msg}"
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

