# Professional Audio Engineering & Broadcast Mastering

Commercial audio requires meticulous level calibration and dynamic ducking so voiceover cuts through the music effortlessly without ever fatiguing listener ears.

---

## 1. The EBU R128 / ITU-R BS.1770 Standard

Every audio render is mastered to international broadcast targets:
- **Integrated Loudness**: `-14.0 LUFS` (optimal target for YouTube, Spotify, and streaming ads).
- **Loudness Range (LRA)**: `7.0 LU` (preserves punch without wild volume swings).
- **True Peak Maximum**: `-1.0 dBFS` (prevents inter-sample clipping upon AAC/MP3 transcoding).

---

## 2. Sidechain Ducking via FFmpeg

When voiceover speaks, background music volume smoothly decreases by 10–14 dB. When dialogue pauses, music swells back up naturally.

### FFmpeg Sidechain Filter Formula:
```bash
ffmpeg -i music.mp3 -i voiceover.wav -filter_complex \
"[0:a][1:a]sidechaincompress=threshold=0.08:ratio=6:attack=20:release=300[ducked_music]; \
 [ducked_music][1:a]amix=inputs=2:duration=first:dropout_transition=2[mixed]; \
 [mixed]loudnorm=I=-14:LRA=7:TP=-1.0[out]" \
-map "[out]" -c:a aac -b:a 320k master_output.wav
```

### Parameter Breakdown:
- `threshold=0.08`: Detects voice presence instantly.
- `ratio=6`: Compresses music by 6:1 (approx 12dB reduction).
- `attack=20`: 20ms quick fade down when speech starts (no abrupt cutting).
- `release=300`: 300ms smooth decay when speech ends (pleasant cinematic swell).

---

## 3. Micro-SFX Layering Map

Professional video editors use sound effects to anchor eye movement:

| Visual Event | Audio Sound Effect | Frequency Profile |
|--------------|-------------------|-------------------|
| Scene cut / Transition | High-speed air whoosh (`whoosh_cinematic.wav`) | High-pass filtered at 800Hz |
| Core value hook / Stat reveal | Sub-bass drop / cinematic impact (`impact_deep.wav`) | Low-pass resonant at 60Hz |
| UI Mockup Click / Tap | Tactile glass/mechanical click (`click_tactile.wav`) | Sharp transient at 2.5kHz |
| Feature cards fly-in | Subtle paper/air swish (`swish_soft.wav`) | Mid-frequency sweep |
| End Logo Reveal | Shimmer / orchestral swell (`swell_resolve.wav`) | Full spectrum release |

---

## 4. TTS Voice Calibration Table

| Engine | Recommended Voice ID | Character / Tone |
|--------|----------------------|------------------|
| Edge-TTS | `en-US-GuyNeural` | Authoritative, warm, corporate documentary |
| Edge-TTS | `en-US-AriaNeural` | Friendly, crisp, modern SaaS explainer |
| Edge-TTS | `en-GB-SoniaNeural` | Elegant, luxury, editorial agency |
| Kokoro-ONNX | `af_heart` | Studio-grade conversational podcast tone |
| Kokoro-ONNX | `am_adam` | Deep baritone keynote speaker tone |
