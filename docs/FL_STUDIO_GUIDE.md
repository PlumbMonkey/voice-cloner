# FL Studio Integration Guide

Complete guide for integrating Voice Cloner output with FL Studio.

## Audio Specifications

Your converted audio is optimized for FL Studio:

```
Format: WAV (PCM)
Sample Rate: 44.1kHz
Bit Depth: 24-bit
Channels: Mono (if input was stereo)
Duration: Variable (based on input)
```

## FL Studio Setup

### Create Audio Track

```
1. File → New
2. Click on an audio track slot
3. In Mixer, insert a new audio track
4. Name it: [Voice Clone]
5. Set volume to -6dB (prevent clipping)
```

### Assign Edison Plugin

```
1. Click on audio track in Mixer
2. Right-click "Master Track" area
3. Select "Plugins" → "Edison"
4. Edison plugin window opens
```

## Edison Import Workflow

Edison is FL Studio's professional audio editor.

### Import Audio File

```
EDISON WINDOW:

  File Menu
  ├─ Open... (Ctrl+O)
  └─ Opens WAV file browser

Steps:
1. Click "File" → "Open..."
2. Navigate to your converted_vocals.wav
3. Select file
4. Click "Open"
5. Waveform appears in Edison window
```

### Workspace Layout

```
Edison Interface:

┌─────────────────────────────────────────────┐
│ [File] [Undo] [Redo] | Time: 0:00.000       │
├─────────────────────────────────────────────┤
│                                             │
│         WAVEFORM DISPLAY                   │
│    ╱╲    ╱╲╱╲    ╱╲╱╲╱╲╱╲╱╲╱╲           │
│   ╱  ╲  ╱          ╱                      │
│                                             │
├─────────────────────────────────────────────┤
│ [Play] [Export] [Insert] Tools...          │
└─────────────────────────────────────────────┘
```

## Editing Tools

### Time Stretch

Match vocal timing to your project tempo.

```
Usage:
1. Select section of waveform
2. Drag edges to adjust length
3. Edison auto-stretches without changing pitch

When to use:
- Sync vocals to drum tempo
- Speed up slow vocals
- Slow down fast vocals
```

### Pitch Shift

Adjust pitch after recording.

```
Usage:
1. Select waveform
2. Use Pitch Shift slider
3. Adjust in semitones (±12)
4. Real-time preview

When to use:
- Fine-tune pitch already trained with
- Match vocals to key change
- Create harmonies
```

### Loop Points

Mark and loop sections.

```
Usage:
1. Set loop start point (green marker)
2. Set loop end point (red marker)
3. Toggle loop button
4. Plays section repeatedly

When to use:
- Loop chorus sections
- Repeat vocal phrases
- Create layered arrangements
```

### Spectral Editing

Precise editing of frequency content.

```
Usage:
1. Switch to Spectral view
2. Select problematic areas
3. Erase or reduce unwanted frequencies
4. Apply changes

When to use:
- Remove artifacts
- Reduce harshness
- Fix frequency imbalances
```

### Fade In/Out

Smooth transitions at beginning/end.

```
Usage:
1. Drag edge of waveform
2. Creates fade curve
3. Adjust fade length

When to use:
- Smooth intro
- Smooth outro
- Prevent clicks/pops
```

## Export Process

### Export from Edison

```
Steps:
1. Complete all edits in Edison
2. Click "Export" button
3. Choose export format:
   - WAV (24-bit recommended)
   - MP3 (if compatibility needed)
4. Choose location
5. Click "Export"
6. Audio saved to file

Quality Settings:
- PCM: 24-bit (best)
- PCM: 16-bit (good)
- MP3: 320kbps (good compatibility)
```

### Import Back to FL Studio

```
After exporting:
1. Go to File browser in FL Studio
2. Browse to exported audio
3. Drag into audio track
4. Audio appears in playlist
5. Ready to arrange!
```

## Arranging in FL Studio

### Mixer Setup

```
Mixer Track Configuration:

Track 1: [Drums]
Track 2: [Bass]
Track 3: [Keys]
Track 4: [Voice Clone] ← Your converted vocals
Track 5: [Harmony 1]  ← Duplicate with +5 semitones
Track 6: [Harmony 2]  ← Duplicate with -3 semitones
Track 7: [Reverb Send] ← Effects track
Track 8: [Master]     ← Final output

Recommended Levels:
- Drums: -2 dB
- Bass: -3 dB
- Keys: -4 dB
- Voice Clone: -6 dB (important: prevent clipping)
- Harmony 1: -8 dB
- Harmony 2: -9 dB
```

### Panning

```
Stereo Width:

Left Pan (-100):     Right Pan (+100):
  Harmony 1            Harmony 2
    ↓                     ↓
    ◉═════●═════◉
         Voice Clone
         (Center: 0)

Tips:
- Center main vocal
- Pan harmonies left/right
- Creates wider, richer sound
- Leave bass/drums centered
```

## Effects

### Reverb

Adds space and depth.

```
Settings:
Type: Hall or Plate
Mix: 30-50%
Decay: 1.5-3 seconds
Pre-delay: 20-50ms

Usage:
1. Insert Reverb plugin on track
2. Adjust mix and decay
3. Listen for natural space
4. Subtle is better than extreme
```

### Delay

Adds echo/repetition.

