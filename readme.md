# Live Video Transcription

**Live Video Transcription** is a cross-platform desktop application that captures system audio in real time and generates live speech-to-text transcriptions using **Whisper** (via _faster-whisper_).

The application is built with **Python**, **Kivy**, and **multithreaded audio processing**, and it supports **macOS**, **Windows**, and **Ubuntu** using OS-specific virtual audio drivers.

---

## ✨ Features

- 🎤 **Real-time system audio capture**
- 📝 **Live transcription using Whisper**
- 🖥️ **Cross-platform support**:
  - macOS → **BlackHole**
  - Windows → **VB-Audio VoiceMeeter** or **VB-Audio Virtual Cable**
  - Ubuntu → **PipeWire** (or PulseAudio) virtual sinks/monitors
- 🎛️ Device selection UI
- 🚦 Start/Stop transcription control
- ⚡ Non-blocking threaded audio pipeline
- 🪶 Lightweight UI built with **Kivy**
- 🧩 Modular architecture for easy future expansion

---

## 🔧 System Requirements

| OS          | Virtual Audio Device       | Notes                              |
| ----------- | -------------------------- | ---------------------------------- |
| **macOS**   | BlackHole                  | For internal audio loopback        |
| **Windows** | VoiceMeeter / VB-Cable     | Select the virtual output as input |
| **Ubuntu**  | PipeWire (monitor sources) | Can create null-sink loopbacks     |

Other requirements:

- Python **3.10+**
- FFmpeg available on PATH
- GPU optional (CUDA supported)
- Working microphone or virtual input device

---

## 📦 Installation

Clone the repository:

```bash
cd LiveTranscriptor

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

## 🎙️ System Audio Setup

### macOS (BlackHole)

    1.	Install BlackHole: https://existential.audio/blackhole/
    2.	Open Audio MIDI Setup
    3.	Create a Multi-Output or Aggregate device
    4.	Set macOS Output → BlackHole
    5.	In the app, select BlackHole as your input source

⸻

### Windows (VoiceMeeter / VB-Cable)

Recommended: VoiceMeeter Banana or Potato
Download: https://vb-audio.com/Voicemeeter/

Steps:
• Set system output → VoiceMeeter Input
• In the app, choose VoiceMeeter Output as the capture device

Alternative: VB-Audio Virtual Cable
• Set system output → CABLE Input
• In the app, select CABLE Output

⸻

### Ubuntu (PipeWire)

PipeWire automatically exposes monitor sources:

```bash
pactl list sources | grep -e Name -e 'Monitor'
```

You can also create your own virtual sink:

```bash
pactl load-module module-null-sink sink_name=virt_sink
pactl load-module module-loopback source=virt_sink.monitor
```

Then select virt_sink.monitor inside the app.

## ▶️ Running the Application

```bash
python main.py
```

Then:

1. Select an input device
2. Select a Whisper model
3. Click Start
4. Watch live transcription appear in real time

## 🧠 Architecture Overview

```
 ┌──────────────────────┐         ┌─────────────────────────────┐
 │   record_audio       │  --->   │     audio_queue (FIFO)      │
 │  (producer thread)   │         └─────────────────────────────┘
 └──────────────────────┘                        │
                                                 ▼
                                   ┌─────────────────────────┐
                                   │   transcript_audio      │
                                   │   (consumer thread)     │
                                   └─────────────────────────┘
```

- `record_audio` captures audio chunks and pushes them to a queue
- `transcript_audio` pulls chunks and passes them to Whisper
- UI updates are scheduled safely using Kivy's `Clock`

## 🧪 Whisper Models

This project uses **faster-whisper**, which provides:

- Very fast CPU & GPU inference
- Lower memory usage
- Streaming capabilities

Supported compute types:

- `float32`
- `float16`
- `int8` (CPU-optimized)
