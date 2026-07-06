; Inno Setup Script for Digital_TTS Studio
; Double-click this file in Inno Setup on Windows to compile into a single installer file.

[Setup]
AppName=Digital_TTS Studio
AppVersion=1.2.0
DefaultDirName={localappdata}\Digital_TTS_Studio
DefaultGroupName=Digital_TTS Studio
OutputDir=client
OutputBaseFilename=setup
DiskSpanning=no
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=app_icon.ico

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Copy all compiled executable dependencies and DLLs
Source: "dist\Digital_TTS_Studio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs nocompression

; Copy project source script files (EXCLUDING licensing & gateway to protect code)
Source: "*.py"; DestDir: "{app}"; Excludes: "gateway.py,license_verify.py"; Flags: ignoreversion
Source: "dist\gateway.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "UPDATE RELEASE\*"; DestDir: "{app}\UPDATE RELEASE"; Flags: recursesubdirs createallsubdirs ignoreversion

; Copy project shell scripts and batch files
Source: "*.bat"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "*.sh"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "*.command"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "master_keys.json"; DestDir: "{app}"; Flags: ignoreversion

; Copy preloaded VoxCPM2 framework files (EXCLUDING voxcpm_runtime, models, and ffmpeg)
Source: "VoxCPM2\VoxCPM-main\*"; DestDir: "{app}\VoxCPM2\VoxCPM-main"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "VoxCPM2\*.py"; DestDir: "{app}\VoxCPM2"; Flags: ignoreversion skipifsourcedoesntexist
Source: "VoxCPM2\*.bat"; DestDir: "{app}\VoxCPM2"; Flags: ignoreversion skipifsourcedoesntexist

; Copy user guide instructions
Source: "INSTALLATION_GUIDE.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Digital_TTS Studio"; Filename: "{app}\Digital_TTS_Studio.exe"
Name: "{autodesktop}\Digital_TTS Studio"; Filename: "{app}\Digital_TTS_Studio.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Digital_TTS_Studio.exe"; Description: "{cm:LaunchProgram,Digital_TTS Studio}"; Flags: nowait postinstall skipifsilent