```
Settings:
Time: 300-500ms (synced to tempo)
Feedback: 30-50%
Mix: 20-40%

Usage:
1. Insert Delay on track
2. Sync to project tempo
3. Adjust feedback for repeat count
4. Add movement to vocals
```

### Compression

Controls dynamic range.

```
Settings:
Ratio: 4:1
Attack: 10-20ms
Release: 100-200ms
Threshold: -20dB

Usage:
1. Insert Compressor
2. Set threshold where peaks compress
3. Ratio controls intensity
4. Tames loud peaks, controls dynamics
```

### EQ

Shapes tone.

```
Common Adjustments:
- 100Hz: Reduce mud, thin out low end
- 1-2kHz: Presence peak, makes brighter
- 3-5kHz: Clarity boost
- 10kHz: Air/shimmer top end

Technique:
1. Use subtractive EQ (cut rather than boost)
2. Small cuts (3dB) more natural than boosts
3. Compare with reference
4. A/B toggle bypass
```

### Distortion

Adds character/aggression.

```
Settings:
Amount: 10-30% (subtle)
Tone: Varies by plugin
Mix: 20-50% blend with original

Usage:
- Light distortion: Character
- Heavy distortion: Effect/style
- Mix with clean for balance
```

## Layering Techniques

### Create Harmonies

```
1. Duplicate audio track with voice
2. Use different checkpoint model
3. Or use same model with different pitch shift:
   - Main: 0 semitones
   - Harmony 1: +5 semitones
   - Harmony 2: -3 semitones
4. Pan left and right
5. Blend volumes
6. Add reverb to harmonies

Result: Full, rich vocal sound
```

### Double Tracking

```
1. Import same vocal twice
2. Shift one by 5-10ms (delay)
3. Small pitch shift on second (±1-2 semitones)
4. Pan left and right
5. Creates wider, fatter sound
```

### Background Vocals

```
1. Create simplified melody
2. Convert to AI vocals
3. Layer underneath
4. Lower volume (-10dB)
5. Add more reverb than lead
6. Creates depth and support
```

## Mixing Tips

### Vocal Leveling

```
1. Set Master to -3dB headroom
2. Voice Clone track: -6dB starting point
3. Play your mix
4. Adjust until vocals sit well
5. Not too loud (distortion)
6. Not too quiet (gets lost)

Golden Rule: Vocals should be most prominent
```

### EQ Workflow

```
FIRST PASS (Subtractive):
1. Load EQ plugin
2. Play vocal
3. Find problem frequencies
4. Cut 3-6dB at problem area
5. A/B toggle to verify

SECOND PASS (Additive):
1. Use different EQ or chain
2. Subtle boosts (1-2dB) if needed
3. Don't overdo it
4. Compare with reference vocals
```

### Level Automation

```
Create dynamics in automation:
1. Create automation lane on vocal track
2. Click points on volume automation
3. Create volume envelope:
   - Raise for important sections
   - Lower during busy sections
   - Smooth curves between

Result: Vocal presence stays consistent
```

### Reference Monitoring

```
Setup for quality checking:
1. Use studio monitors
2. Mix at moderate levels (85dB)
3. Take breaks (ears fatigue)
4. Use reference tracks
5. Compare your mix to professional vocals
6. Check on phone speakers too
```

## Exporting Your Project

### Stereo Mix Export

```
Steps:
1. View → Master Channel
2. Click Master track
3. File → Export → Wave File
4. Settings:
   - Sample Rate: 44.1kHz
   - Bit Depth: 24-bit
   - Format: WAV
5. Choose filename and location
6. Click "Export"
7. Your mix is ready!
```

### Uploading to Distribution

```
Audio Specifications:
- Format: WAV or MP3
- Sample Rate: 44.1kHz
- Bit Depth: 16-bit minimum
- Loudness: -14 LUFS (loudness standard)
- File Size: Keep under 100MB

Platforms:
- DistroKid
- CD Baby
- CDBaby
- Tunecore
- Yourself (personal releases)
```

## Troubleshooting FL Studio Integration

### Audio Not Playing

```
Fix:
1. Check Master is not muted (M button)
2. Verify Speaker/headphone connected
3. Restart FL Studio
4. Check audio driver in Settings
```

### Audio Sounds Distorted

```
Fix:
1. Lower track volume (was set to -6dB, try -9dB)
2. Lower Master volume
3. Check plugins not overdriving
4. Rebuild audio driver
```

### Edison Won't Open

```
Fix:
1. Double-click audio track in Mixer
2. Or right-click → Edison
3. Verify audio file is loaded
4. Restart FL Studio
```

### Timing Issues

```
Fix:
1. Use Edison Time Stretch tool
2. Verify project tempo matches vocal tempo
3. Use Detect Beats if available
4. Manual adjustment in playlist
```

### Quality Loss

```
Prevention:
1. Always use 24-bit exports
2. Avoid re-converting multiple times
3. Mix at proper levels (-6dB headroom)
4. Use lossless formats (WAV) until final
```

## Best Practices

```
✓ DO:
- Keep backups of original files
- Save FL Studio project frequently
- Use folder hierarchies for organization
- Reference against professional vocals
- Monitor at reasonable levels
- Take breaks while mixing
- Document your settings

✗ DON'T:
- Maximize everything to 0dB
- Use maximum reverb/delay
- Over-compress vocals
- Change too many settings without A/B
- Mix at extreme volumes
- Skip backups
- Use low-quality monitoring
```

---

**Ready to create professional vocals with Voice Cloner! 🎵**
