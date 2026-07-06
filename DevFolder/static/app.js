// --- Digital_TTS by MR.THY Client Logic ---

document.addEventListener("DOMContentLoaded", () => {
    // --- TRANSLATION CATALOGS ---
    const TRANSLATIONS = {
        en: {
            brand_name: "Digital_TTS by MR.THY",
            nav_home: "Home",
            nav_studio: "Studio",
            nav_history: "History",
            nav_settings: "Settings",
            studio_btn: "Studio",
            editor_title: "EDITOR",
            font_size_label: "Font Size:",
            stat_chars: "characters",
            stat_words: "words",
            btn_clear: "Clear",
            btn_generate: "Generate Speech",
            synthesizing_text: "Synthesizing...",
            output_title: "Generated Audio",
            btn_download: "Download",
            visualizer_label: "Acoustic Waveform Visualizer",
            engine_title: "TTS ENGINE",
            tab_voxcpm_sub: "Neural Khmer",
            tab_omnivoice_sub: "Khmer & English",
            tab_fish_sub: "Voice Cloning",
            connected_label: "Connected",
            running_mode: "Running Mode",
            local_port: "Local Port",
            drawer_language: "Language",
            drawer_voice: "Voice",
            drawer_cloning: "Clone a Voice (VoxCPM2)",
            drawer_emotions: "Emotion Controls",
            drawer_style: "Voice Style",
            drawer_speed: "Speed / Pitch / Volume",
            drawer_format: "Output Format",
            drawer_import: "File Import",
            drawer_batch: "Batch Processing",
            lbl_expressiveness: "Emotion Expression",
            lbl_strength: "Emotion Strength",
            lbl_fidelity: "Fidelity / Sound quality",
            lbl_speed: "Speed",
            lbl_pitch: "Pitch",
            lbl_volume: "Volume",
            voice_default: "Default Voice",
            voice_sokha: "Sokha (Male)",
            voice_sreypich: "Sreypich (Female)",
            voice_sokly: "Sokly (Female)",
            clone_none: "No clone reference (standard)",
            dropzone_desc: "Drag & drop 5-15s WAV reference clip here or browse files",
            ref_transcript_label: "Reference Transcript (Highly Recommended)",
            emo_neutral: "Normal",
            emo_happy: "Happy",
            emo_rough: "Rough",
            emo_excited: "Excited",
            emo_angry: "Angry",
            emo_calm: "Calm",
            emo_soft: "Soft/Loud",
            emo_serious: "Serious",
            style_default: "Default",
            style_news: "News / Broadcast",
            style_story: "Story / Narrate",
            style_chat: "Conversation",
            style_happy: "Happy / Excited",
            style_calm: "Calm",
            style_rough: "Rough",
            style_clerk: "Clerk",
            style_official: "Official",
            style_customer: "Customer Service",
            style_commercial: "Commercial",
            style_poetry: "Poetry",
            format_wav_sub: "Lossless - High quality",
            format_mp3_sub: "Compressed - Smaller file",
            import_preview: "Drag file",
            import_guide: "Drop file here or browse",
            batch_preview: "Inactive",
            btn_batch_start: "Start Batch Translation",
            mock_mode: "Mock Mode Fallback",
            emotion_guide: "Emotion controls let you fine-tune synthesis attributes. Adjust sliders to shape audio pitch variations.",
            voxcpm_desc: "Highly accurate neural Khmer TTS. Supports multiple speed, pitch, and voice styles. Zero-shot voice cloning capability is integrated using reference audio.",
            omnivoice_desc: "C++ optimized Discrete Non-AR single-stage text-to-acoustic GGUF weights. Exposing low-latency local execution on CPUs and consumer hardware.",
            fish_desc: "Zero-shot vocal cloning and fast streaming flow-matching engine. Exposes rapid parallel inference for multilingual voice replication.",
            settings_main_title: "System Settings & Configurations",
            settings_probe_title: "Unified Microservices Probe",
            settings_probe_desc: "Check active local ports for running model servers (VoxCPM2, OmniVoice, Fish Speech).",
            settings_probe_btn: "Probe Server Status",
            settings_cleanup_title: "Model Cache & Memory Cleanup",
            settings_cleanup_desc: "Clear GPU VRAM cache, run Python garbage collection, and purge temporary file uploads.",
            settings_cleanup_btn: "Purge VRAM Cache & Clean Files",
            settings_download_title: "VoxCPM2 Model Downloader",
            settings_download_desc: "Ensure all offline weights are fully loaded to local directories.",
            settings_download_btn: "Trigger Model Downloader",
            settings_lang_title: "Interface Language Selection",
            settings_lang_desc: "Select default localization for studio tooltips and menus.",
            settings_setup_title: "1-Click Super Setup & Calibrator",
            settings_setup_desc: "Configure environments, download model weights, and calibrate Python libraries for offline portability.",
            settings_setup_btn: "Run 1-Click Setup",
            settings_presets_title: "Voice Presets & Designed Profiles",
            settings_presets_desc: "Manage, review prompts/transcripts, and remove your custom designed voices and cloned presettings.",
            settings_designed_header: "Designed Voices",
            settings_cloned_header: "Cloned Presets",
            history_title: "Synthesis History",
            btn_clear_history_all: "Clear All History",
            history_empty_header: "No speech generated yet.",
            history_empty_desc: "Head to the Studio, type some text, and click \"Generate Speech\" to begin building your library.",
            console_title: "Host Activity Console",
            console_low_spec: "Low-Spec Mode",
            mode_local: "Local",
            offline_label: "Offline",
            btn_insert_pause: "Insert Pause",
            btn_ai_polish: "AI Polish",
            btn_voice_input: "Voice Dictate",
            btn_record_cloning: "Record Voice",
            btn_recording_stop: "Stop Recording",
            btn_merge_history: "Merge Selected",
            settings_lexicon_title: "Pronunciation Lexicon",
            settings_lexicon_desc: "Define acronyms or foreign words and their phonetic Khmer spellings (e.g. 'AI' -> 'អេអាយ').",
            nav_transcriber: "Transcriber",
            transcriber_title: "Local Audio Transcriber (Speech to Text)",
            transcriber_upload_title: "Upload Audio",
            transcriber_upload_desc: "Select an MP3 or WAV file to transcribe completely locally using OpenAI Whisper.",
            transcriber_config_title: "Configuration",
            whisper_model_label: "Whisper Model size",
            whisper_tiny_opt: "Tiny (Fast, ~75MB)",
            whisper_base_opt: "Base (Recommended, ~140MB)",
            whisper_small_opt: "Small (Better Khmer, ~460MB)",
            whisper_medium_opt: "Medium (High Accuracy, ~1.5GB)",
            whisper_large_opt: "Large V3 (Best Quality, ~3GB)",
            target_format_label: "Target Format",
            format_txt_opt: "Plain Text (.txt)",
            format_srt_opt: "Subtitles (.srt)",
            format_lrc_opt: "Song Lyrics (.lrc)",
            btn_start_transcribe: "Start Transcription",
            transcription_result_title: "Transcription Result",
            btn_copy_clipboard: "Copy to Clipboard",
            btn_save_file: "Save File",
            transcribe_language_label: "Language",
            lang_auto_opt: "Auto Detect",
            lang_km_opt: "Khmer (ខ្មែរ)",
            lang_en_opt: "English",
            transcribe_engine_label: "Transcription Engine",
            engine_whisper_opt: "Local Whisper (Offline)",
            engine_qwen_opt: "Khmer Transcrip (Local)"
        },
        km: {
            brand_name: "Digital_TTS by MR.THY",
            nav_home: "ទំព័រដើម",
            nav_studio: "ស្ទូឌីយោ",
            nav_history: "ប្រវត្តិ",
            nav_settings: "ការកំណត់",
            studio_btn: "ស្ទូឌីយោ",
            editor_title: "កម្មវិធីនិពន្ធ",
            font_size_label: "ទំហំអក្សរ:",
            stat_chars: "តួអក្សរ",
            stat_words: "ពាក្យ",
            btn_clear: "សម្អាត",
            btn_generate: "បង្កើតសំឡេង",
            synthesizing_text: "កំពុងបង្កើត...",
            output_title: "សំឡេងដែលបានបង្កើត",
            btn_download: "ទាញយក",
            visualizer_label: "រលកសំឡេង Visualizer",
            engine_title: "ក្បាលម៉ាស៊ីន TTS",
            tab_voxcpm_sub: "សរសៃប្រសាទខ្មែរ",
            tab_omnivoice_sub: "ខ្មែរ និង អង់គ្លេស",
            tab_fish_sub: "ចម្លងសំឡេង",
            connected_label: "ភ្ជាប់រួចរាល់",
            running_mode: "របៀបរត់",
            local_port: "ច្រកផ្លូវមូលដ្ឋាន",
            drawer_language: "ភាសា",
            drawer_voice: "សំឡេង",
            drawer_cloning: "ចម្លងសំឡេង (VoxCPM2)",
            drawer_emotions: "ការគ្រប់គ្រងអារម្មណ៍",
            drawer_style: "រចនាបថសំឡេង",
            drawer_speed: "ល្បឿន / កម្ពស់សំឡេង / កម្រិតសំឡេង",
            drawer_format: "ទ្រង់ទ្រាយលទ្ធផល",
            drawer_import: "នាំចូលឯកសារ",
            drawer_batch: "ដំណើរការជាក្រុម",
            lbl_expressiveness: "ការបញ្ចេញអារម្មណ៍",
            lbl_strength: "កម្រិតអារម្មណ៍",
            lbl_fidelity: "គុណភាពសំឡេង",
            lbl_speed: "ល្បឿន",
            lbl_pitch: "កម្ពស់សំឡេង",
            lbl_volume: "កម្រិតសំឡេង",
            voice_default: "សំឡេងលំនាំដើម",
            voice_sokha: "សុខា (ប្រុស)",
            voice_sreypich: "ស្រីពេជ្រ (ស្រី)",
            voice_sokly: "សុខលី (ស្រី)",
            clone_none: "គ្មានប្រភពចម្លង (ស្តង់ដារ)",
            dropzone_desc: "អូសនិងទម្លាក់ឯកសារសំឡេង 5-15 វិនាទីនៅទីនេះ ឬ រកមើលឯកសារ",
            ref_transcript_label: "អត្ថបទយោង (ណែនាំខ្លាំង)",
            emo_neutral: "ធម្មតា",
            emo_happy: "រីករាយ",
            emo_rough: "គ្រោត",
            emo_excited: "រំភើប",
            emo_angry: "ខឹង",
            emo_calm: "ស្ងប់",
            emo_soft: "ស្រទន់/ស្រែក",
            emo_serious: "ធ្ងន់ធ្ងរ",
            style_default: "លំនាំដើម",
            style_news: "ព័ត៌មាន / ផ្សាយ",
            style_story: "និទាន / រឿងនិទាន",
            style_chat: "សន្ទនា",
            style_happy: "រីករាយ / រំភើប",
            style_calm: "ស្ងប់",
            style_rough: "គ្រោត",
            style_clerk: "ស្មៀន",
            style_official: "ធ្ងន់ធ្ងរ / ផ្លូវការ",
            style_customer: "សេវាកម្មអតិថិជន",
            style_commercial: "ពាណិជ្ជកម្ម",
            style_poetry: "កំណាព្យ",
            format_wav_sub: "គ្មានការបាត់បង់ - គុណភាពខ្ពស់",
            format_mp3_sub: "បង្ហាប់ - ឯកសារតូចជាង",
            import_preview: "អូសឯកសារ",
            import_guide: "ទម្លាក់ឯកសារនៅទីនេះ ឬ រកមើល",
            batch_preview: "អសកម្ម",
            btn_batch_start: "ចាប់ផ្តើមការបកប្រែជាក្រុម",
            mock_mode: "របៀបក្លែងក្លាយជាជំនួយ",
            emotion_guide: "ការគ្រប់គ្រងអារម្មណ៍កំណត់កម្រិតបញ្ចេញសំឡេង និងលក្ខណៈសំឡេងផ្សេងៗ។ កែសម្រួលគ្រាប់រំកិលដើម្បីកំណត់ទម្រង់សំឡេង។",
            voxcpm_desc: "សំឡេងសរសៃប្រសាទភាសាខ្មែរដែលមានភាពត្រឹមត្រូវខ្ពស់។ គាំទ្រល្បឿន កម្ពស់សំឡេង និងរចនាបថជាច្រើន។ អាចចម្លងសំឡេងដោយផ្ទាល់ពីឯកសារសំឡេងយោង។",
            omnivoice_desc: "ទម្ងន់ GGUF សម្រាប់ដំណើរការល្បឿនលឿនលើ CPU និងឧបករណ៍ធម្មតា គាំទ្រទាំងភាសាខ្មែរ និងអង់គ្លេស។",
            fish_desc: "ម៉ាស៊ីនចម្លងសំឡេងរហ័ស គាំទ្រការចម្លងសំឡេងភាសាចម្រុះ និងរលកសំឡេងល្បឿនលឿនបំផុត។",
            settings_main_title: "ការកំណត់ប្រព័ន្ធ & ការកំណត់រចនាសម្ព័ន្ធ",
            settings_probe_title: "ការពិនិត្យមីក្រូសេវាដែលបង្រួបបង្រួម",
            settings_probe_desc: "ពិនិត្យមើលច្រកមូលដ្ឋានសកម្មសម្រាប់ម៉ាស៊ីនមេម៉ូដែលដែលកំពុងដំណើរការ (VoxCPM2, OmniVoice, Fish Speech)។",
            settings_probe_btn: "ពិនិត្យស្ថានភាពម៉ាស៊ីនមេ",
            settings_cleanup_title: "ការសម្អាតអង្គចងចាំ & ឃ្លាំងសម្ងាត់ម៉ូដែល",
            settings_cleanup_desc: "សម្អាតឃ្លាំងសម្ងាត់ GPU VRAM ដំណើរការការប្រមូលសំរាម Python និងលុបការផ្ទុកឡើងឯកសារបណ្តោះអាសន្ន។",
            settings_cleanup_btn: "សម្អាត VRAM Cache & សម្អាតឯកសារ",
            settings_download_title: "កម្មវិធីទាញយកម៉ូដែល VoxCPM2",
            settings_download_desc: "ធានាថាទម្ងន់ក្រៅបណ្តាញទាំងអស់ត្រូវបានផ្ទុកពេញលេញទៅកាន់ថតក្នុងតំបន់។",
            settings_download_btn: "ដំណើរការកម្មវិធីទាញយកម៉ូដែល",
            settings_lang_title: "ការជ្រើសរើសភាសានៃចំណុចប្រទាក់",
            settings_lang_desc: "ជ្រើសរើសការធ្វើមូលដ្ឋានីយកម្មលំនាំដើមសម្រាប់ផ្ទាំងជំនួយ និងម៉ឺនុយស្ទូឌីយោ។",
            settings_setup_title: "ការដំឡើងរហ័ស 1-Click & កម្មវិធីក្រិតខ្នាត",
            settings_setup_desc: "កំណត់រចនាសម្ព័ន្ធបរិស្ថាន ទាញយកទម្ងន់ម៉ូដែល និងក្រិតបណ្ណាល័យ Python សម្រាប់ការលោតក្រៅបណ្តាញ។",
            settings_setup_btn: "ដំណើរការដំឡើង 1-Click",
            settings_presets_desc: "គ្រប់គ្រង ពិនិត្យមើលការណែនាំ/អត្ថបទចម្លង និងលុបសំឡេងរចនាផ្ទាល់ខ្លួន និងការកំណត់ក្លូនជាមុនរបស់អ្នក។",
            settings_designed_header: "សំឡេងដែលបានរចនា",
            settings_cloned_header: "ការកំណត់ក្លូនជាមុន",
            history_title: "ប្រវត្តិនៃការបង្កើតសំឡេង",
            btn_clear_history_all: "សម្អាតប្រវត្តិទាំងអស់",
            history_empty_header: "មិនទាន់មានសំឡេងត្រូវបានបង្កើតឡើយ។",
            history_empty_desc: "សូមទៅកាន់ស្ទូឌីយោ វាយអត្ថបទខ្លះ រួចចុច \"បង្កើតសំឡេង\" ដើម្បីចាប់ផ្តើមបង្កើតបណ្ណាល័យរបស់អ្នក។",
            console_title: "ផ្ទាំងគ្រប់គ្រងសកម្មភាពម៉ាស៊ីនមេ",
            console_low_spec: "របៀបលក្ខណៈពិសេសទាប",
            mode_local: "មូលដ្ឋាន",
            offline_label: "ក្រៅបណ្តាញ",
            btn_insert_pause: "បញ្ចូលការផ្អាក (500ms)",
            btn_ai_polish: "AI កែសម្រួលអត្ថបទ",
            btn_voice_input: "សរសេរតាមការអាន (Voice)",
            btn_record_cloning: "ថតសំឡេង / និយាយជំនួស",
            btn_recording_stop: "បញ្ឈប់ការថត",
            btn_merge_history: "ផ្គុំសំឡេងដែលជ្រើសរើស",
            settings_lexicon_title: "វចនានុក្រមបញ្ចេញសំឡេង",
            settings_lexicon_desc: "កំណត់ពាក្យកាត់ ឬពាក្យបរទេស និងសំឡេងអានជាភាសាខ្មែរ (ឧទាហរណ៍៖ 'AI' -> 'អេអាយ')។",
            nav_transcriber: "កម្មវិធីបម្លែងសំឡេង",
            transcriber_title: "កម្មវិធីបម្លែងសំឡេងទៅជាអត្ថបទក្នុងស្រុក (Speech to Text)",
            transcriber_upload_title: "នាំចូលឯកសារសំឡេង",
            transcriber_upload_desc: "ជ្រើសរើសឯកសារ MP3 ឬ WAV ដើម្បីបម្លែងជាអត្ថបទដោយផ្ទាល់នៅលើម៉ាស៊ីន ដោយប្រើប្រាស់ OpenAI Whisper។",
            transcriber_config_title: "ការកំណត់រចនាសម្ព័ន្ធ",
            whisper_model_label: "ទំហំម៉ូដែល Whisper",
            whisper_tiny_opt: "Tiny (លឿនបំផុត, ~75MB)",
            whisper_base_opt: "Base (ណែនាំ, ~140MB)",
            whisper_small_opt: "Small (ល្អសម្រាប់ភាសាខ្មែរ, ~460MB)",
            whisper_medium_opt: "Medium (ភាពត្រឹមត្រូវខ្ពស់, ~1.5GB)",
            whisper_large_opt: "Large V3 (គុណភាពល្អបំផុត, ~3GB)",
            target_format_label: "ទ្រង់ទ្រាយលទ្ធផល",
            format_txt_opt: "Plain Text (.txt)",
            format_srt_opt: "Subtitles (.srt)",
            format_lrc_opt: "Song Lyrics (.lrc)",
            btn_start_transcribe: "ចាប់ផ្តើមបម្លែង",
            transcription_result_title: "លទ្ធផលនៃការបម្លែង",
            btn_copy_clipboard: "ចម្លងទុក",
            btn_save_file: "រក្សាទុកឯកសារ",
            transcribe_language_label: "ភាសា",
            lang_auto_opt: "ស្វែងរកដោយស្វ័យប្រវត្តិ",
            lang_km_opt: "ភាសាខ្មែរ (Khmer)",
            lang_en_opt: "ភាសាអង់គ្លេស (English)",
            transcribe_engine_label: "ម៉ាស៊ីនបម្លែងសំឡេង",
            engine_whisper_opt: "Local Whisper (ក្រៅបណ្តាញ)",
            engine_qwen_opt: "Khmer Transcrip (ក្នុងស្រុក)"
        }
    };

    let currentGUIlang = "en"; // 'en' or 'km'

    // --- DOM Elements ---
    const textInput = document.getElementById("text-input");
    const charCount = document.getElementById("char-count");
    const wordCount = document.getElementById("word-count");
    const btnClearText = document.getElementById("btn-clear-text");
    const btnVoiceInput = document.getElementById("btn-voice-input");
    const btnGenerate = document.getElementById("btn-generate");
    const btnPurgeVram = document.getElementById("btn-purge-vram");
    const btnClearLogs = document.getElementById("btn-clear-logs");
    
    // Emotion tags insertion
    const emotionTags = document.querySelectorAll(".btn-emotion-tag");
    emotionTags.forEach(btn => {
        btn.addEventListener("click", () => {
            const tag = btn.getAttribute("data-tag");
            const start = textInput.selectionStart;
            const end = textInput.selectionEnd;
            const text = textInput.value;
            const before = text.substring(0, start);
            const after = text.substring(end, text.length);
            
            // Auto add spaces around the tag for correct format
            let padBefore = (before.length > 0 && !before.endsWith(" ") && !before.endsWith("\n")) ? " " : "";
            let padAfter = (after.length > 0 && !after.startsWith(" ") && !after.startsWith("\n")) ? " " : "";
            
            textInput.value = before + padBefore + tag + padAfter + after;
            
            // Move cursor to after the inserted tag
            textInput.selectionStart = textInput.selectionEnd = before.length + padBefore.length + tag.length + padAfter.length;
            textInput.focus();
            updateTextStats();
        });
    });
    
    // Fix double-click selection for [emotion] tags
    textInput.addEventListener("dblclick", () => {
        const start = textInput.selectionStart;
        const end = textInput.selectionEnd;
        const text = textInput.value;
        
        // If the browser selected the word inside the brackets, expand to include the brackets
        if (start > 0 && end < text.length) {
            if (text.charAt(start - 1) === '[' && text.charAt(end) === ']') {
                textInput.setSelectionRange(start - 1, end + 1);
            }
        }
    });
    
    // Language glob toggler
    const btnLangSelector = document.getElementById("btn-lang-selector");
    const currentLangText = document.getElementById("current-lang-text");
    const langMenuBox = document.getElementById("lang-menu-box");
    const langMenuItems = document.querySelectorAll(".lang-menu-item");
    
    // Font sizing
    const btnFontDec = document.getElementById("btn-font-dec");
    const btnFontInc = document.getElementById("btn-font-inc");
    const fontSizeDisplay = document.getElementById("font-size-display");
    
    // Accordion group
    const accordionHeaders = document.querySelectorAll(".accordion-header");
    
    // Sliders
    const inputExpressiveness = document.getElementById("input-expressiveness");
    const displayExpressiveness = document.getElementById("val-expressiveness");
    const inputStyle = document.getElementById("input-style");
    const displayStyle = document.getElementById("val-style");
    const inputFidelity = document.getElementById("input-fidelity");
    const displayFidelity = document.getElementById("val-fidelity");
    
    const inputSpeed = document.getElementById("input-speed");
    const displaySpeed = document.getElementById("val-speed");
    const inputPitch = document.getElementById("input-pitch");
    const displayPitch = document.getElementById("val-pitch");
    const inputVolume = document.getElementById("input-volume");
    const displayVolume = document.getElementById("val-volume");
    
    // Engine selections
    const engineTabs = document.querySelectorAll(".engine-tab-item");
    const engineLabel = document.getElementById("selected-engine-label");
    const engineStatus = document.getElementById("selected-engine-status");
    const engineDesc = document.getElementById("selected-engine-desc");
    const enginePort = document.getElementById("selected-engine-port");
    
    // Emotion card buttons
    const emotionBtns = document.querySelectorAll(".emotion-btn");
    const selectVoiceStyle = document.getElementById("select-voice-style");
    const formatBtns = document.querySelectorAll(".format-btn");
    
    // File inputs
    const fileImportDropzone = document.getElementById("file-import-dropzone");
    const fileImportInput = document.getElementById("file-import-input");
    const fileImportLoadedInfo = document.getElementById("import-file-loaded-info");
    const loadedImportFileName = document.getElementById("loaded-import-file-name");
    const btnRemoveImport = document.getElementById("btn-remove-import");
    
    // Drag & Drop Cloning reference
    const dropzone = document.getElementById("audio-dropzone");
    const fileInput = document.getElementById("reference-audio-file");
    const fileLoadedInfo = document.getElementById("file-loaded-info");
    const loadedFileName = document.getElementById("loaded-file-name");
    const btnRemoveAudio = document.getElementById("btn-remove-audio");
    const inputRefTranscript = document.getElementById("reference-text");
    
    // Selector elements for value previews
    const valLangPreview = document.getElementById("val-lang-preview");
    const valVoicePreview = document.getElementById("val-voice-preview");
    const valClonePreview = document.getElementById("val-clone-preview");
    const valEmotionPreview = document.getElementById("val-emotion-preview");
    const valStylePreview = document.getElementById("val-style-preview");
    const valSpeedPreview = document.getElementById("val-speed-preview");
    const valFormatPreview = document.getElementById("val-format-preview");
    
    // Dropdowns
    const selectLanguage = document.getElementById("select-language");
    const selectVoice = document.getElementById("select-voice");
    const selectClonedVoices = document.getElementById("select-cloned-voices");
    
    // Save Cloned Voice selectors
    const voiceSaveGroup = document.getElementById("voice-save-group");
    const inputNewVoiceName = document.getElementById("input-new-voice-name");
    const btnSaveClonedVoice = document.getElementById("btn-save-cloned-voice");
    
    // Nav elements
    const navStudio = document.getElementById("nav-studio");
    const navTranscriber = document.getElementById("nav-transcriber");
    const navHistory = document.getElementById("nav-history");
    const navSettings = document.getElementById("nav-settings");
    const btnStudioDirect = document.querySelector(".btn-studio-direct");
    const studioView = document.getElementById("studio-view");
    const transcriberView = document.getElementById("transcriber-view");
    const historyView = document.getElementById("history-view");
    const settingsView = document.getElementById("settings-view");

    // Transcriber elements
    const transcribeDropzone = document.getElementById("transcribe-dropzone");
    const transcribeDropzoneTxt = document.getElementById("transcribe-dropzone-txt");
    const transcribeAudioFile = document.getElementById("transcribe-audio-file");
    const transcribeFileInfo = document.getElementById("transcribe-file-info");
    const transcribeFileName = document.getElementById("transcribe-file-name");
    const btnRemoveTranscribeAudio = document.getElementById("btn-remove-transcribe-audio");
    const selectWhisperModel = document.getElementById("select-whisper-model");
    const selectTranscribeFormat = document.getElementById("select-transcribe-format");
    const selectTranscribeLanguage = document.getElementById("select-transcribe-language");
    const selectTranscribeEngine = document.getElementById("select-transcribe-engine");
    const whisperModelGroup = document.getElementById("whisper-model-group");
    const btnStartTranscribe = document.getElementById("btn-start-transcribe");
    const transcribeResultText = document.getElementById("transcribe-result-text");
    const btnCopyTranscribe = document.getElementById("btn-copy-transcribe");
    const btnDownloadTranscribe = document.getElementById("btn-download-transcribe");
    const btnToggleTimestamps = document.getElementById("btn-toggle-timestamps");
    const lblToggleTimestamps = document.getElementById("lbl-toggle-timestamps");
    let originalTranscriptionText = "";
    let isTranscriptionCleaned = false;
    
    // Voice design elements
    const btnDeleteVoice = document.getElementById("btn-delete-voice");
    const btnToggleDesignVoice = document.getElementById("btn-toggle-design-voice");
    const voiceDesignGroup = document.getElementById("voice-design-group");
    const inputNewVoiceProfile = document.getElementById("input-new-voice-profile");
    const inputVoicePrompt = document.getElementById("input-voice-prompt");
    const btnSaveDesignedVoice = document.getElementById("btn-save-designed-voice");
    
    // Cloned Voice elements
    const btnDeleteClonedVoice = document.getElementById("btn-delete-cloned-voice");
    
    // History elements
    const btnClearHistoryAll = document.getElementById("btn-clear-history-all");
    const historyEmpty = document.getElementById("history-empty");
    const historyList = document.getElementById("history-list");
    
    // Settings elements
    const btnSettingsProbe = document.getElementById("btn-settings-probe");
    const btnSettingsCleanup = document.getElementById("btn-settings-cleanup");
    const btnSettingsDownload = document.getElementById("btn-settings-download");
    const btnSettingsSetup = document.getElementById("btn-settings-setup");
    const selectSettingsLang = document.getElementById("select-settings-lang");
    
    // Preset voice profiles
    const PRESET_CLONE_VOICES = {
        voice1: {
            name: "Sinn Sisamouth Clone",
            transcript: "សួស្តីបងប្អូនខ្មែរទាំងអស់គ្នា ខ្ញុំបាទ Sinn Sisamouth",
            audio: "data:audio/wav;base64,UklGRkYAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
        },
        voice2: {
            name: "Ros Serey Sothea Clone",
            transcript: "សូមស្វាគមន៍មកកាន់ប្រព័ន្ធបកប្រែសំឡេងខ្មែរ Ros Serey Sothea",
            audio: "data:audio/wav;base64,UklGRkYAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
        },
        voice3: {
            name: "News Anchor Male",
            transcript: "ព័ត៌មានជាតិ និងអន្តរជាតិ ផ្សាយចេញពីទីក្រុងភ្នំពេញ",
            audio: "data:audio/wav;base64,UklGRkYAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
        },
        voice4: {
            name: "News Anchor Female",
            transcript: "ព្រឹត្តិការណ៍ព័ត៌មានថ្មីៗប្រចាំថ្ងៃ ផ្សាយជូនពីបន្ទប់ផ្សាយផ្ទាល់",
            audio: "data:audio/wav;base64,UklGRkYAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
        }
    };
    
    // Audio Player Elements
    const audioEl = document.getElementById("main-audio-element");
    const btnPlayPause = document.getElementById("btn-play-pause");
    const btnDownload = document.getElementById("btn-download");
    const volumeSlider = document.getElementById("volume-slider");
    const currentTimeEl = document.getElementById("current-time");
    const totalTimeEl = document.getElementById("total-time");
    const progressBarContainer = document.getElementById("progress-bar-container");
    const progressBarFill = document.getElementById("progress-bar-fill");
    
    // Canvas visualizer
    const canvas = document.getElementById("waveform-canvas");
    const canvasCtx = canvas.getContext("2d");
    const visualizerPlaceholder = document.getElementById("visualizer-placeholder");
    
    // Downloader
    const btnTriggerDownload = document.getElementById("btn-trigger-download");
    const btnRefreshStatus = document.getElementById("btn-refresh-status");
    const downloadProgressIndicator = document.getElementById("download-progress-indicator");
    const downloadPercentTxt = document.getElementById("download-percent-txt");
    const downloadBarFill = document.getElementById("download-bar-fill");
    
    // Toggle
    const mockFallbackCheckbox = document.getElementById("mock-fallback-checkbox");
    const lowSpecCheckbox = document.getElementById("low-spec-checkbox");
    const terminalOutput = document.getElementById("terminal-output");
    
    // State Variables
    let currentEngine = "voxcpm";
    let base64AudioData = null;
    let currentAudioUrl = null;
    let audioCtx = null;
    let analyser = null;
    let audioSource = null;
    let isVisualizing = false;
    let pollInterval = null;
    let selectedReferenceAudioBase64 = null;
    let activeEmotion = "neutral";
    let activeVoiceStyle = "default";
    let activeFormat = "wav";
    let editorFontSize = 20;
    let isDownloading = false;
    let downloadPollInterval = null;
    let savedClonedVoicesList = [];

    // Transcriber state variables
    let transcribeAudioBase64 = null;
    let transcribeFilename = "";
    let isTranscribing = false;
    let transcribeAbortController = null;

    // Speech generation state variables
    let isGeneratingSpeech = false;
    let generateAbortController = null;

    async function checkAppLicense() {
        const licenseModal = document.getElementById("license-modal");
        const licenseHwidInput = document.getElementById("license-hwid");
        const btnCopyHwid = document.getElementById("btn-copy-hwid");
        const btnActivateLicense = document.getElementById("btn-activate-license");
        const inputLicenseKey = document.getElementById("input-license-key");
        const activationStatus = document.getElementById("license-activation-status");

        if (!licenseModal) return;

        try {
            const res = await fetch("/api/license/status");
            const data = await res.json();

            if (data.status === "active") {
                licenseModal.classList.add("hidden");
            } else {
                licenseModal.classList.remove("hidden");
                if (licenseHwidInput) {
                    licenseHwidInput.value = data.hwid || "THY-ERROR-NO-HWID";
                }
            }
        } catch (err) {
            console.error("License status check failed:", err);
            licenseModal.classList.remove("hidden");
        }

        // Setup Copy HWID handler
        if (btnCopyHwid && licenseHwidInput) {
            btnCopyHwid.addEventListener("click", () => {
                const hwidVal = licenseHwidInput.value;
                navigator.clipboard.writeText(hwidVal).then(() => {
                    const originalText = btnCopyHwid.innerHTML;
                    btnCopyHwid.innerHTML = '<i class="fa-solid fa-circle-check" style="color: #22c55e;"></i> Copied!';
                    setTimeout(() => {
                        btnCopyHwid.innerHTML = originalText;
                    }, 1500);
                }).catch(e => {
                    console.error("Clipboard copy failed:", e);
                });
            });
        }

        // Setup Activation handler
        if (btnActivateLicense && inputLicenseKey && activationStatus) {
            btnActivateLicense.addEventListener("click", async () => {
                const keyVal = inputLicenseKey.value.trim();
                if (!keyVal) {
                    activationStatus.style.color = "#ef4444";
                    activationStatus.textContent = currentGUIlang === "km" ? "សូមបញ្ចូលកូដអាជ្ញាប័ណ្ណ!" : "Please enter your license key!";
                    activationStatus.style.display = "block";
                    return;
                }

                btnActivateLicense.disabled = true;
                btnActivateLicense.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Activating...';
                activationStatus.style.color = "var(--text-dim)";
                activationStatus.textContent = currentGUIlang === "km" ? "កំពុងផ្ទៀងផ្ទាត់..." : "Verifying activation...";
                activationStatus.style.display = "block";

                try {
                    const response = await fetch("/api/license/activate", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ license_key: keyVal })
                    });
                    const result = await response.json();

                    if (result.success) {
                        activationStatus.style.color = "#22c55e";
                        activationStatus.innerHTML = '<i class="fa-solid fa-circle-check"></i> ' + (currentGUIlang === "km" ? "បានសកម្មដោយជោគជ័យ! កំពុងផ្ទុកឡើងវិញ..." : "Activated successfully! Reloading...");
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    } else {
                        btnActivateLicense.disabled = false;
                        btnActivateLicense.innerHTML = '<i class="fa-solid fa-key"></i> Activate Software';
                        activationStatus.style.color = "#ef4444";
                        activationStatus.textContent = result.message || "Activation failed.";
                    }
                } catch (e) {
                    btnActivateLicense.disabled = false;
                    btnActivateLicense.innerHTML = '<i class="fa-solid fa-key"></i> Activate Software';
                    activationStatus.style.color = "#ef4444";
                    activationStatus.textContent = currentGUIlang === "km" ? "កំហុសបណ្តាញ៖ មិនអាចភ្ជាប់ទៅកាន់ម៉ាស៊ីនមេបានទេ!" : "Network error: Failed to connect to server!";
                }
            });
        }
    }

    // --- INITIALIZATION ---
    function init() {
        // Run License checks
        checkAppLicense();

        // Render initial translation
        translateGUI(currentGUIlang);
        
        // Font resizing handlers
        btnFontDec.addEventListener("click", () => adjustFontSize(-2));
        btnFontInc.addEventListener("click", () => adjustFontSize(2));
        
        // Accordion binding
        accordionHeaders.forEach(header => {
            header.addEventListener("click", (e) => {
                const item = e.currentTarget.parentElement;
                const isActive = item.classList.contains("active");
                
                // Collapse others
                document.querySelectorAll(".accordion-item").forEach(el => el.classList.remove("active"));
                
                if (!isActive) {
                    item.classList.add("active");
                }
            });
        });
        
        // Language selectors dropdown Glob binding
        btnLangSelector.addEventListener("click", (e) => {
            e.stopPropagation();
            langMenuBox.classList.toggle("show-menu");
        });
        
        document.addEventListener("click", () => {
            langMenuBox.classList.remove("show-menu");
        });
        
        langMenuItems.forEach(item => {
            item.addEventListener("click", (e) => {
                const selectedLang = e.currentTarget.getAttribute("data-lang");
                currentGUIlang = selectedLang;
                currentLangText.textContent = e.currentTarget.textContent;
                translateGUI(currentGUIlang);
                langMenuBox.classList.remove("show-menu");
                writeLog(`GUI Display language switched to: ${e.currentTarget.textContent}`, "system");
            });
        });
        
        // Sliders updates & previews binding
        bindSlider(inputExpressiveness, displayExpressiveness, updateEmotionPreview);
        bindSlider(inputStyle, displayStyle, updateEmotionPreview);
        bindSlider(inputFidelity, displayFidelity, updateEmotionPreview);
        
        bindSlider(inputSpeed, displaySpeed, updateSpeedPreview);
        bindSlider(inputPitch, displayPitch, updateSpeedPreview);
        bindSlider(inputVolume, displayVolume, updateSpeedPreview);
        
        // Selector details updates
        selectLanguage.addEventListener("change", () => {
            valLangPreview.textContent = selectLanguage.value;
            writeLog(`Target speech language set to: ${selectLanguage.value}`, "info");
        });
        
        selectVoice.addEventListener("change", () => {
            const val = selectVoice.value;
            if (val.startsWith("designed_")) {
                btnDeleteVoice.classList.remove("hidden");
            } else {
                btnDeleteVoice.classList.add("hidden");
            }
            valVoicePreview.textContent = selectVoice.options[selectVoice.selectedIndex].text;
            writeLog(`Voice model profile set to: ${selectVoice.value}`, "info");
        });
        
        btnDeleteVoice.addEventListener("click", () => {
            const val = selectVoice.value;
            if (val.startsWith("designed_")) {
                const index = parseInt(val.split("_")[1]);
                const list = getCustomDesignedVoices();
                const name = list[index]?.name || "Custom Voice";
                list.splice(index, 1);
                localStorage.setItem("custom_designed_voices", JSON.stringify(list));
                writeLog(`Deleted designed voice profile: ${name}`, "warning");
                
                refreshVoiceDropdown();
                selectVoice.value = "default";
                btnDeleteVoice.classList.add("hidden");
                valVoicePreview.textContent = selectVoice.options[selectVoice.selectedIndex].text;
            }
        });
        
        btnToggleDesignVoice.addEventListener("click", () => {
            voiceDesignGroup.classList.toggle("hidden");
        });
        
        btnSaveDesignedVoice.addEventListener("click", () => {
            const name = inputNewVoiceProfile.value.trim();
            const prompt = inputVoicePrompt.value.trim();
            if (!name || !prompt) {
                alert(currentGUIlang === "km" ? "សូមបញ្ចូលឈ្មោះ និងសេចក្តីពិពណ៌នា" : "Please enter both name and description.");
                return;
            }
            
            saveCustomDesignedVoice(name, prompt);
            writeLog(`Saved designed voice profile: ${name}`, "success");
            
            refreshVoiceDropdown();
            
            const list = getCustomDesignedVoices();
            selectVoice.value = `designed_${list.length - 1}`;
            btnDeleteVoice.classList.remove("hidden");
            valVoicePreview.textContent = name;
            
            voiceDesignGroup.classList.add("hidden");
            inputNewVoiceProfile.value = "";
            inputVoicePrompt.value = "";
        });
        
        selectClonedVoices.addEventListener("change", () => {
            const val = selectClonedVoices.value;
            const dict = TRANSLATIONS[currentGUIlang];
            
            if (val.startsWith("custom_")) {
                btnDeleteClonedVoice.classList.remove("hidden");
            } else {
                btnDeleteClonedVoice.classList.add("hidden");
            }
            
            if (val === "none") {
                selectedReferenceAudioBase64 = null;
                inputRefTranscript.value = "";
                fileInput.value = "";
                fileLoadedInfo.classList.add("hidden");
                dropzone.classList.remove("hidden");
                voiceSaveGroup.classList.add("hidden");
                valClonePreview.textContent = dict.clone_none;
                writeLog("Cleared cloning reference.", "info");
            } else if (val.startsWith("voice")) {
                const preset = PRESET_CLONE_VOICES[val];
                selectedReferenceAudioBase64 = preset.audio;
                inputRefTranscript.value = preset.transcript;
                loadedFileName.textContent = preset.name;
                dropzone.classList.add("hidden");
                fileLoadedInfo.classList.remove("hidden");
                voiceSaveGroup.classList.add("hidden");
                valClonePreview.textContent = preset.name;
                writeLog(`Loaded preset cloned voice: ${preset.name}`, "info");
            } else if (val.startsWith("custom_")) {
                const index = parseInt(val.split("_")[1]);
                const savedList = getSavedClonedVoices();
                const customVoice = savedList[index];
                if (customVoice) {
                    selectedReferenceAudioBase64 = customVoice.audio;
                    inputRefTranscript.value = customVoice.transcript;
                    loadedFileName.textContent = customVoice.name;
                    dropzone.classList.add("hidden");
                    fileLoadedInfo.classList.remove("hidden");
                    voiceSaveGroup.classList.add("hidden");
                    valClonePreview.textContent = customVoice.name;
                    writeLog(`Loaded saved cloned voice: ${customVoice.name}`, "info");
                }
            }
        });
        
        btnDeleteClonedVoice.addEventListener("click", () => {
            const val = selectClonedVoices.value;
            if (val.startsWith("custom_")) {
                const index = parseInt(val.split("_")[1]);
                const list = getSavedClonedVoices();
                const v = list[index];
                if (v) {
                    deleteClonedVoiceFile(v.audio);
                    const name = v.name;
                    list.splice(index, 1);
                    localStorage.setItem("saved_cloned_voices", JSON.stringify(list));
                    writeLog(`Deleted cloned voice preset: ${name}`, "warning");
                    
                    refreshClonedVoicesDropdown();
                    selectClonedVoices.value = "none";
                    btnDeleteClonedVoice.classList.add("hidden");
                    valClonePreview.textContent = TRANSLATIONS[currentGUIlang].clone_none;
                    
                    selectedReferenceAudioBase64 = null;
                    inputRefTranscript.value = "";
                    fileInput.value = "";
                    fileLoadedInfo.classList.add("hidden");
                    dropzone.classList.remove("hidden");
                    voiceSaveGroup.classList.add("hidden");
                }
            }
        });
        
        // Tab routing updates
        engineTabs.forEach(tab => {
            tab.addEventListener("click", (e) => {
                engineTabs.forEach(el => el.classList.remove("active"));
                e.currentTarget.classList.add("active");
                
                currentEngine = e.currentTarget.getAttribute("data-engine");
                updateEngineDetails();
                writeLog(`Routed synthesis compiler to target: ${currentEngine.toUpperCase()}`, "info");
            });
        });
        
        // Emotion selections
        emotionBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                emotionBtns.forEach(el => el.classList.remove("active"));
                e.currentTarget.classList.add("active");
                activeEmotion = e.currentTarget.getAttribute("data-emotion");
                
                const emoText = e.currentTarget.querySelector(".txt").textContent;
                valEmotionPreview.textContent = emoText;
                
                writeLog(`Speech emotional style constraint set to: ${activeEmotion.toUpperCase()}`, "info");
            });
        });
        
        // Voice Style selections
        if (selectVoiceStyle) {
            selectVoiceStyle.addEventListener("change", () => {
                activeVoiceStyle = selectVoiceStyle.value;
                if (valStylePreview) {
                    valStylePreview.textContent = selectVoiceStyle.options[selectVoiceStyle.selectedIndex].text;
                }
                writeLog(`Vocal delivery style constraint set to: ${activeVoiceStyle.toUpperCase()}`, "info");
            });
        }
        
        // Format selections
        formatBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                formatBtns.forEach(el => el.classList.remove("active"));
                e.currentTarget.classList.add("active");
                activeFormat = e.currentTarget.getAttribute("data-format");
                valFormatPreview.textContent = activeFormat.toUpperCase();
                writeLog(`Output encoding format set to: ${activeFormat.toUpperCase()}`, "info");
            });
        });
        
        // Editor clear
        btnClearText.addEventListener("click", () => {
            textInput.value = "";
            textInput.focus();
            updateTextStats();
            writeLog("Cleared input text area.", "system");
        });

        // Speech Recognition (Voice Keyboard Dictation)
        let recognition = null;
        let isDictating = false;

        if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = () => {
                isDictating = true;
                btnVoiceInput.innerHTML = `<i class="fa-solid fa-microphone-slash fa-beat" style="color: #ef4444; margin-right: 0.3rem;"></i> Stop dictation`;
                btnVoiceInput.style.borderColor = "#ef4444";
                btnVoiceInput.style.color = "#ef4444";
                writeLog("Voice dictation started. Speak into your microphone...", "info");
            };

            recognition.onerror = (event) => {
                writeLog("Voice dictation error: " + event.error, "error");
            };

            recognition.onend = () => {
                isDictating = false;
                btnVoiceInput.innerHTML = `<i class="fa-solid fa-microphone"></i> ${TRANSLATIONS[currentGUIlang].btn_voice_input}`;
                btnVoiceInput.style.borderColor = "rgba(14, 165, 233, 0.3)";
                btnVoiceInput.style.color = "var(--accent-cyan)";
                writeLog("Voice dictation stopped.", "info");
            };

            recognition.onresult = (event) => {
                let finalTranscript = "";
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    }
                }
                if (finalTranscript) {
                    const start = textInput.selectionStart;
                    const end = textInput.selectionEnd;
                    const val = textInput.value;
                    textInput.value = val.substring(0, start) + finalTranscript + val.substring(end);
                    textInput.selectionStart = textInput.selectionEnd = start + finalTranscript.length;
                    textInput.focus();
                    updateTextStats();
                }
            };

            btnVoiceInput.addEventListener("click", () => {
                if (isDictating) {
                    recognition.stop();
                } else {
                    const selectedLang = document.getElementById("select-language").value;
                    recognition.lang = selectedLang; // e.g. "km-KH" or "en-US"
                    recognition.start();
                }
            });
        } else {
            // Tell user how to resolve insecure context/origin issues if blocked
            if (btnVoiceInput) {
                btnVoiceInput.addEventListener("click", () => {
                    alert("Speech dictation is blocked or unsupported by your browser.\n\nTo enable voice dictation, please open the app using the link http://localhost:8000 (not 127.0.0.1) in Google Chrome so the browser can request microphone access.");
                });
            }
        }
        
        textInput.addEventListener("input", updateTextStats);
        
        // File dropzones
        setupDropzoneCloning();
        setupDropzoneFileImport();
        setupTranscriber();
        
        // Core buttons
        btnGenerate.addEventListener("click", handleGenerate);
        if (btnPurgeVram) {
            btnPurgeVram.addEventListener("click", handlePurgeVram);
        }
        btnRefreshStatus.addEventListener("click", pollServicesStatus);
        btnTriggerDownload.addEventListener("click", handleStartDownload);

        // Load & save Low Spec setting state
        if (lowSpecCheckbox) {
            if (localStorage.getItem("low_spec_mode") !== null) {
                lowSpecCheckbox.checked = localStorage.getItem("low_spec_mode") === "true";
            } else {
                lowSpecCheckbox.checked = true; // lightweight by default
            }
            lowSpecCheckbox.addEventListener("change", () => {
                localStorage.setItem("low_spec_mode", lowSpecCheckbox.checked);
                writeLog(`Low-Spec PC Mode set to: ${lowSpecCheckbox.checked ? "ENABLED (Auto VRAM release)" : "DISABLED (Cache weights)"}`, "info");
            });
        }

        // Load & save Mock Fallback setting state
        if (mockFallbackCheckbox) {
            if (localStorage.getItem("mock_fallback") !== null) {
                mockFallbackCheckbox.checked = localStorage.getItem("mock_fallback") === "true";
            }
            mockFallbackCheckbox.addEventListener("change", () => {
                localStorage.setItem("mock_fallback", mockFallbackCheckbox.checked);
            });
        }
        
        // Audio Player
        setupAudioPlayer();
        
        // Tab switching bindings
        navStudio.addEventListener("click", (e) => {
            e.preventDefault();
            switchTab("studio");
        });
        if (navTranscriber) {
            navTranscriber.addEventListener("click", (e) => {
                e.preventDefault();
                switchTab("transcriber");
            });
        }
        navHistory.addEventListener("click", (e) => {
            e.preventDefault();
            switchTab("history");
        });
        navSettings.addEventListener("click", (e) => {
            e.preventDefault();
            switchTab("settings");
        });
        btnStudioDirect.addEventListener("click", (e) => {
            e.preventDefault();
            switchTab("studio");
        });
        
        // Settings page buttons
        btnSettingsProbe.addEventListener("click", pollServicesStatus);
        btnSettingsCleanup.addEventListener("click", handlePurgeVram);
        btnSettingsDownload.addEventListener("click", handleStartDownload);
        if (btnSettingsSetup) {
            btnSettingsSetup.addEventListener("click", handleStartSetup);
        }
        selectSettingsLang.addEventListener("change", () => {
            currentGUIlang = selectSettingsLang.value;
            translateGUI(currentGUIlang);
            currentLangText.textContent = currentGUIlang === "en" ? "us English" : "KH ខ្មែរ";
        });
        
        // Clear all history button
        btnClearHistoryAll.addEventListener("click", clearAllHistory);
        
        // Load custom voices dropdown
        refreshVoiceDropdown();
        
        // Status Polling loop
        pollServicesStatus();
        pollInterval = setInterval(pollServicesStatus, 5000);
        

        
        // Bind Insert Pause
        const btnInsertPause = document.getElementById("btn-insert-pause");
        if (btnInsertPause) {
            btnInsertPause.addEventListener("click", () => {
                insertTextAtCursor(textInput, '<break time="500ms"/>');
                writeLog("Inserted pause break tag.", "info");
            });
        }
        

        
        // Bind Voice Record for Cloning / Respeaker
        const btnRecordCloning = document.getElementById("btn-record-cloning");
        if (btnRecordCloning) {
            btnRecordCloning.addEventListener("click", () => {
                if (isRecordingCloning) {
                    stopRecordingCloning();
                } else {
                    startRecordingCloning();
                }
            });
        }
        
        // Bind Merge History
        const btnMergeHistory = document.getElementById("btn-merge-history");
        if (btnMergeHistory) {
            btnMergeHistory.addEventListener("click", handleMergeHistoryClips);
        }
        
        // Bind Lexicon Add button
        const lexiconWordInput = document.getElementById("lexicon-word");
        const lexiconPhoneticInput = document.getElementById("lexicon-phonetic");
        const btnAddLexicon = document.getElementById("btn-add-lexicon");
        if (btnAddLexicon && lexiconWordInput && lexiconPhoneticInput) {
            btnAddLexicon.addEventListener("click", () => {
                const word = lexiconWordInput.value.trim();
                const phonetic = lexiconPhoneticInput.value.trim();
                if (!word || !phonetic) {
                    alert(currentGUIlang === "km" ? "សូមបញ្ចូលពាក្យ និងសំឡេងអាន!" : "Please enter both word and phonetic spelling!");
                    return;
                }
                const rules = getLexiconRules();
                const existsIdx = rules.findIndex(r => r.word.toLowerCase() === word.toLowerCase());
                if (existsIdx !== -1) {
                    rules[existsIdx].phonetic = phonetic;
                } else {
                    rules.push({ word, phonetic });
                }
                saveLexiconRules(rules);
                renderLexiconUI();
                lexiconWordInput.value = "";
                lexiconPhoneticInput.value = "";
                writeLog(`Added lexicon rule: "${word}" -> "${phonetic}"`, "success");
            });
        }
        
        // Render lexicon on launch
        renderLexiconUI();

        // Synchronize custom cloned voices with the server
        syncClonedVoicesFromServer();

        // Canvas boundary adjustment
        resizeCanvas();
        window.addEventListener("resize", resizeCanvas);

        // Software Update handlers
        const btnCheckUpdate = document.getElementById("btn-check-update");
        const btnDownloadUpdate = document.getElementById("btn-download-update");
        const updateStatusMsg = document.getElementById("update-status-msg");
        const changelogArea = document.getElementById("changelog-area");
        const updateChangelogTxt = document.getElementById("update-changelog-txt");

        if (btnCheckUpdate) {
            btnCheckUpdate.addEventListener("click", async () => {
                btnCheckUpdate.disabled = true;
                updateStatusMsg.innerText = currentGUIlang === "km" ? "កំពុងពិនិត្យមើលការអាប់ដេត..." : "Checking server for updates...";
                changelogArea.classList.add("hidden");
                btnDownloadUpdate.classList.add("hidden");
                
                try {
                    const res = await fetch("/api/check-update");
                    const data = await res.json();
                    
                    if (data.update_available) {
                        updateStatusMsg.innerHTML = `<span style="color:var(--accent-fuchsia);font-weight:600;">${currentGUIlang === "km" ? "មានកំណែទម្រង់ថ្មី៖ v" : "Update Available: v"}${data.online_version}</span>`;
                        btnDownloadUpdate.href = data.download_url;
                        btnDownloadUpdate.classList.remove("hidden");
                        
                        if (data.changelog) {
                            updateChangelogTxt.innerText = data.changelog;
                            changelogArea.classList.remove("hidden");
                        }
                    } else {
                        updateStatusMsg.innerText = currentGUIlang === "km" ? `កម្មវិធីរបស់អ្នកជាកំណែចុងក្រោយបង្អស់ហើយ (v${data.current_version})` : `Your software is up to date (v${data.current_version}).`;
                    }
                } catch (e) {
                    updateStatusMsg.innerText = currentGUIlang === "km" ? "មិនអាចភ្ជាប់ទៅកាន់ម៉ាស៊ីនបម្រើបានទេ!" : "Failed to connect to version check server.";
                } finally {
                    btnCheckUpdate.disabled = false;
                }
            });
        }
    }
    
    // --- ADVANCED FEATURE SUITE HELPERS ---
    
    // Phase 1: Lexicon Local Storage Helpers
    function getLexiconRules() {
        const stored = localStorage.getItem("digital_tts_lexicon_rules");
        return stored ? JSON.parse(stored) : [];
    }
    
    function saveLexiconRules(rules) {
        localStorage.setItem("digital_tts_lexicon_rules", JSON.stringify(rules));
    }
    
    function applyLexiconRules(text) {
        const rules = getLexiconRules();
        let replacedText = text;
        const sortedRules = [...rules].sort((a, b) => b.word.length - a.word.length);
        let matchCount = 0;
        
        for (const rule of sortedRules) {
            if (!rule.word.trim()) continue;
            const isLatin = /^[a-zA-Z0-9_]+$/.test(rule.word);
            const regexStr = isLatin ? `\\b${escapeRegExp(rule.word)}\\b` : escapeRegExp(rule.word);
            const regex = new RegExp(regexStr, "gi");
            const count = (replacedText.match(regex) || []).length;
            if (count > 0) {
                replacedText = replacedText.replace(regex, rule.phonetic);
                matchCount += count;
            }
        }
        if (matchCount > 0) {
            writeLog(`Lexicon Substitution applied: replaced ${matchCount} match(es).`, "info");
        }
        return replacedText;
    }
    
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    function renderLexiconUI() {
        const container = document.getElementById("lexicon-list-container");
        if (!container) return;
        
        const rules = getLexiconRules();
        container.innerHTML = "";
        
        if (rules.length === 0) {
            const emptyEl = document.createElement("div");
            emptyEl.style.fontSize = "0.75rem";
            emptyEl.style.opacity = "0.5";
            emptyEl.style.padding = "0.2rem";
            emptyEl.textContent = currentGUIlang === "km" ? "គ្មានច្បាប់វចនានុក្រម..." : "No lexicon rules defined...";
            container.appendChild(emptyEl);
            return;
        }
        
        rules.forEach((rule, idx) => {
            const item = document.createElement("div");
            item.style.display = "flex";
            item.style.justifyContent = "space-between";
            item.style.alignItems = "center";
            item.style.padding = "0.25rem 0.4rem";
            item.style.borderBottom = "1px solid rgba(255,255,255,0.05)";
            item.style.fontSize = "0.8rem";
            
            const textSpan = document.createElement("span");
            textSpan.innerHTML = `<strong style="color: var(--accent-cyan);">${escapeHTML(rule.word)}</strong> &rarr; <span style="color: var(--accent-fuchsia);">${escapeHTML(rule.phonetic)}</span>`;
            
            const deleteBtn = document.createElement("button");
            deleteBtn.className = "btn-ghost";
            deleteBtn.style.padding = "0.2rem";
            deleteBtn.style.color = "#ef4444";
            deleteBtn.innerHTML = '<i class="fa-solid fa-trash-can" style="font-size: 0.75rem;"></i>';
            deleteBtn.addEventListener("click", () => {
                const removed = rules.splice(idx, 1)[0];
                saveLexiconRules(rules);
                renderLexiconUI();
                writeLog(`Deleted lexicon rule: ${removed.word}`, "info");
            });
            
            item.appendChild(textSpan);
            item.appendChild(deleteBtn);
            container.appendChild(item);
        });
    }
    
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag));
    }
    
    // Phase 2: SSML break insert
    function insertTextAtCursor(textarea, textToInsert) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;
        const before = text.substring(0, start);
        const after = text.substring(end, text.length);
        textarea.value = before + textToInsert + after;
        textarea.selectionStart = textarea.selectionEnd = start + textToInsert.length;
        textarea.focus();
        updateTextStats();
    }
    

    
    // Phase 4: Audio Merger handler
    async function handleMergeHistoryClips() {
        const btn = document.getElementById("btn-merge-history");
        const checked = document.querySelectorAll(".history-select-chk:checked");
        if (checked.length < 2) {
            alert(currentGUIlang === "km" ? "សូមជ្រើសរើសសំឡេងយ៉ាងតិច ២ ដើម្បីផ្គុំ!" : "Please select at least 2 audio clips to merge.");
            return;
        }
        
        const urls = Array.from(checked).map(chk => chk.value).filter(url => url && !url.startsWith("db:") && !url.startsWith("data:"));
        if (urls.length < checked.length) {
            alert(currentGUIlang === "km" ? "ការផ្គុំគាំទ្រតែសំឡេងដែលរក្សាទុកលើម៉ាស៊ីនមេប៉ុណ្ណោះ។" : "Merging only supports clips that are hosted on the server.");
            return;
        }
        
        btn.disabled = true;
        const toast = showToast(currentGUIlang === "km" ? "កំពុងផ្គុំឯកសារសំឡេង..." : "Merging audio files...", "processing");
        
        try {
            const res = await fetch("/api/merge", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ files: urls })
            });
            
            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Merge failed");
            }
            const data = await res.json();
            if (data.success) {
                if (toast && toast.close) toast.close();
                showToast(currentGUIlang === "km" ? "ការផ្គុំទទួលបានជោគជ័យ!" : "Merged successfully!", "success", 4000);
                writeLog(`Merged ${urls.length} audio clips into ${data.audio_url}`, "success");
                
                const newId = Date.now().toString() + Math.random().toString();
                const mergedItem = {
                    id: newId,
                    timestamp: new Date().toLocaleString(),
                    text: "[Merged Clip] " + Array.from(checked).map(chk => {
                        const card = chk.closest(".history-item-card");
                        const txtEl = card ? card.querySelector("p") : null;
                        return txtEl ? txtEl.textContent : "";
                    }).join(" + ").substring(0, 80) + "...",
                    engine: "merged",
                    format: "wav",
                    speed: 1.0,
                    pitch: 0,
                    latency_ms: 0,
                    audio_url: data.audio_url,
                    mock: false
                };
                
                saveHistoryItem(mergedItem);
                document.querySelectorAll(".history-select-chk").forEach(c => c.checked = false);
            }
        } catch (err) {
            if (toast && toast.close) toast.close();
            showToast(err.message, "error", 5000);
            writeLog(`Audio merge failed: ${err.message}`, "error");
        } finally {
            btn.disabled = false;
        }
    }
    
    // Phase 5: Voice Recorder & Speech-to-Speech cloning (Respeaker)
    let mediaRecorder = null;
    let audioChunks = [];
    let recognition = null;
    let isRecordingCloning = false;
    
    if (window.webkitSpeechRecognition || window.SpeechRecognition) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRec();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = "km-KH";
        
        recognition.onresult = (event) => {
            let finalTranscript = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            if (finalTranscript.trim()) {
                if (inputRefTranscript.value) {
                    inputRefTranscript.value += " " + finalTranscript;
                } else {
                    inputRefTranscript.value = finalTranscript;
                }
                writeLog(`WebSpeech transcribed reference text: "${finalTranscript}"`, "info");
            }
        };
        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            writeLog(`Speech recognition error: ${event.error}`, "warning");
        };
    }
    
    async function startRecordingCloning() {
        audioChunks = [];
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                const mimeType = mediaRecorder.mimeType || 'audio/webm';
                const audioBlob = new Blob(audioChunks, { type: mimeType });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    selectedReferenceAudioBase64 = reader.result;
                    if (dropzone) dropzone.classList.add("hidden");
                    if (fileLoadedInfo && loadedFileName) {
                        let extension = "webm";
                        if (mimeType.includes("mp4")) extension = "mp4";
                        else if (mimeType.includes("aac")) extension = "aac";
                        else if (mimeType.includes("ogg")) extension = "ogg";
                        else if (mimeType.includes("wav")) extension = "wav";
                        
                        loadedFileName.textContent = "Recorded_Voice_Input." + extension;
                        fileLoadedInfo.classList.remove("hidden");
                    }
                    if (valClonePreview) valClonePreview.textContent = "Voice Recorded";
                    if (voiceSaveGroup) {
                        voiceSaveGroup.classList.remove("hidden");
                        if (inputNewVoiceName) inputNewVoiceName.value = "Recorded_Voice";
                    }
                    writeLog("Microphone audio loaded as zero-shot voice clone reference.", "success");
                };
                stream.getTracks().forEach(track => track.stop());
            };
            
            mediaRecorder.start();
            if (recognition) {
                recognition.lang = selectLanguage.value || "km-KH";
                try {
                    recognition.start();
                } catch (e) {}
            }
            
            isRecordingCloning = true;
            updateRecordCloningButtonUI();
            writeLog("Recording voice & transcribing...", "info");
        } catch (err) {
            console.error("Mic access failed:", err);
            writeLog(`Mic access failed: ${err.message}`, "error");
            alert("Could not access microphone.");
        }
    }
    
    function stopRecordingCloning() {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
        }
        if (recognition) {
            try {
                recognition.stop();
            } catch (e) {}
        }
        isRecordingCloning = false;
        updateRecordCloningButtonUI();
        writeLog("Recording stopped.", "info");
    }
    
    function updateRecordCloningButtonUI() {
        const btn = document.getElementById("btn-record-cloning");
        if (!btn) return;
        if (isRecordingCloning) {
            btn.innerHTML = '<i class="fa-solid fa-square" style="color: #ef4444; animation: pulse 1s infinite;"></i> <span data-translate="btn_recording_stop">Stop Recording</span>';
            btn.style.background = "rgba(239, 68, 68, 0.15)";
            btn.style.borderColor = "rgba(239, 68, 68, 0.3)";
            btn.style.color = "#f87171";
        } else {
            btn.innerHTML = '<i class="fa-solid fa-microphone"></i> <span data-translate="btn_record_cloning">Record Voice</span>';
            btn.style.background = "rgba(59, 130, 246, 0.15)";
            btn.style.borderColor = "rgba(59, 130, 246, 0.3)";
            btn.style.color = "#60a5fa";
        }
    }

    // --- TRANSLATOR RUNNER ---
    function translateGUI(langCode) {
        const dictionary = TRANSLATIONS[langCode];
        
        // Translate all data-translate elements
        document.querySelectorAll("[data-translate]").forEach(el => {
            const key = el.getAttribute("data-translate");
            if (dictionary[key]) {
                el.textContent = dictionary[key];
            }
        });
        
        // Translate placeholder
        if (langCode === "km") {
            textInput.placeholder = "សរសេរ ឬ បញ្ចូលអត្ថបទភាសាខ្មែរនៅទីនេះដើម្បីបំលែងជាសំឡេងសិប្បនិម្មិត...";
            inputRefTranscript.placeholder = "បញ្ចូលអត្ថបទសរសេរនៃសំឡេងយោង...";
        } else {
            textInput.placeholder = "Enter text here to synthesize speech...";
            inputRefTranscript.placeholder = "Enter transcript of reference voice audio...";
        }
        
        // Keep previews translated
        updateEngineDetails();
        
        // Rebuild voice select dropdown with localizations
        const prevVoiceVal = selectVoice.value;
        refreshVoiceDropdown();
        selectVoice.value = prevVoiceVal;
        
        // Rebuild cloned voice select dropdown with localizations
        const prevValue = selectClonedVoices.value;
        refreshClonedVoicesDropdown();
        selectClonedVoices.value = prevValue;
        
        // Sync settings lang selection
        if (selectSettingsLang) {
            selectSettingsLang.value = langCode;
        }
        
        // Target speech language sync removed per request to separate UI and input language
        
        // Sync top-right language label
        if (currentLangText) {
            currentLangText.textContent = langCode === "km" ? "KH ខ្មែរ" : "us English";
        }
    }
    
    // --- ACCORDION PREVIEWS ---
    function updateEmotionPreview() {
        displayExpressiveness.textContent = inputExpressiveness.value;
        displayStyle.textContent = inputStyle.value;
        displayFidelity.textContent = inputFidelity.value;
    }
    
    function updateSpeedPreview() {
        displaySpeed.textContent = inputSpeed.value;
        displayPitch.textContent = (parseInt(inputPitch.value) >= 0 ? "+" : "") + inputPitch.value;
        displayVolume.textContent = inputVolume.value;
        
        valSpeedPreview.textContent = `${inputSpeed.value}x ${displayPitch.textContent} ${inputVolume.value}%`;
    }
    
    function adjustFontSize(delta) {
        editorFontSize = Math.max(12, Math.min(36, editorFontSize + delta));
        fontSizeDisplay.textContent = editorFontSize;
        textInput.style.fontSize = `${editorFontSize}px`;
        writeLog(`Adjusted editor text font scale to: ${editorFontSize}px`, "system");
    }
    
    function updateTextStats() {
        const text = textInput.value;
        charCount.textContent = text.length.toLocaleString();
        
        // Count words (simple whitespace split)
        const words = text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
        wordCount.textContent = words.toLocaleString();
    }
    
    function bindSlider(slider, display, callback) {
        slider.addEventListener("input", () => {
            display.textContent = slider.value;
            if (callback) callback();
        });
    }
    
    // --- ACCORDION DETAILS SYNC ---
    function updateEngineDetails() {
        const dictionary = TRANSLATIONS[currentGUIlang];
        const cloneTitleEl = document.querySelector("#drawer-cloning .header-text span[data-translate='drawer_cloning']") || document.querySelector("#drawer-cloning .header-text span");
        
        if (currentEngine === "voxcpm") {
            engineLabel.textContent = "VoxCPM2 Khmer TTS";
            engineDesc.textContent = dictionary.voxcpm_desc;
            enginePort.textContent = "8081";
            
            document.getElementById("drawer-cloning").classList.remove("hidden");
            document.getElementById("drawer-emotions").classList.remove("hidden");
            if (cloneTitleEl) {
                cloneTitleEl.textContent = currentGUIlang === "km" ? "ចម្លងសំឡេង (VoxCPM2)" : "Clone a Voice (VoxCPM2)";
            }
        } else if (currentEngine === "omnivoice") {
            engineLabel.textContent = "OmniVoice Engine";
            engineDesc.textContent = dictionary.omnivoice_desc;
            enginePort.textContent = "8082";
            
            document.getElementById("drawer-cloning").classList.add("hidden");
            document.getElementById("drawer-emotions").classList.remove("hidden");
        } else if (currentEngine === "fish") {
            engineLabel.textContent = "Fish Speech Cloner";
            engineDesc.textContent = dictionary.fish_desc;
            enginePort.textContent = "8080";
            
            document.getElementById("drawer-cloning").classList.remove("hidden");
            document.getElementById("drawer-emotions").classList.add("hidden"); // Fish handles expressiveness slider only
            if (cloneTitleEl) {
                cloneTitleEl.textContent = currentGUIlang === "km" ? "ចម្លងសំឡេង (Fish Speech)" : "Clone a Voice (Fish Speech)";
            }
        }
    }
    
    // --- TRANSCRIBER SETUP ---
    function setupTranscriber() {
        if (!transcribeDropzone || !transcribeAudioFile) return;

        transcribeDropzone.addEventListener("click", () => transcribeAudioFile.click());

        transcribeAudioFile.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                processTranscribeFile(e.target.files[0]);
            }
        });

        transcribeDropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            transcribeDropzone.classList.add("dragover");
        });

        transcribeDropzone.addEventListener("dragleave", () => {
            transcribeDropzone.classList.remove("dragover");
        });

        transcribeDropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            transcribeDropzone.classList.remove("dragover");
            if (e.dataTransfer.files.length > 0) {
                processTranscribeFile(e.dataTransfer.files[0]);
            }
        });

        if (btnRemoveTranscribeAudio) {
            btnRemoveTranscribeAudio.addEventListener("click", (e) => {
                e.stopPropagation();
                resetTranscriberAudio();
            });
        }

        if (btnStartTranscribe) {
            btnStartTranscribe.addEventListener("click", runTranscription);
        }

        if (btnCopyTranscribe) {
            btnCopyTranscribe.addEventListener("click", copyTranscriptionToClipboard);
        }

        if (btnDownloadTranscribe) {
            btnDownloadTranscribe.addEventListener("click", downloadTranscriptionFile);
        }

        if (btnToggleTimestamps) {
            btnToggleTimestamps.addEventListener("click", () => {
                if (!originalTranscriptionText) return;
                if (!isTranscriptionCleaned) {
                    const cleanedText = cleanTranscriptionTimestamps(originalTranscriptionText);
                    if (transcribeResultText) {
                        transcribeResultText.value = cleanedText;
                    }
                    isTranscriptionCleaned = true;
                } else {
                    if (transcribeResultText) {
                        transcribeResultText.value = originalTranscriptionText;
                    }
                    isTranscriptionCleaned = false;
                }
                updateToggleTimestampsLabel();
            });
        }

        if (selectTranscribeEngine && whisperModelGroup) {
            selectTranscribeEngine.addEventListener("change", () => {
                const val = selectTranscribeEngine.value;
                if (val === "qwen") {
                    whisperModelGroup.style.display = "none";
                    if (selectTranscribeLanguage) {
                        selectTranscribeLanguage.value = "km";
                    }
                } else {
                    whisperModelGroup.style.display = "block";
                }
            });
            // Initial run
            const initialVal = selectTranscribeEngine.value;
            if (initialVal === "qwen") {
                whisperModelGroup.style.display = "none";
                if (selectTranscribeLanguage) {
                    selectTranscribeLanguage.value = "km";
                }
            }
        }
    }

    function processTranscribeFile(file) {
        if (!file.type.startsWith("audio/") && !file.name.endsWith(".mp3") && !file.name.endsWith(".wav") && !file.name.endsWith(".m4a")) {
            writeLog("Error: transcription reference file must be an audio file.", "error");
            alert(currentGUIlang === "km" ? "កំហុស៖ ឯកសារត្រូវតែជាប្រភេទសំឡេង (.mp3, .wav, .m4a)" : "Error: Reference file must be an audio file (.mp3, .wav, .m4a).");
            return;
        }

        transcribeFilename = file.name;
        if (transcribeFileName) {
            transcribeFileName.textContent = file.name;
        }
        if (transcribeDropzone) {
            transcribeDropzone.classList.add("hidden");
        }
        if (transcribeFileInfo) {
            transcribeFileInfo.classList.remove("hidden");
        }

        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            transcribeAudioBase64 = reader.result;
            writeLog(`Loaded audio file for transcription: ${file.name}`, "success");
        };
        reader.onerror = (err) => {
            writeLog(`Failed to read audio file: ${err}`, "error");
        };
    }

    function resetTranscriberAudio() {
        transcribeAudioFile.value = "";
        transcribeAudioBase64 = null;
        transcribeFilename = "";
        if (transcribeFileInfo) {
            transcribeFileInfo.classList.add("hidden");
        }
        if (transcribeDropzone) {
            transcribeDropzone.classList.remove("hidden");
        }
        writeLog("Cleared transcription audio file.", "info");
    }

    async function runTranscription() {
        if (isTranscribing) {
            if (transcribeAbortController) {
                transcribeAbortController.abort();
            }
            return;
        }

        if (!transcribeAudioBase64) {
            alert(currentGUIlang === "km" ? "សូមជ្រើសរើសឯកសារសំឡេងជាមុនសិន។" : "Please select or drop an audio file first.");
            return;
        }

        const modelSize = selectWhisperModel ? selectWhisperModel.value : "base";
        const outputFormat = selectTranscribeFormat ? selectTranscribeFormat.value : "srt";
        const transcribeLanguage = selectTranscribeLanguage ? selectTranscribeLanguage.value : "auto";
        const transcribeEngine = selectTranscribeEngine ? selectTranscribeEngine.value : "whisper";
        const apiKeyValue = localStorage.getItem("digital_tts_gemini_api_key") || null;

        isTranscribing = true;
        if (btnToggleTimestamps) btnToggleTimestamps.classList.add("hidden");
        transcribeAbortController = new AbortController();
        const { signal } = transcribeAbortController;

        const originalHTML = btnStartTranscribe.innerHTML;
        btnStartTranscribe.classList.add("btn-transcribing-stop");
        btnStartTranscribe.innerHTML = '<i class="fa-solid fa-circle-stop"></i> ' + (currentGUIlang === "km" ? "បញ្ឈប់ការបម្លែង (Stop)" : "Stop Transcription");
        
        if (transcribeResultText) {
            if (transcribeEngine === "qwen") {
                transcribeResultText.value = currentGUIlang === "km"
                    ? "កំពុងបម្លែង... (ប្រសិនបើនេះជាលើកដំបូង ម៉ាស៊ីនត្រូវការទាញយកម៉ូដែល Khmer Transcrip (~1.2GB) ដែលអាចចំណាយពេលពីរបីនាទី)"
                    : "Transcribing... (If this is the first run, the local system will download the Khmer Transcrip model (~1.2GB) which may take several minutes.)";
            } else {
                transcribeResultText.value = currentGUIlang === "km" 
                    ? "កំពុងបម្លែង... (ប្រសិនបើនេះជាលើកដំបូង ម៉ាស៊ីនអាចត្រូវការទាញយកម៉ូដែល Whisper ដែលអាចចំណាយពេលខ្លះ)" 
                    : "Transcribing... (If this is the first run, the local system might download the Whisper model weights, which could take a moment)";
            }
        }

        // Set up Progress Bar elements
        const transcribeProgressIndicator = document.getElementById("transcribe-progress-indicator");
        const transcribeProgressStatus = document.getElementById("transcribe-progress-status");
        const transcribeProgressPercent = document.getElementById("transcribe-progress-percent");
        const transcribeBarFill = document.getElementById("transcribe-bar-fill");
        let progressPollInterval = null;

        if (transcribeProgressIndicator) {
            transcribeProgressIndicator.classList.remove("hidden");
            if (transcribeBarFill) transcribeBarFill.style.width = "0%";
            if (transcribeProgressPercent) transcribeProgressPercent.textContent = "0%";
            if (transcribeProgressStatus) {
                transcribeProgressStatus.textContent = currentGUIlang === "km" ? "កំពុងរៀបចំឯកសារសំឡេង..." : "Preparing audio file...";
            }
        }

        let simulatedPercent = 0;
        let isDownloadingModel = false;

        progressPollInterval = setInterval(async () => {
            try {
                const res = await fetch("/api/transcribe/progress");
                if (res.ok) {
                    const pData = await res.json();
                    const statusText = pData.status || "";
                    const pct = pData.progress;

                    if (statusText.toLowerCase().includes("downloading")) {
                        isDownloadingModel = true;
                        if (transcribeBarFill) transcribeBarFill.style.width = "0%";
                        if (transcribeProgressPercent) transcribeProgressPercent.textContent = "0%";
                        if (transcribeProgressStatus) {
                            transcribeProgressStatus.textContent = statusText;
                        }
                    } else {
                        // Not downloading
                        if (transcribeEngine === "qwen") {
                            // Qwen: Use actual backend chunking progress
                            if (transcribeBarFill) transcribeBarFill.style.width = `${pct}%`;
                            if (transcribeProgressPercent) transcribeProgressPercent.textContent = `${Math.round(pct)}%`;
                            if (transcribeProgressStatus) {
                                if (pct >= 99) {
                                    transcribeProgressStatus.textContent = currentGUIlang === "km" ? "កំពុងបញ្ចប់..." : "Finalizing...";
                                } else {
                                    transcribeProgressStatus.textContent = currentGUIlang === "km" ? `កំពុងដំណើរការ... ${Math.round(pct)}%` : `Transcribing chunks... ${Math.round(pct)}%`;
                                }
                            }
                        } else {
                            // Whisper: Use simulated progress once transcribing starts
                            if (simulatedPercent < 95) {
                                simulatedPercent += Math.random() * 2 + 1; // Increase by 1-3%
                                if (simulatedPercent > 95) simulatedPercent = 95;
                            }
                            if (transcribeBarFill) {
                                transcribeBarFill.style.width = `${Math.round(simulatedPercent)}%`;
                            }
                            if (transcribeProgressPercent) {
                                transcribeProgressPercent.textContent = `${Math.round(simulatedPercent)}%`;
                            }
                            if (transcribeProgressStatus) {
                                transcribeProgressStatus.textContent = statusText || (currentGUIlang === "km" ? "កំពុងដំណើរការ (Whisper)..." : "Transcribing (Whisper)...");
                            }
                        }
                    }
                }
            } catch (e) {
                console.error("Progress poll error:", e);
            }
        }, 1000);

        writeLog(`Starting local transcription of ${transcribeFilename} (Engine: ${transcribeEngine}, Model: ${modelSize}, Format: ${outputFormat}, Language: ${transcribeLanguage})...`, "info");

        try {
            const response = await fetch("/api/transcribe", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    audio_base64: transcribeAudioBase64,
                    filename: transcribeFilename,
                    model_size: modelSize,
                    output_format: outputFormat,
                    language: transcribeLanguage,
                    engine: transcribeEngine,
                    api_key: apiKeyValue
                }),
                signal: signal
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Server error during transcription");
            }

            const data = await response.json();
            if (data.status === "success" && transcribeResultText) {
                transcribeResultText.value = data.text;
                originalTranscriptionText = data.text;
                isTranscriptionCleaned = false;
                updateToggleTimestampsLabel();
                if (btnToggleTimestamps) btnToggleTimestamps.classList.remove("hidden");
                writeLog(`Transcription completed successfully! Result filename: ${data.filename}`, "success");
            } else {
                throw new Error(data.message || "Failed transcription status check");
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                showToast(currentGUIlang === "km" ? "ការបម្លែងសំឡេងត្រូវបានបោះបង់!" : "Transcription cancelled by user!", "warning", 3000);
                writeLog("Transcription cancelled by user.", "warning");
                if (transcribeResultText) {
                    transcribeResultText.value = "";
                }
            } else {
                writeLog(`Transcription failed: ${error.message}`, "error");
                alert((currentGUIlang === "km" ? "ការបម្លែងបានបរាជ័យ៖ " : "Transcription failed: ") + error.message);
                if (transcribeResultText) {
                    transcribeResultText.value = "";
                }
            }
        } finally {
            if (progressPollInterval) {
                clearInterval(progressPollInterval);
            }
            if (transcribeProgressIndicator) {
                transcribeProgressIndicator.classList.add("hidden");
            }
            isTranscribing = false;
            transcribeAbortController = null;
            btnStartTranscribe.classList.remove("btn-transcribing-stop");
            btnStartTranscribe.innerHTML = originalHTML;
        }
    }

    function copyTranscriptionToClipboard() {
        if (!transcribeResultText || !transcribeResultText.value.trim()) {
            alert(currentGUIlang === "km" ? "គ្មានលទ្ធផលសម្រាប់ចម្លងឡើយ។" : "Nothing to copy.");
            return;
        }
        navigator.clipboard.writeText(transcribeResultText.value)
            .then(() => {
                alert(currentGUIlang === "km" ? "បានចម្លងទៅកាន់ Clipboard!" : "Copied to clipboard!");
                writeLog("Copied transcription result to clipboard.", "info");
            })
            .catch(err => {
                writeLog(`Failed to copy to clipboard: ${err}`, "error");
            });
    }

    function cleanTranscriptionTimestamps(text) {
        // Remove SRT timestamp lines: e.g. "00:00:05,919 --> 00:00:10,960"
        let cleaned = text.replace(/\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}/g, "");
        // Remove LRC timestamps: e.g. "[00:05.91]"
        cleaned = cleaned.replace(/\[\d{2,}:\d{2}(?:\.\d{2,3})?\]/g, "");
        // Remove SRT sequence numbers (digit-only lines)
        let lines = cleaned.split("\n");
        let resultLines = [];
        for (let line of lines) {
            let trimmed = line.trim();
            if (/^\d+$/.test(trimmed)) {
                continue;
            }
            if (trimmed === "") {
                continue;
            }
            resultLines.push(trimmed);
        }
        return resultLines.join(" ");
    }

    function updateToggleTimestampsLabel() {
        if (!lblToggleTimestamps) return;
        if (isTranscriptionCleaned) {
            lblToggleTimestamps.setAttribute("data-translate", "btn_restore_timestamps");
            lblToggleTimestamps.textContent = currentGUIlang === "km" ? "ស្តារពេលវេលាឡើងវិញ" : "Restore Timestamps";
        } else {
            lblToggleTimestamps.setAttribute("data-translate", "btn_clean_timestamps");
            lblToggleTimestamps.textContent = currentGUIlang === "km" ? "លុបម៉ោងចេញ" : "Clean Timestamps";
        }
    }

    function downloadTranscriptionFile() {
        if (!transcribeResultText || !transcribeResultText.value.trim()) {
            alert(currentGUIlang === "km" ? "គ្មានលទ្ធផលដើម្បីរក្សាទុកឡើយ។" : "No transcription result to save.");
            return;
        }

        const text = transcribeResultText.value;
        const format = selectTranscribeFormat ? selectTranscribeFormat.value : "srt";
        
        let mimeType = "text/plain";
        let defaultFilename = `transcription.${format}`;

        if (transcribeFilename) {
            const dotIdx = transcribeFilename.lastIndexOf(".");
            const baseName = dotIdx !== -1 ? transcribeFilename.substring(0, dotIdx) : transcribeFilename;
            defaultFilename = `${baseName}.${format}`;
        }

        if (format === "srt") {
            mimeType = "application/x-subrip";
        } else if (format === "lrc") {
            mimeType = "text/lrc";
        }

        const blob = new Blob([text], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = defaultFilename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        writeLog(`Downloaded transcription file: ${defaultFilename}`, "success");
    }

    // --- DRAG & DROP CLONING ZONE ---
    function setupDropzoneCloning() {
        dropzone.addEventListener("click", () => fileInput.click());
        
        fileInput.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                processReferenceFile(e.target.files[0]);
            }
        });
        
        dropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropzone.classList.add("dragover");
        });
        
        dropzone.addEventListener("dragleave", () => {
            dropzone.classList.remove("dragover");
        });
        
        dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropzone.classList.remove("dragover");
            if (e.dataTransfer.files.length > 0) {
                processReferenceFile(e.dataTransfer.files[0]);
            }
        });
        
        btnRemoveAudio.addEventListener("click", (e) => {
            e.stopPropagation();
            fileInput.value = "";
            selectedReferenceAudioBase64 = null;
            inputRefTranscript.value = "";
            selectClonedVoices.value = "none";
            fileLoadedInfo.classList.add("hidden");
            dropzone.classList.remove("hidden");
            voiceSaveGroup.classList.add("hidden");
            valClonePreview.textContent = TRANSLATIONS[currentGUIlang].clone_none;
            writeLog("Removed vocal cloning reference file.", "info");
        });
        
        // Save Cloned Voice Preset Handler
        btnSaveClonedVoice.addEventListener("click", async () => {
            const name = inputNewVoiceName.value.trim();
            if (!name) {
                alert(currentGUIlang === "km" ? "សូមបញ្ចូលឈ្មោះសំឡេងចម្លង" : "Please enter a name for the cloned voice.");
                return;
            }
            if (!selectedReferenceAudioBase64) {
                alert(currentGUIlang === "km" ? "គ្មានឯកសារសំឡេងយោង" : "No reference audio file found.");
                return;
            }
            
            btnSaveClonedVoice.disabled = true;
            const originalHTML = btnSaveClonedVoice.innerHTML;
            btnSaveClonedVoice.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Saving...';
            
            try {
                let audioBase64 = selectedReferenceAudioBase64;
                // If it is a relative path (e.g. preset file path), convert to base64 first
                if (!selectedReferenceAudioBase64.startsWith("data:")) {
                    try {
                        const fileRes = await fetch(selectedReferenceAudioBase64);
                        if (fileRes.ok) {
                            const blob = await fileRes.blob();
                            const reader = new FileReader();
                            const base64Promise = new Promise((resolve, reject) => {
                                reader.onloadend = () => resolve(reader.result);
                                reader.onerror = reject;
                                reader.readAsDataURL(blob);
                            });
                            audioBase64 = await base64Promise;
                        }
                    } catch (err) {
                        console.error("Failed to read relative audio file as base64:", err);
                    }
                }
                
                let audioUrl = selectedReferenceAudioBase64;
                const res = await fetch("/api/clones/upload", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: name,
                        audio_base64: audioBase64,
                        transcript: inputRefTranscript.value.trim()
                    })
                });
                if (!res.ok) {
                    throw new Error(await res.text());
                }
                const data = await res.json();
                if (data.success) {
                    audioUrl = data.audio_url;
                }
                
                saveClonedVoice(name, audioUrl, inputRefTranscript.value.trim());
                writeLog(`Saved cloned voice preset: ${name}`, "success");
                
                refreshClonedVoicesDropdown();
                
                const savedList = getSavedClonedVoices();
                selectClonedVoices.value = `custom_${savedList.length - 1}`;
                valClonePreview.textContent = name;
                
                voiceSaveGroup.classList.add("hidden");
                inputNewVoiceName.value = "";
            } catch (err) {
                console.error("Failed to save preset", err);
                writeLog(`Failed to save cloned voice preset: ${err.message}`, "error");
                alert(`Error: ${err.message}`);
            } finally {
                btnSaveClonedVoice.disabled = false;
                btnSaveClonedVoice.innerHTML = originalHTML;
            }
        });
    }
    
    function deleteClonedVoiceFile(audioUrl) {
        if (audioUrl && audioUrl.startsWith("/presets/")) {
            fetch("/api/clones/delete", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ audio_url: audioUrl })
            }).catch(err => console.error("Failed to delete preset file from server", err));
        }
    }
    
    function getSavedClonedVoices() {
        return savedClonedVoicesList;
    }
    
    function saveClonedVoice(name, audio, transcript) {
        // Prevent duplicate addition in memory
        if (!savedClonedVoicesList.some(v => v.name === name && v.audio === audio)) {
            savedClonedVoicesList.push({ name, audio, transcript });
        }
        // Sync to localStorage as a fallback backup
        localStorage.setItem("saved_cloned_voices", JSON.stringify(savedClonedVoicesList));
    }
    
    function refreshClonedVoicesDropdown() {
        selectClonedVoices.innerHTML = "";
        const dict = TRANSLATIONS[currentGUIlang];
        
        const optNone = document.createElement("option");
        optNone.value = "none";
        optNone.textContent = dict.clone_none;
        selectClonedVoices.appendChild(optNone);
        
        const optV1 = document.createElement("option");
        optV1.value = "voice1";
        optV1.textContent = currentGUIlang === "km" ? "សំឡេង Sinn Sisamouth" : "Sinn Sisamouth Clone";
        selectClonedVoices.appendChild(optV1);
        
        const optV2 = document.createElement("option");
        optV2.value = "voice2";
        optV2.textContent = currentGUIlang === "km" ? "សំឡេង Ros Serey Sothea" : "Ros Serey Sothea Clone";
        selectClonedVoices.appendChild(optV2);
        
        const optV3 = document.createElement("option");
        optV3.value = "voice3";
        optV3.textContent = currentGUIlang === "km" ? "អ្នកអានព័ត៌មានប្រុស" : "News Anchor Male";
        selectClonedVoices.appendChild(optV3);
        
        const optV4 = document.createElement("option");
        optV4.value = "voice4";
        optV4.textContent = currentGUIlang === "km" ? "អ្នកអានព័ត៌មានស្រី" : "News Anchor Female";
        selectClonedVoices.appendChild(optV4);
        
        const savedVoices = getSavedClonedVoices();
        if (savedVoices.length > 0) {
            const group = document.createElement("optgroup");
            group.label = currentGUIlang === "km" ? "សំឡេងដែលបានរក្សាទុក" : "Saved Cloned Voices";
            
            savedVoices.forEach((v, index) => {
                const opt = document.createElement("option");
                opt.value = `custom_${index}`;
                opt.textContent = v.name;
                group.appendChild(opt);
            });
            selectClonedVoices.appendChild(group);
        }
    }
    
    async function syncClonedVoicesFromServer() {
        try {
            // 1. Fetch registry from server
            const res = await fetch("/api/clones/list");
            if (!res.ok) throw new Error("Server returned error status");
            const data = await res.json();
            
            let serverList = [];
            if (data.success && Array.isArray(data.presets)) {
                serverList = data.presets;
            }
            
            // 2. Load fallback list from localStorage
            let localList = [];
            const stored = localStorage.getItem("saved_cloned_voices");
            if (stored) {
                try {
                    localList = JSON.parse(stored) || [];
                } catch(e) {}
            }
            
            // 3. Migrate any local presets that are NOT on the server
            for (const localVoice of localList) {
                const alreadyOnServer = serverList.some(
                    sv => sv.name === localVoice.name || sv.audio === localVoice.audio
                );
                if (!alreadyOnServer) {
                    writeLog(`Migrating local preset "${localVoice.name}" to server...`, "info");
                    try {
                        let finalAudioUrl = localVoice.audio;
                        if (localVoice.audio && localVoice.audio.startsWith("data:")) {
                            // Upload base64 audio to server
                            const uploadRes = await fetch("/api/clones/upload", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    name: localVoice.name,
                                    audio_base64: localVoice.audio,
                                    transcript: localVoice.transcript || ""
                                })
                            });
                            if (uploadRes.ok) {
                                const uploadData = await uploadRes.json();
                                if (uploadData.success) {
                                    finalAudioUrl = uploadData.audio_url;
                                }
                            }
                        } else if (localVoice.audio && !localVoice.audio.startsWith("data:")) {
                            // Convert relative path to base64 and upload to server
                            try {
                                const fileRes = await fetch(localVoice.audio);
                                if (fileRes.ok) {
                                    const blob = await fileRes.blob();
                                    const reader = new FileReader();
                                    const base64Promise = new Promise((resolve, reject) => {
                                        reader.onloadend = () => resolve(reader.result);
                                        reader.onerror = reject;
                                        reader.readAsDataURL(blob);
                                    });
                                    const base64Data = await base64Promise;
                                    
                                    const uploadRes = await fetch("/api/clones/upload", {
                                        method: "POST",
                                        headers: { "Content-Type": "application/json" },
                                        body: JSON.stringify({
                                            name: localVoice.name,
                                            audio_base64: base64Data,
                                            transcript: localVoice.transcript || ""
                                        })
                                    });
                                    if (uploadRes.ok) {
                                        const uploadData = await uploadRes.json();
                                        if (uploadData.success) {
                                            finalAudioUrl = uploadData.audio_url;
                                        }
                                    }
                                }
                            } catch (err) {
                                console.error(`Failed to fetch and sync audio file for ${localVoice.name}:`, err);
                            }
                        }
                    } catch (err) {
                        console.error(`Migration failed for ${localVoice.name}:`, err);
                    }
                }
            }
            
            // Re-fetch registry list after migration to make sure we are fully synced
            const finalRes = await fetch("/api/clones/list");
            if (finalRes.ok) {
                const finalData = await finalRes.ok ? await finalRes.json() : null;
                if (finalData && finalData.success && Array.isArray(finalData.presets)) {
                    serverList = finalData.presets;
                }
            }
            
            savedClonedVoicesList = serverList;
            localStorage.setItem("saved_cloned_voices", JSON.stringify(savedClonedVoicesList));
            refreshClonedVoicesDropdown();
            writeLog("Cloned voice presets synchronized successfully from server.", "success");
        } catch (err) {
            console.error("Failed to synchronize cloned voices from server:", err);
            let localList = [];
            const stored = localStorage.getItem("saved_cloned_voices");
            if (stored) {
                try {
                    localList = JSON.parse(stored) || [];
                } catch(e) {}
            }
            savedClonedVoicesList = localList;
            refreshClonedVoicesDropdown();
            writeLog("Synchronizer failed. Loaded backup presets from local storage.", "warning");
        }
    }
    
    function processReferenceFile(file) {
        if (!file.type.startsWith("audio/") && !file.name.endsWith(".mp3") && !file.name.endsWith(".wav") && !file.name.endsWith(".m4a")) {
            writeLog("Error: reference file must be an audio file.", "error");
            return;
        }
        
        loadedFileName.textContent = file.name;
        dropzone.classList.add("hidden");
        fileLoadedInfo.classList.remove("hidden");
        valClonePreview.textContent = "Custom File Loaded";
        
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            selectedReferenceAudioBase64 = reader.result;
            writeLog(`Loaded reference audio clip: ${file.name} for cloning.`, "success");
            
            // Show save group and pre-fill voice name
            voiceSaveGroup.classList.remove("hidden");
            const baseName = file.name.substring(0, file.name.lastIndexOf('.')) || file.name;
            inputNewVoiceName.value = baseName;
        };
    }
    
    // --- DRAG & DROP FILE IMPORT ZONE ---
    function setupDropzoneFileImport() {
        fileImportDropzone.addEventListener("click", () => fileImportInput.click());
        
        fileImportInput.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                processImportFile(e.target.files[0]);
            }
        });
        
        fileImportDropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            fileImportDropzone.classList.add("dragover");
        });
        
        fileImportDropzone.addEventListener("dragleave", () => {
            fileImportDropzone.classList.remove("dragover");
        });
        
        fileImportDropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            fileImportDropzone.classList.remove("dragover");
            if (e.dataTransfer.files.length > 0) {
                processImportFile(e.dataTransfer.files[0]);
            }
        });
        
        btnRemoveImport.addEventListener("click", (e) => {
            e.stopPropagation();
            fileImportInput.value = "";
            fileImportLoadedInfo.classList.add("hidden");
            fileImportDropzone.classList.remove("hidden");
            writeLog("Removed imported script file.", "info");
        });
    }
    
    function processImportFile(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        const allowed = ['txt', 'srt', 'vtt', 'docx'];
        
        if (!allowed.includes(extension)) {
            writeLog(`Error: File extension .${extension} not supported for script imports.`, "error");
            return;
        }
        
        loadedImportFileName.textContent = file.name;
        fileImportDropzone.classList.add("hidden");
        fileImportLoadedInfo.classList.remove("hidden");
        
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => {
            textInput.value = reader.result;
            updateTextStats();
            writeLog(`Successfully imported script file: ${file.name} (${reader.result.length} chars).`, "success");
        };
        reader.onerror = () => {
            writeLog(`Failed to parse script import: ${file.name}`, "error");
        };
    }
    
    // --- SYSTEM STATUS PROBING ---
    async function pollServicesStatus() {
        try {
            const res = await fetch("/api/status");
            const data = await res.json();
            
            updateTabStatus("voxcpm", data.voxcpm.online);
            updateTabStatus("omnivoice", data.omnivoice.online);
            updateTabStatus("fish", data.fish.online);
            
            // Check active engine connection status text
            const activeOnline = data[currentEngine].online;
            engineStatus.textContent = activeOnline ? TRANSLATIONS[currentGUIlang].connected_label : TRANSLATIONS[currentGUIlang].offline_label;
            engineStatus.className = activeOnline ? "info-badge green" : "info-badge red";
            
            // Autoconfigured weight logger
            if (data.voxcpm_local_config.detected && currentEngine === "voxcpm") {
                writeLog("VoxCPM2 Autoconfigured local model path: detected & active.", "success");
            }
            
        } catch (err) {
            updateTabStatus("voxcpm", false);
            updateTabStatus("omnivoice", false);
            updateTabStatus("fish", false);
            engineStatus.textContent = TRANSLATIONS[currentGUIlang].offline_label;
            engineStatus.className = "info-badge red";
            writeLog(`Connection to local API Gateway failed.`, "network");
        }
    }
    
    function updateTabStatus(engine, online) {
        const dot = document.getElementById(`dot-${engine}`);
        if (!dot) return;
        if (online) {
            dot.className = "tab-indicator dot-green";
        } else {
            dot.className = "tab-indicator dot-red";
        }
    }
    
    // --- HOST MEMORY CLEANUP ---
    async function handlePurgeVram() {
        writeLog("Triggering Host Cache Optimization...", "info");
        if (btnPurgeVram) btnPurgeVram.disabled = true;
        
        try {
            const res = await fetch("/api/cleanup", { method: "POST" });
            const data = await res.json();
            
            if (data.status === "success") {
                writeLog(data.message, "success");
            } else {
                writeLog("Memory optimization failed.", "error");
            }
        } catch (err) {
            writeLog(`Memory cleanup request error: ${err.message}`, "error");
        } finally {
            if (btnPurgeVram) btnPurgeVram.disabled = false;
        }
    }
    
    // --- HF MODEL DOWNLOADER POLLING ---
    async function handleStartDownload() {
        if (isDownloading) return;
        writeLog("Initializing HuggingFace Model Downloader task...", "info");
        
        try {
            const res = await fetch("/api/download", { method: "POST" });
            const data = await res.json();
            
            if (data.status === "started") {
                writeLog("Downloading process launched in background threads.", "success");
                startDownloadPolling();
            } else {
                writeLog(data.message, "warning");
            }
        } catch (err) {
            writeLog(`Downloader trigger failed: ${err.message}`, "error");
        }
    }
    
    function startDownloadPolling() {
        if (downloadPollInterval) clearInterval(downloadPollInterval);
        isDownloading = true;
        
        downloadProgressIndicator.classList.remove("hidden");
        
        downloadPollInterval = setInterval(async () => {
            try {
                const res = await fetch("/api/download-status");
                const data = await res.json();
                
                if (data.downloading) {
                    downloadPercentTxt.textContent = `${Math.round(data.percent)}%`;
                    downloadBarFill.style.width = `${data.percent}%`;
                    
                    if (data.status === "downloading") {
                        writeLog(`[DOWNLOADER] Downloading ${data.filename} - ${Math.round(data.percent)}% (${data.speed_mbps} MB/s)`, "network");
                    }
                } else {
                    clearInterval(downloadPollInterval);
                    isDownloading = false;
                    downloadProgressIndicator.classList.add("hidden");
                    
                    if (data.status === "completed") {
                        writeLog("[DOWNLOADER] Model files successfully stored in local project folders.", "success");
                        alert("Downloads completed! OmniVoice and Fish Speech weights are configured.");
                    } else if (data.status === "error") {
                        writeLog(`[DOWNLOADER] Process aborted: ${data.error}`, "error");
                        alert(`Download error: ${data.error}`);
                    }
                    pollServicesStatus(); // refresh indicators
                }
            } catch (err) {
                console.error("Download status poll failed", err);
            }
        }, 2000);
    }
    
    // --- 1-CLICK SUPER SETUP POLLING ---
    let isSettingUp = false;
    let setupPollInterval = null;

    async function handleStartSetup() {
        if (isSettingUp) return;
        writeLog("Initializing 1-Click Super Setup & Installer task...", "info");
        
        const btnSetup = document.getElementById("btn-settings-setup");
        if (btnSetup) btnSetup.disabled = true;

        try {
            const res = await fetch("/api/setup", { method: "POST" });
            const data = await res.json();
            
            if (data.status === "started") {
                writeLog("1-Click Super Setup successfully launched in background.", "success");
                startSetupPolling();
            } else {
                writeLog(data.message, "warning");
                if (btnSetup) btnSetup.disabled = false;
            }
        } catch (err) {
            writeLog(`Setup trigger failed: ${err.message}`, "error");
            if (btnSetup) btnSetup.disabled = false;
        }
    }
    
    function startSetupPolling() {
        if (setupPollInterval) clearInterval(setupPollInterval);
        isSettingUp = true;
        
        const indicator = document.getElementById("setup-progress-indicator");
        const statusTxt = document.getElementById("setup-status-txt");
        const percentTxt = document.getElementById("setup-percent-txt");
        const barFill = document.getElementById("setup-bar-fill");
        const btnSetup = document.getElementById("btn-settings-setup");

        if (indicator) indicator.classList.remove("hidden");
        
        setupPollInterval = setInterval(async () => {
            try {
                const res = await fetch("/api/setup-status");
                const data = await res.json();
                
                if (data.active) {
                    if (percentTxt) percentTxt.textContent = `${Math.round(data.percent)}%`;
                    if (barFill) barFill.style.width = `${data.percent}%`;
                    if (statusTxt) {
                        statusTxt.textContent = data.message;
                        statusTxt.title = data.message;
                    }
                    writeLog(`[SETUP PROGRESS] Phase: ${data.phase.toUpperCase()} | ${data.message} (${Math.round(data.percent)}%)`, "info");
                } else {
                    clearInterval(setupPollInterval);
                    isSettingUp = false;
                    if (indicator) indicator.classList.add("hidden");
                    if (btnSetup) btnSetup.disabled = false;
                    
                    if (data.status === "completed") {
                        writeLog("[SETUP SUCCESS] Environment setup and model downloads successfully completed!", "success");
                        alert("1-Click Super Setup completed successfully! All environment requirements and model weights are ready for use.");
                    } else if (data.status === "error" || data.phase === "error") {
                        writeLog(`[SETUP ERROR] Process aborted: ${data.message || data.error}`, "error");
                        alert(`Setup error: ${data.message || data.error}`);
                    }
                    pollServicesStatus(); // Refresh status displays
                }
            } catch (err) {
                console.error("Setup status poll failed", err);
            }
        }, 1500);
    }
    
    // --- GENERATE SPEECH ---
    async function handleGenerate() {
        if (isGeneratingSpeech) {
            if (generateAbortController) {
                generateAbortController.abort();
            }
            return;
        }

        let text = textInput.value.trim();
        if (!text) {
            writeLog("Aborted: Editor text area is empty.", "warning");
            alert("Please type some text.");
            return;
        }
        
        // Apply Lexicon rules
        text = applyLexiconRules(text);
        
        isGeneratingSpeech = true;
        generateAbortController = new AbortController();
        const { signal } = generateAbortController;

        btnGenerate.classList.add("btn-generating-stop");
        const btnContentEl = btnGenerate.querySelector(".btn-content");
        const btnLoaderEl = btnGenerate.querySelector(".btn-loader");

        if (btnContentEl) btnContentEl.classList.add("hidden");
        if (btnLoaderEl) {
            btnLoaderEl.innerHTML = '<i class="fa-solid fa-circle-stop"></i> ' + (currentGUIlang === "km" ? "បញ្ឈប់ការបង្កើត (Stop)" : "Stop Generation");
            btnLoaderEl.classList.remove("hidden");
        }
        
        let customVoicePrompt = null;
        if (selectVoice.value.startsWith("designed_")) {
            const idx = parseInt(selectVoice.value.split("_")[1]);
            const list = getCustomDesignedVoices();
            customVoicePrompt = list[idx]?.prompt || null;
        }
        
        const payload = {
            engine_selection: currentEngine,
            text: text,
            expressiveness: parseInt(inputExpressiveness.value),
            style_intensity: parseInt(inputStyle.value),
            clone_fidelity: parseInt(inputFidelity.value),
            reference_audio: selectedReferenceAudioBase64,
            reference_text: inputRefTranscript.value.trim() || null,
            mock_fallback: mockFallbackCheckbox.checked,
            low_spec_mode: lowSpecCheckbox ? lowSpecCheckbox.checked : true,
            // Screenshot variables
            language: selectLanguage.value,
            voice: selectVoice.value,
            emotion: activeEmotion,
            style: activeVoiceStyle,
            speed: parseFloat(inputSpeed.value),
            pitch: parseInt(inputPitch.value),
            volume: parseInt(inputVolume.value),
            format: activeFormat,
            custom_voice_prompt: customVoicePrompt
        };
        
        writeLog(`Compiling Speech [${currentEngine.toUpperCase()}] ...`, "info");
        
        // Show processing toast notification with animated progress bar
        const processingMsg = currentGUIlang === "km" ? "កំពុងដំណើរការបំលែងទៅជាសំឡេង... សូមរង់ចាំ" : "Synthesizing Khmer speech... Please wait";
        const processToast = showToast(processingMsg, "processing");
        
        try {
            const startTime = performance.now();
            const res = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
                signal: signal
            });
            const elapsed = performance.now() - startTime;
            
            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Server error");
            }
            const data = await res.json();
            
            if (data.success) {
                // Dismiss loading indicator and show success toast
                if (processToast && processToast.close) {
                    processToast.close();
                }
                const successMsg = currentGUIlang === "km" ? "ការបំលែងត្រូវបានបញ្ចប់រួចរាល់ហើយ!" : "Speech processing completed successfully!";
                showToast(successMsg, "success", 4000);
                
                base64AudioData = data.audio;
                currentAudioUrl = data.audio_url || data.audio;
                
                // Use the same-origin static URL from the server if available, to bypass all CORS/WebAudio data URI blocks.
                if (data.audio_url) {
                    audioEl.src = data.audio_url;
                } else {
                    // Fallback to local blob conversion if audio_url is not returned
                    try {
                        const parts = base64AudioData.split(",");
                        const mimeType = parts[0].split(":")[1].split(";")[0];
                        const base64Data = parts[1];
                        const byteCharacters = atob(base64Data);
                        const byteNumbers = new Array(byteCharacters.length);
                        for (let i = 0; i < byteCharacters.length; i++) {
                            byteNumbers[i] = byteCharacters.charCodeAt(i);
                        }
                        const byteArray = new Uint8Array(byteNumbers);
                        const blob = new Blob([byteArray], { type: mimeType });
                        
                        if (audioEl.src && audioEl.src.startsWith("blob:")) {
                            URL.revokeObjectURL(audioEl.src);
                        }
                        audioEl.src = URL.createObjectURL(blob);
                    } catch (e) {
                        console.error("Blob conversion failed, falling back to data URI", e);
                        audioEl.src = base64AudioData;
                    }
                }
                
                btnPlayPause.classList.remove("disabled");
                btnDownload.classList.remove("disabled");
                
                writeLog(`Success: Synthesized in ${data.latency_ms}ms (Routing elapsed: ${Math.round(elapsed)}ms) [${data.mock ? "Procedural Fallback" : "Live Model"}]`, "success");
                writeLog(`Details: Format=${activeFormat.toUpperCase()} | Speed=${payload.speed}x | Pitch=${payload.pitch}`, "success");
                
                // Cache into synthesis history
                let audioBlob = null;
                try {
                    const parts = data.audio.split(",");
                    const mimeType = parts[0].split(":")[1].split(";")[0];
                    const base64Data = parts[1];
                    const byteCharacters = atob(base64Data);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    audioBlob = new Blob([byteArray], { type: mimeType });
                } catch (blobErr) {
                    console.error("Failed to convert dataURL to Blob:", blobErr);
                }

                const itemId = Date.now().toString() + "_" + Math.random().toString().substring(2, 6);
                const historyItem = {
                    id: itemId,
                    timestamp: new Date().toLocaleString(),
                    text: text,
                    engine: currentEngine,
                    format: activeFormat,
                    speed: payload.speed,
                    pitch: payload.pitch,
                    latency_ms: data.latency_ms,
                    audio_url: data.audio_url || data.audio,
                    mock: data.mock
                };

                if (audioBlob) {
                    saveAudioBlob(itemId, audioBlob).then(() => {
                        saveHistoryItem(historyItem);
                    }).catch(err => {
                        console.error("Failed to save audio blob to DB", err);
                        saveHistoryItem(historyItem);
                    });
                } else {
                    saveHistoryItem(historyItem);
                }
                
                progressBarFill.style.width = "0%";
                playAudio();
            } else {
                throw new Error(data.message || "Synthesis failed");
            }
        } catch (err) {
            if (processToast && processToast.close) {
                processToast.close();
            }
            if (err.name === 'AbortError') {
                const cancelMsg = currentGUIlang === "km" ? "ការបង្កើតសំឡេងត្រូវបានបោះបង់!" : "Speech generation cancelled!";
                showToast(cancelMsg, "warning", 3000);
                writeLog("Speech generation cancelled by user.", "warning");
            } else {
                const errorMsg = currentGUIlang === "km" ? `ការបំលែងបានបរាជ័យ: ${err.message}` : `Synthesis failed: ${err.message}`;
                showToast(errorMsg, "error", 5000);
                writeLog(`Synthesis failed: ${err.message}`, "error");
                alert(`Error: ${err.message}`);
            }
        } finally {
            isGeneratingSpeech = false;
            generateAbortController = null;
            btnGenerate.classList.remove("btn-generating-stop");
            if (btnContentEl) btnContentEl.classList.remove("hidden");
            if (btnLoaderEl) {
                btnLoaderEl.classList.add("hidden");
            }
        }
    }
    
    // --- AUDIO PLAYER CONTROLS ---
    function setupAudioPlayer() {
        btnPlayPause.addEventListener("click", () => {
            if (btnPlayPause.classList.contains("disabled")) return;
            if (audioEl.paused) {
                playAudio();
            } else {
                pauseAudio();
            }
        });
        
        audioEl.addEventListener("timeupdate", () => {
            const current = audioEl.currentTime;
            const total = audioEl.duration || 0;
            
            currentTimeEl.textContent = formatTime(current);
            if (!isNaN(total)) {
                totalTimeEl.textContent = formatTime(total);
                progressBarFill.style.width = `${(current / total) * 100}%`;
            }
        });
        
        audioEl.addEventListener("loadedmetadata", () => {
            const total = audioEl.duration || 0;
            if (!isNaN(total)) {
                totalTimeEl.textContent = formatTime(total);
            }
        });
        
        audioEl.addEventListener("ended", () => {
            btnPlayPause.innerHTML = '<i class="fa-solid fa-play"></i>';
            writeLog("Playback finished.", "system");
        });
        
        volumeSlider.addEventListener("input", () => {
            audioEl.volume = volumeSlider.value;
        });
        
        progressBarContainer.addEventListener("click", (e) => {
            if (!audioEl.src || isNaN(audioEl.duration)) return;
            const rect = progressBarContainer.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const percentage = clickX / rect.width;
            audioEl.currentTime = percentage * audioEl.duration;
        });
        
        btnDownload.addEventListener("click", () => {
            if (!currentAudioUrl) return;
            triggerDownload(currentAudioUrl, `digital_tts_${currentEngine}_output.${activeFormat}`);
            writeLog(`Downloaded ${activeFormat.toUpperCase()} output file.`, "success");
        });
    }
    
    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }
    
    function playAudio() {
        try {
            if (!audioCtx) {
                initAudioContext();
            }
            if (audioCtx && audioCtx.state === "suspended") {
                audioCtx.resume();
            }
        } catch (e) {
            console.error("AudioContext failed: ", e);
        }
        
        audioEl.play()
            .then(() => {
                btnPlayPause.innerHTML = '<i class="fa-solid fa-pause"></i>';
                visualizerPlaceholder.classList.add("hidden");
                if (!isVisualizing) {
                    isVisualizing = true;
                    visualize();
                }
            })
            .catch(err => {
                console.error("Play failed", err);
            });
    }
    
    function pauseAudio() {
        audioEl.pause();
        btnPlayPause.innerHTML = '<i class="fa-solid fa-play"></i>';
    }
    
    // --- CANVAS OSCILLOSCOPE SPECTRUM ---
    function initAudioContext() {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        
        audioSource = audioCtx.createMediaElementSource(audioEl);
        audioSource.connect(analyser);
        analyser.connect(audioCtx.destination);
    }
    
    function resizeCanvas() {
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
    }
    
    function visualize() {
        if (!isVisualizing) return;
        requestAnimationFrame(visualize);
        
        if (!analyser) return;
        
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        if (audioEl.paused || audioEl.ended) {
            canvasCtx.fillStyle = "rgba(9, 9, 11, 0.2)";
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
            
            canvasCtx.lineWidth = 2;
            canvasCtx.strokeStyle = "rgba(255, 255, 255, 0.15)";
            canvasCtx.beginPath();
            canvasCtx.moveTo(0, canvas.height / 2);
            canvasCtx.lineTo(canvas.width, canvas.height / 2);
            canvasCtx.stroke();
            return;
        }
        
        // Draw frequency bars spectrum
        analyser.getByteFrequencyData(dataArray);
        
        canvasCtx.fillStyle = "rgba(9, 9, 11, 0.25)";
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
        
        const barWidth = (canvas.width / bufferLength) * 1.5;
        let barHeight;
        let x = 0;
        
        for (let i = 0; i < bufferLength; i++) {
            barHeight = (dataArray[i] / 255) * canvas.height * 0.85;
            
            const percent = i / bufferLength;
            const hue = 210 + (percent * 40); // Cool slate blues
            
            canvasCtx.shadowBlur = 12;
            canvasCtx.shadowColor = `hsla(${hue}, 90%, 65%, 0.2)`;
            canvasCtx.fillStyle = `hsla(${hue}, 85%, 65%, 0.9)`;
            
            const y = (canvas.height / 2) - (barHeight / 2);
            canvasCtx.fillRect(x, y, barWidth - 2, barHeight);
            
            x += barWidth;
        }
        canvasCtx.shadowBlur = 0;
    }
    
    function writeLog(message, type = "info") {
        const line = document.createElement("div");
        line.className = `terminal-line ${type}`;
        const timestamp = new Date().toLocaleTimeString([], {hour12: false});
        line.innerHTML = `[${timestamp}] [${type.toUpperCase()}] ${message}`;
        terminalOutput.appendChild(line);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
    
    // --- DESIGNED VOICES DATA MANAGEMENT ---
    function getCustomDesignedVoices() {
        const stored = localStorage.getItem("custom_designed_voices");
        if (stored) {
            try { return JSON.parse(stored); } catch (e) { return []; }
        }
        return [];
    }
    
    function saveCustomDesignedVoice(name, prompt) {
        const list = getCustomDesignedVoices();
        list.push({ name, prompt });
        localStorage.setItem("custom_designed_voices", JSON.stringify(list));
    }
    
    function refreshVoiceDropdown() {
        const dict = TRANSLATIONS[currentGUIlang];
        selectVoice.innerHTML = "";
        
        const optDefault = document.createElement("option");
        optDefault.value = "default";
        optDefault.textContent = dict.voice_default || "Default Voice";
        selectVoice.appendChild(optDefault);
        
        const optSokha = document.createElement("option");
        optSokha.value = "sokha";
        optSokha.textContent = dict.voice_sokha || "Sokha (Male)";
        selectVoice.appendChild(optSokha);
        
        const optSreypich = document.createElement("option");
        optSreypich.value = "sreypich";
        optSreypich.textContent = dict.voice_sreypich || "Sreypich (Female)";
        selectVoice.appendChild(optSreypich);
        
        const optSokly = document.createElement("option");
        optSokly.value = "sokly";
        optSokly.textContent = dict.voice_sokly || "Sokly (Female)";
        selectVoice.appendChild(optSokly);
        
        const customList = getCustomDesignedVoices();
        if (customList.length > 0) {
            const group = document.createElement("optgroup");
            group.label = currentGUIlang === "km" ? "សំឡេងដែលបានរចនា" : "Designed Custom Voices";
            customList.forEach((v, index) => {
                const opt = document.createElement("option");
                opt.value = `designed_${index}`;
                opt.textContent = v.name;
                group.appendChild(opt);
            });
            selectVoice.appendChild(group);
        }
    }
    
    // --- WORKSPACE VIEW ROUTER ---
    function renderSettingsVoices() {
        const designedList = document.getElementById("settings-designed-list");
        const clonedList = document.getElementById("settings-cloned-list");
        if (!designedList || !clonedList) return;
        
        // Render Designed Voices
        const customDesigned = getCustomDesignedVoices();
        if (customDesigned.length === 0) {
            designedList.innerHTML = `<div style="font-size: 0.75rem; color: var(--text-muted); padding: 0.5rem 0;">No designed voices saved.</div>`;
        } else {
            designedList.innerHTML = "";
            customDesigned.forEach((v, index) => {
                const row = document.createElement("div");
                row.style.display = "flex";
                row.style.justifyContent = "space-between";
                row.style.alignItems = "center";
                row.style.background = "rgba(255, 255, 255, 0.01)";
                row.style.border = "1px solid var(--border-soft)";
                row.style.borderRadius = "4px";
                row.style.padding = "0.5rem 0.75rem";
                row.style.marginBottom = "0.25rem";
                
                row.innerHTML = `
                    <div style="flex: 1; min-width: 0; padding-right: 0.5rem;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-pure); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${v.name}</div>
                        <div style="font-size: 0.7rem; color: var(--text-dim); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${v.prompt}</div>
                    </div>
                    <div style="display: flex; gap: 0.25rem; flex-shrink: 0;">
                        <button class="btn-rename-voice-item" style="background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.2); color: var(--accent-cyan); border-radius: 4px; padding: 0.25rem 0.5rem; font-size: 0.7rem; cursor: pointer; font-weight: 600;">
                            Rename
                        </button>
                        <button class="btn-remove-voice-item" style="background: rgba(255,77,77,0.1); border: 1px solid rgba(255,77,77,0.2); color: #ff4d4d; border-radius: 4px; padding: 0.25rem 0.5rem; font-size: 0.7rem; cursor: pointer; font-weight: 600;">
                            Delete
                        </button>
                    </div>
                `;
                
                row.querySelector(".btn-rename-voice-item").addEventListener("click", () => {
                    const newName = prompt(`Enter new name for designed voice profile "${v.name}":`, v.name);
                    if (newName && newName.trim()) {
                        v.name = newName.trim();
                        localStorage.setItem("custom_designed_voices", JSON.stringify(customDesigned));
                        writeLog(`Renamed designed voice profile to: ${v.name}`, "info");
                        refreshVoiceDropdown();
                        renderSettingsVoices();
                    }
                });
                
                row.querySelector(".btn-remove-voice-item").addEventListener("click", () => {
                    if (confirm(`Delete custom voice profile "${v.name}"?`)) {
                        customDesigned.splice(index, 1);
                        localStorage.setItem("custom_designed_voices", JSON.stringify(customDesigned));
                        writeLog(`Deleted designed voice profile: ${v.name}`, "warning");
                        refreshVoiceDropdown();
                        renderSettingsVoices();
                    }
                });
                
                designedList.appendChild(row);
            });
        }
        
        // Render Cloned Presets
        const customCloned = getSavedClonedVoices();
        if (customCloned.length === 0) {
            clonedList.innerHTML = `<div style="font-size: 0.75rem; color: var(--text-muted); padding: 0.5rem 0;">No cloned presets saved.</div>`;
        } else {
            clonedList.innerHTML = "";
            customCloned.forEach((v, index) => {
                const row = document.createElement("div");
                row.style.display = "flex";
                row.style.justifyContent = "space-between";
                row.style.alignItems = "center";
                row.style.background = "rgba(255, 255, 255, 0.01)";
                row.style.border = "1px solid var(--border-soft)";
                row.style.borderRadius = "4px";
                row.style.padding = "0.5rem 0.75rem";
                row.style.marginBottom = "0.25rem";
                
                row.innerHTML = `
                    <div style="flex: 1; min-width: 0; padding-right: 0.5rem;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-pure); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${v.name}</div>
                        <div style="font-size: 0.7rem; color: var(--text-dim); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${v.transcript || "No transcript"}</div>
                    </div>
                    <div style="display: flex; gap: 0.25rem; flex-shrink: 0;">
                        <button class="btn-rename-cloned-item" style="background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.2); color: var(--accent-cyan); border-radius: 4px; padding: 0.25rem 0.5rem; font-size: 0.7rem; cursor: pointer; font-weight: 600;">
                            Rename
                        </button>
                        <button class="btn-remove-cloned-item" style="background: rgba(255,77,77,0.1); border: 1px solid rgba(255,77,77,0.2); color: #ff4d4d; border-radius: 4px; padding: 0.25rem 0.5rem; font-size: 0.7rem; cursor: pointer; font-weight: 600;">
                            Delete
                        </button>
                    </div>
                `;
                
                row.querySelector(".btn-rename-cloned-item").addEventListener("click", async () => {
                    const newName = prompt(`Enter new name for cloned voice preset "${v.name}":`, v.name);
                    if (newName && newName.trim()) {
                        v.name = newName.trim();
                        try {
                            const updateRes = await fetch("/api/clones/update", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    audio_url: v.audio,
                                    new_name: v.name,
                                    new_transcript: v.transcript || ""
                                })
                            });
                            if (updateRes.ok) {
                                writeLog(`Renamed cloned voice preset to: ${v.name}`, "info");
                            } else {
                                throw new Error(await updateRes.text());
                            }
                        } catch (err) {
                            console.error("Failed to update preset name on server:", err);
                        }
                        localStorage.setItem("saved_cloned_voices", JSON.stringify(customCloned));
                        refreshClonedVoicesDropdown();
                        renderSettingsVoices();
                    }
                });
                
                row.querySelector(".btn-remove-cloned-item").addEventListener("click", () => {
                    if (confirm(`Delete cloned voice preset "${v.name}"?`)) {
                        deleteClonedVoiceFile(v.audio);
                        customCloned.splice(index, 1);
                        localStorage.setItem("saved_cloned_voices", JSON.stringify(customCloned));
                        writeLog(`Deleted cloned voice preset: ${v.name}`, "warning");
                        refreshClonedVoicesDropdown();
                        renderSettingsVoices();
                    }
                });
                
                clonedList.appendChild(row);
            });
        }
    }

    function switchTab(tabName) {
        navStudio.classList.remove("active");
        if (navTranscriber) navTranscriber.classList.remove("active");
        navHistory.classList.remove("active");
        navSettings.classList.remove("active");
        
        studioView.classList.add("hidden");
        if (transcriberView) transcriberView.classList.add("hidden");
        historyView.classList.add("hidden");
        settingsView.classList.add("hidden");
        
        if (tabName === "studio") {
            navStudio.classList.add("active");
            studioView.classList.remove("hidden");
        } else if (tabName === "transcriber") {
            if (navTranscriber) navTranscriber.classList.add("active");
            if (transcriberView) transcriberView.classList.remove("hidden");
        } else if (tabName === "history") {
            navHistory.classList.add("active");
            historyView.classList.remove("hidden");
            renderHistory();
        } else if (tabName === "settings") {
            navSettings.classList.add("active");
            settingsView.classList.remove("hidden");
            renderSettingsVoices();
        }
        writeLog(`Navigated view workspace to: ${tabName.toUpperCase()}`, "system");
    }
    
    // --- INDEXEDDB HELPER FUNCTIONS ---
    const DB_NAME = "DigitalTTSHistoryDB";
    const DB_VERSION = 1;
    const STORE_NAME = "audio_blobs";

    function initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(DB_NAME, DB_VERSION);
            request.onupgradeneeded = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains(STORE_NAME)) {
                    db.createObjectStore(STORE_NAME);
                }
            };
            request.onsuccess = (e) => {
                resolve(e.target.result);
            };
            request.onerror = (e) => {
                reject(e.target.error);
            };
        });
    }

    function saveAudioBlob(id, blob) {
        return initDB().then(db => {
            return new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, "readwrite");
                const store = tx.objectStore(STORE_NAME);
                const request = store.put(blob, id);
                request.onsuccess = () => resolve(true);
                request.onerror = () => reject(request.error);
            });
        });
    }

    function getAudioBlob(id) {
        return initDB().then(db => {
            return new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, "readonly");
                const store = tx.objectStore(STORE_NAME);
                const request = store.get(id);
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
        });
    }

    function deleteAudioBlob(id) {
        return initDB().then(db => {
            return new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, "readwrite");
                const store = tx.objectStore(STORE_NAME);
                const request = store.delete(id);
                request.onsuccess = () => resolve(true);
                request.onerror = () => reject(request.error);
            });
        });
    }

    function clearAllAudioBlobs() {
        return initDB().then(db => {
            return new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, "readwrite");
                const store = tx.objectStore(STORE_NAME);
                const request = store.clear();
                request.onsuccess = () => resolve(true);
                request.onerror = () => reject(request.error);
            });
        });
    }

    // Helper to safely trigger audio downloads using object URLs for maximum reliability
    async function triggerDownload(urlOrBase64, filename) {
        if (!urlOrBase64) return;
        
        try {
            let blob;
            if (urlOrBase64.startsWith("data:")) {
                const parts = urlOrBase64.split(",");
                const mimeType = parts[0].split(":")[1].split(";")[0];
                const base64Data = parts[1];
                const byteCharacters = atob(base64Data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                blob = new Blob([byteArray], { type: mimeType });
            } else if (urlOrBase64.startsWith("blob:")) {
                const link = document.createElement("a");
                link.href = urlOrBase64;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                return;
            } else {
                const res = await fetch(urlOrBase64);
                if (!res.ok) throw new Error(`HTTP error ${res.status}`);
                blob = await res.blob();
            }
            
            const blobUrl = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = blobUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            setTimeout(() => {
                URL.revokeObjectURL(blobUrl);
            }, 10000);
        } catch (e) {
            console.error("Direct blob download failed, falling back to legacy link", e);
            const link = document.createElement("a");
            link.href = urlOrBase64;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }

    // --- SYNTHESIS HISTORY CACHING & RENDERER ---
    function getHistory() {
        const stored = localStorage.getItem("synthesis_history");
        if (stored) {
            try { 
                const list = JSON.parse(stored);
                if (Array.isArray(list)) {
                    // Safe migration to guarantee all required properties exist
                    return list.map(item => {
                        if (!item) return null;
                        return {
                            id: item.id || Date.now().toString() + Math.random().toString(),
                            timestamp: item.timestamp || new Date().toLocaleString(),
                            text: item.text || "Generated speech",
                            engine: item.engine || "voxcpm",
                            format: item.format || "wav",
                            speed: item.speed !== undefined ? item.speed : 1.0,
                            pitch: item.pitch !== undefined ? item.pitch : 0,
                            latency_ms: item.latency_ms !== undefined ? item.latency_ms : 0,
                            audio_url: item.audio_url || item.audio || "",
                            mock: item.mock !== undefined ? item.mock : true
                        };
                    }).filter(item => item && item.id);
                }
                return []; 
            } catch (e) { 
                return []; 
            }
        }
        return [];
    }
    
    function saveHistoryItem(item) {
        // Clear large base64 data URL from the item before saving to keep localStorage small
        const itemCopy = { ...item };
        if (itemCopy.audio_url && itemCopy.audio_url.startsWith("data:")) {
            itemCopy.audio_url = "db:" + itemCopy.id;
        }
        itemCopy.audio = null; 

        const list = getHistory();
        list.unshift(itemCopy);
        if (list.length > 50) {
            const popped = list.pop();
            if (popped && popped.id) {
                deleteAudioBlob(popped.id);
            }
        }
        try {
            localStorage.setItem("synthesis_history", JSON.stringify(list));
        } catch (e) {
            console.error("Failed to save history to localStorage", e);
        }
        
        // Keep the history view updated dynamically if the user is currently viewing it
        if (document.getElementById("history-view") && !document.getElementById("history-view").classList.contains("hidden")) {
            renderHistory();
        }
    }
    
    let activePlayingHistoryAudio = null;

    function renderHistory() {
        const history = getHistory();
        if (history.length === 0) {
            historyEmpty.classList.remove("hidden");
            historyList.classList.add("hidden");
            return;
        }
        
        historyEmpty.classList.add("hidden");
        historyList.classList.remove("hidden");
        historyList.innerHTML = "";
        
        history.forEach(item => {
            try {
                const itemId = item.id;
                const itemTimestamp = item.timestamp;
                const itemText = item.text;
                const itemEngine = item.engine;
                const itemFormat = item.format;
                const itemSpeed = item.speed;
                const itemPitch = item.pitch;
                const itemLatency = item.latency_ms;
                const itemMock = item.mock;
                const itemAudioUrl = item.audio_url;
                
                const card = document.createElement("div");
                card.className = "history-item-card";
                card.style.background = "rgba(255, 255, 255, 0.02)";
                card.style.border = "1px solid var(--border-color)";
                card.style.borderRadius = "12px";
                card.style.padding = "1.25rem";
                card.style.display = "flex";
                card.style.flexDirection = "column";
                card.style.gap = "0.75rem";
                card.style.transition = "var(--transition-smooth)";
                
                card.addEventListener("mouseenter", () => {
                    card.style.borderColor = "var(--accent-purple)";
                    card.style.background = "rgba(255, 255, 255, 0.04)";
                });
                card.addEventListener("mouseleave", () => {
                    card.style.borderColor = "var(--border-color)";
                    card.style.background = "rgba(255, 255, 255, 0.02)";
                });
                
                const header = document.createElement("div");
                header.style.display = "flex";
                header.style.justifyContent = "space-between";
                header.style.alignItems = "center";
                
                const leftHeaderGroup = document.createElement("div");
                leftHeaderGroup.style.display = "flex";
                leftHeaderGroup.style.alignItems = "center";
                leftHeaderGroup.style.gap = "0.5rem";
                
                const selectChk = document.createElement("input");
                selectChk.type = "checkbox";
                selectChk.className = "history-select-chk";
                selectChk.value = itemAudioUrl;
                selectChk.style.cursor = "pointer";
                selectChk.style.width = "16px";
                selectChk.style.height = "16px";
                
                const badge = document.createElement("span");
                badge.className = "info-badge";
                badge.style.fontSize = "0.75rem";
                badge.style.padding = "0.25rem 0.6rem";
                badge.style.borderRadius = "6px";
                badge.style.fontWeight = "700";
                
                if (itemEngine === "voxcpm") {
                    badge.textContent = "VoxCPM2";
                    badge.style.background = "rgba(139, 92, 246, 0.15)";
                    badge.style.color = "var(--accent-purple)";
                } else if (itemEngine === "omnivoice") {
                    badge.textContent = "OmniVoice";
                    badge.style.background = "rgba(6, 182, 212, 0.15)";
                    badge.style.color = "var(--accent-cyan)";
                } else {
                    badge.textContent = itemEngine === "merged" ? "Merged" : "Fish Speech";
                    badge.style.background = itemEngine === "merged" ? "rgba(6, 182, 212, 0.15)" : "rgba(16, 185, 129, 0.15)";
                    badge.style.color = itemEngine === "merged" ? "var(--accent-cyan)" : "var(--accent-emerald)";
                }
                
                const timeSpan = document.createElement("span");
                timeSpan.textContent = itemTimestamp;
                timeSpan.style.fontSize = "0.75rem";
                timeSpan.style.color = "var(--text-muted)";
                
                leftHeaderGroup.appendChild(selectChk);
                leftHeaderGroup.appendChild(badge);
                header.appendChild(leftHeaderGroup);
                header.appendChild(timeSpan);
                
                const textBlock = document.createElement("p");
                textBlock.textContent = itemText;
                textBlock.style.fontSize = "0.85rem";
                textBlock.style.color = "var(--text-primary)";
                textBlock.style.lineHeight = "1.4";
                textBlock.style.whiteSpace = "nowrap";
                textBlock.style.overflow = "hidden";
                textBlock.style.textOverflow = "ellipsis";
                
                const meta = document.createElement("div");
                meta.style.fontSize = "0.75rem";
                meta.style.color = "var(--text-muted)";
                meta.style.display = "flex";
                meta.style.gap = "1rem";
                meta.style.flexWrap = "wrap";
                meta.innerHTML = `
                    <span><strong>Format</strong>: ${itemFormat.toUpperCase()}</span>
                    <span><strong>Speed</strong>: ${itemSpeed}x</span>
                    <span><strong>Pitch</strong>: ${itemPitch}</span>
                    <span><strong>Latency</strong>: ${itemLatency}ms</span>
                    <span><strong>Mode</strong>: ${itemMock ? "Fallback" : "Neural"}</span>
                `;
                
                const actions = document.createElement("div");
                actions.style.display = "flex";
                actions.style.gap = "0.75rem";
                actions.style.marginTop = "0.25rem";
                
                const playBtn = document.createElement("button");
                playBtn.className = "btn-lang";
                playBtn.innerHTML = '<i class="fa-solid fa-play"></i> Play';
                playBtn.style.padding = "0.4rem 0.8rem";
                
                let itemAudioEl = null;
                let activeBlobUrl = null;
                
                async function initHistoryAudio() {
                    if (itemAudioEl) return itemAudioEl;
                    
                    try {
                        const blob = await getAudioBlob(itemId);
                        if (blob) {
                            activeBlobUrl = URL.createObjectURL(blob);
                            itemAudioEl = new Audio(activeBlobUrl);
                        }
                    } catch (dbErr) {
                        console.warn("Could not load from IndexedDB:", dbErr);
                    }
                    
                    if (!itemAudioEl) {
                        if (itemAudioUrl && !itemAudioUrl.startsWith("db:")) {
                            itemAudioEl = new Audio(itemAudioUrl);
                        } else {
                            throw new Error("Audio data not found in DB or server");
                        }
                    }
                    
                    itemAudioEl.addEventListener("ended", () => {
                        playBtn.innerHTML = '<i class="fa-solid fa-play"></i> Play';
                    });
                    
                    return itemAudioEl;
                }
                
                playBtn.addEventListener("click", async () => {
                    try {
                        const audioElObj = await initHistoryAudio();
                        if (audioElObj.paused) {
                            audioEl.pause();
                            
                            if (activePlayingHistoryAudio && activePlayingHistoryAudio !== audioElObj) {
                                activePlayingHistoryAudio.pause();
                            }
                            
                            document.querySelectorAll(".history-item-card button").forEach(btn => {
                                if (btn.innerHTML.includes("Pause")) {
                                    btn.innerHTML = '<i class="fa-solid fa-play"></i> Play';
                                }
                            });
                            
                            activePlayingHistoryAudio = audioElObj;
                            
                            audioElObj.play()
                                .then(() => {
                                    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause';
                                    writeLog(`Playing history synthesis: ${itemText.substring(0, 30)}...`, "system");
                                })
                                .catch(err => console.error("Play failed", err));
                        } else {
                            audioElObj.pause();
                            playBtn.innerHTML = '<i class="fa-solid fa-play"></i> Play';
                        }
                    } catch (playErr) {
                        console.error("Audio init/play failed:", playErr);
                        writeLog(`Could not play: Audio file has expired on the server.`, "error");
                        alert("Play failed: Audio file has expired on the server.");
                    }
                });
                
                const downloadBtn = document.createElement("button");
                downloadBtn.className = "btn-lang";
                downloadBtn.innerHTML = '<i class="fa-solid fa-download"></i> Download';
                downloadBtn.style.padding = "0.4rem 0.8rem";
                downloadBtn.addEventListener("click", async () => {
                    try {
                        const blob = await getAudioBlob(itemId);
                        if (blob) {
                            const blobUrl = URL.createObjectURL(blob);
                            await triggerDownload(blobUrl, `digital_tts_${itemEngine}_history.${itemFormat}`);
                            setTimeout(() => URL.revokeObjectURL(blobUrl), 10000);
                        } else {
                            if (itemAudioUrl && !itemAudioUrl.startsWith("db:")) {
                                await triggerDownload(itemAudioUrl, `digital_tts_${itemEngine}_history.${itemFormat}`);
                            } else {
                                alert("Download failed: Audio data has expired.");
                            }
                        }
                    } catch (err) {
                        console.error("Download failed:", err);
                        alert("Download failed.");
                    }
                });
                
                const deleteBtn = document.createElement("button");
                deleteBtn.className = "btn-lang";
                deleteBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i> Delete';
                deleteBtn.style.padding = "0.4rem 0.8rem";
                deleteBtn.style.borderColor = "rgba(255, 77, 77, 0.2)";
                deleteBtn.style.color = "#ff4d4d";
                deleteBtn.addEventListener("click", () => {
                    if (itemAudioEl) {
                        itemAudioEl.pause();
                    }
                    if (activeBlobUrl) {
                        URL.revokeObjectURL(activeBlobUrl);
                    }
                    deleteHistoryItem(itemId);
                    renderHistory();
                });
                
                actions.appendChild(playBtn);
                actions.appendChild(downloadBtn);
                actions.appendChild(deleteBtn);
                
                card.appendChild(header);
                card.appendChild(textBlock);
                card.appendChild(meta);
                card.appendChild(actions);
                
                historyList.appendChild(card);
            } catch (cardErr) {
                console.error("Failed to render history item:", cardErr, item);
            }
        });
    }
    
    function deleteHistoryItem(id) {
        const list = getHistory();
        const filtered = list.filter(item => item.id !== id);
        localStorage.setItem("synthesis_history", JSON.stringify(filtered));
        writeLog("Deleted synthesis history record.", "warning");
        deleteAudioBlob(id);
    }
    
    function clearAllHistory() {
        if (confirm("Are you sure you want to purge all speech synthesis history?")) {
            localStorage.setItem("synthesis_history", "[]");
            writeLog("Purged all speech synthesis history records.", "warning");
            clearAllAudioBlobs();
            renderHistory();
        }
    }
    
    // --- TOAST NOTIFICATIONS SYSTEM ---
    function showToast(message, type = "info", duration = 4000) {
        let container = document.querySelector(".toast-container");
        if (!container) {
            container = document.createElement("div");
            container.className = "toast-container";
            document.body.appendChild(container);
        }
        
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        
        let icon = '<i class="fa-solid fa-circle-info" style="color: var(--accent-cyan);"></i>';
        if (type === "success") {
            icon = '<i class="fa-solid fa-circle-check" style="color: #10b981;"></i>';
        } else if (type === "error") {
            icon = '<i class="fa-solid fa-circle-exclamation" style="color: #ef4444;"></i>';
        } else if (type === "processing") {
            icon = '<i class="fa-solid fa-circle-notch fa-spin" style="color: var(--accent-fuchsia);"></i>';
        }
        
        toast.innerHTML = `
            ${icon}
            <div class="toast-content" style="flex: 1;">${message}</div>
            <div class="toast-progress"></div>
        `;
        
        container.appendChild(toast);
        
        const progressEl = toast.querySelector(".toast-progress");
        
        if (type === "processing") {
            // Fake progress from 0% to 95% over 15 seconds
            let progress = 0;
            const interval = setInterval(() => {
                if (progress < 95) {
                    progress += 0.5;
                    progressEl.style.width = `${progress}%`;
                } else {
                    clearInterval(interval);
                }
            }, 100);
            
            toast.close = () => {
                clearInterval(interval);
                progressEl.style.width = "100%";
                setTimeout(() => {
                    toast.style.animation = "toastSlideOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
                    setTimeout(() => toast.remove(), 300);
                }, 200);
            };
        } else {
            // Standard automatic dismiss
            const startTime = Date.now();
            const interval = setInterval(() => {
                const elapsed = Date.now() - startTime;
                const percent = Math.min((elapsed / duration) * 100, 100);
                progressEl.style.width = `${percent}%`;
                if (elapsed >= duration) {
                    clearInterval(interval);
                    toast.style.animation = "toastSlideOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
                    setTimeout(() => toast.remove(), 300);
                }
            }, 50);
        }
        
        return toast;
    }
    
    init();
});
