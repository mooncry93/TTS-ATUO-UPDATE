VoxCPM2 Portable GUI

1) របៀបដំណើរការ
  - ចុច `start_voxcpm2_gui.bat`
  - បញ្ចូលអត្ថបទ (Khmer/English)
  - ជ្រើស Output (.wav ឬ .mp3)
  - (Optional) Reference audio + Prompt text
  - ចុច Generate

2) ត្រូវ install អីថែមអត់?
  - មិនចាំបាច់ install Python ឬ package ថែមទេ (Portable folder មាន `voxcpm_runtime\python.exe` រួច)
  - ត្រូវមាន GPU + NVIDIA driver ប្រសើរជាង (Auto/CUDA), តែអាចរត់ CPU បាន (យឺតខ្លាំង)

3) Folder structure ត្រូវមាន (នៅក្នុង folder នេះ)
  - VoxCPM2_GUI.py
  - start_voxcpm2_gui.bat
  - ffmpeg.exe
  - VoxCPM-main\src\voxcpm\...
  - models\openbmb__VoxCPM2\...
  - voxcpm_runtime\python.exe

4) ចំណាំ
  - ប្រសិនបើចង់ .mp3 ត្រូវមាន `ffmpeg.exe` នៅជិត script នេះ។
  - បើ error “missing required files/folders” គឺ Copy folder មិនគ្រប់។

