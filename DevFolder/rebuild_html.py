import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to extract the 3 main parts:
# 1. Editor (lines 64-118 approx)
# 2. Player (lines 120-157 approx)
# 3. Settings (lines 160-550 approx)

# It's easier to just replace the entire studio-workspace div
start_idx = html.find('<div class="studio-workspace">')
end_idx = html.find('<!-- HISTORY VIEW -->')

top_html = html[:start_idx]
bottom_html = html[end_idx:]

new_workspace = """
<div class="studio-layout-v2">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar-panel">
        <h2 class="sidebar-title"><i class="fa-solid fa-sliders"></i> Configuration</h2>
        
        <div class="config-section">
            <label>Language</label>
            <select class="custom-select" id="select-language">
                <option value="km-KH">km-KH (Khmer)</option>
                <option value="en-US">en-US (English)</option>
            </select>
        </div>
        
        <div class="config-section">
            <label>Voice Profile</label>
            <select class="custom-select" id="select-voice">
                <option value="default">Default Voice</option>
                <option value="sokha">Sokha (Male)</option>
                <option value="sreypich">Sreypich (Female)</option>
                <option value="sokly">Sokly (Female)</option>
            </select>
        </div>
        
        <div class="config-section">
            <label>Voice Cloning</label>
            <select class="custom-select" id="select-cloned-voices">
                <option value="none">No clone reference (standard)</option>
                <option value="voice1">Sinn Sisamouth Clone</option>
                <option value="voice2">Ros Serey Sothea Clone</option>
                <option value="voice3">News Anchor Male</option>
                <option value="voice4">News Anchor Female</option>
            </select>
            <div class="drop-zone mt-2" id="audio-dropzone">
                <i class="fa-solid fa-cloud-arrow-up"></i>
                <p>Drag reference audio here</p>
                <input type="file" id="reference-audio-file" accept="audio/wav,audio/mp3,audio/m4a" class="hidden">
            </div>
            <div class="file-loaded hidden mt-2" id="file-loaded-info">
                <span id="loaded-file-name" style="font-size:0.8rem;color:#ccc;"></span>
                <button id="btn-remove-audio" style="background:none;border:none;color:red;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
        </div>

        <div class="config-section">
            <label>Expressiveness</label>
            <input type="range" class="accordion-slider" id="input-expressiveness" min="0" max="100" value="50">
            <label class="mt-2">Style Strength</label>
            <input type="range" class="accordion-slider" id="input-style" min="0" max="100" value="50">
            <label class="mt-2">Fidelity</label>
            <input type="range" class="accordion-slider" id="input-fidelity" min="0" max="100" value="75">
        </div>
        
        <div class="config-section">
            <label>Speed</label>
            <input type="range" class="accordion-slider" id="input-speed" min="0.5" max="2.0" step="0.1" value="1.0">
            <label class="mt-2">Pitch</label>
            <input type="range" class="accordion-slider" id="input-pitch" min="-10" max="10" step="1" value="0">
        </div>
    </aside>

    <!-- CENTER EDITOR -->
    <main class="center-panel">
        <div class="editor-wrapper">
            <textarea id="text-input" placeholder="Type or paste your script here..."></textarea>
            
            <div class="emotion-dock">
                <span>Emotion Tags:</span>
                <button class="btn-emotion-tag" data-tag="[neutral]">[neutral]</button>
                <button class="btn-emotion-tag" data-tag="[happy]">[happy]</button>
                <button class="btn-emotion-tag" data-tag="[excited]">[excited]</button>
                <button class="btn-emotion-tag" data-tag="[angry]">[angry]</button>
                <button class="btn-emotion-tag" data-tag="[calm]">[calm]</button>
                <button class="btn-emotion-tag" data-tag="[rough]">[rough]</button>
                <button class="btn-emotion-tag" data-tag="[soft]">[soft]</button>
                <button class="btn-emotion-tag" data-tag="[serious]">[serious]</button>
            </div>
            
            <div class="editor-stats">
                <span id="char-count">0</span> chars | <span id="word-count">0</span> words
                <button id="btn-clear-text" class="btn-clear"><i class="fa-solid fa-trash"></i></button>
            </div>
            
            <button class="btn-generate-speech-large" id="btn-generate">
                <span class="btn-content"><i class="fa-solid fa-bolt"></i> Generate</span>
                <div class="btn-loader hidden"><div class="spinner"></div></div>
            </button>
        </div>
    </main>

    <!-- BOTTOM DOCK -->
    <footer class="bottom-dock">
        <div class="player-controls">
            <button class="btn-play-pause disabled" id="btn-play-pause"><i class="fa-solid fa-play"></i></button>
            <span id="current-time">0:00</span>
            <div class="progress-bar-wrapper" id="progress-bar-container">
                <div class="progress-bar-fill" id="progress-bar-fill"></div>
            </div>
            <span id="total-time">0:00</span>
            <i class="fa-solid fa-volume-high" style="margin-left:15px;color:#aaa;"></i>
            <input type="range" id="volume-slider" min="0" max="1" step="0.05" value="0.8" style="width:80px;">
            <button class="btn-download-audio disabled" id="btn-download" style="margin-left:auto;"><i class="fa-solid fa-download"></i></button>
        </div>
        <div class="visualizer-container">
            <canvas id="waveform-canvas"></canvas>
        </div>
    </footer>
</div>
</div> <!-- Close #studio-view -->
"""

final_html = top_html + new_workspace + bottom_html

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Rebuilt index.html with new layout")
