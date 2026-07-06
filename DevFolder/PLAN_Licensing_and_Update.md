# Plan for Licensing and Auto-Update System

This document was created by your AI assistant to save the plan we discussed. When you are ready to implement this, just copy the prompt at the bottom of this file and paste it into the AI chat!

## 1. Licensing System (Hardware Binding + Cryptography)
We will protect the app from being freely shared by:
- **HWID Lock:** Generating a unique Hardware ID based on the user's PC.
- **Crypto Keys:** Using Private/Public RSA keys so hackers cannot create fake Keygens.
- **Online Validation (Google Sheets/Firebase):** Storing active/cancelled keys online so you can revoke access at any time.
- **Obfuscation:** Compiling Python (`.py`) files to C extensions (`.pyd`/`.so`) or `.exe` so nobody can read or delete the license check code.

## 2. Auto-Update System (via GitHub)
We will make it easy for your clients to update to new versions:
- **Version Check:** The app will read a `version.txt` from your GitHub.
- **Zip Download:** The app will download `Update_vX.X.zip` from your GitHub Releases.
- **Build Script:** We will create a `build_update.py` script for you. When you run it, it will automatically zip the correct files (Python code, HTML) while ignoring the heavy models (`models/`) and user data (`static/presets/`).

---

## 🚀 How to resume this work later:
When you are ready to build this, start a new chat with me and paste this exact message:

> **"Hello! I am ready to implement the Licensing System and the Auto-Update System for my TTS app as outlined in the `PLAN_Licensing_and_Update.md` file. Let's start step-by-step, beginning with the Hardware ID and License Key Generator."**
