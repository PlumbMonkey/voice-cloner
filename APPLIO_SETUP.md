# 🎤 Voice Cloner - Quick Setup with Applio RVC

## Your System ✓
- **GPU**: NVIDIA GeForce RTX 3070 (8.6 GB) ✅
- **CUDA**: Available ✅
- **Voice Samples**: 8 files (94 MB) ready in `samples/` ✅
- **Test Vocal**: Ready in `input/` ✅

---

## Step 1: Download Applio (2-3 minutes)

**Direct Download Link:**
```
https://huggingface.co/IAHispano/Applio/resolve/main/Compiled/Windows/ApplioV3.5.1.zip
```

1. Download the ZIP file (~2 GB)
2. Extract to `C:\Applio` (or anywhere without spaces in path)
3. ⚠️ **IMPORTANT**: Temporarily disable antivirus during setup

---

## Step 2: Run Applio

1. Open the extracted folder
2. Double-click `run-applio.bat`
3. Wait for the browser window to open (first run takes a few minutes)
4. The WebUI will open at `http://127.0.0.1:7865`

---

## Step 3: Train Your Voice Model (30 min - 2 hours)

### In Applio WebUI:

1. **Go to "Training" tab**

2. **Preprocess your audio:**
   - Model Name: `my-voice`
   - Dataset Path: Browse to `D:\Dev Projects 2025\Voice Cloner\samples`
   - Sample Rate: 40000
   - Click **"Preprocess Dataset"**

3. **Extract features:**
   - F0 Method: `rmvpe` (best quality)
   - Hop Length: 128
   - Click **"Extract Features"**

4. **Train the model:**
   - Total Epochs: 300-500 (start with 300)
   - Save Every Epoch: 50
   - Batch Size: 8 (for 8GB VRAM)
   - Click **"Start Training"**

5. **Wait for training to complete** (~30 min to 2 hours)

### Training Tips:
- You can monitor loss in the console window
- Lower loss = better quality
- Training will auto-save checkpoints

---

## Step 4: Convert Vocals

1. **Go to "Inference" tab**

2. **Load your model:**
   - Model: Select `my-voice.pth`
   - Index: Select `my-voice.index`

3. **Upload audio:**
   - Audio: Browse to `D:\Dev Projects 2025\Voice Cloner\input\`
   - Select your FL Studio vocal stem

4. **Adjust settings:**
   - Pitch: 0 (adjust if needed for gender)
   - Index Ratio: 0.5 (higher = more like training voice)
   - F0 Method: `rmvpe`
   - Protect: 0.33

5. **Click "Convert"**

6. **Download the converted audio**

---

## Step 5: Use in FL Studio

1. Import the converted audio back into FL Studio
2. Place on your vocal track
3. Done! 🎉

---

## Troubleshooting

**"CUDA out of memory"**
- Reduce batch size to 4 or 6
- Close other GPU applications

**Training seems slow**
- 8GB VRAM is fine, just takes longer
- Expect 1-2 hours for good results

**Converted voice doesn't sound right**
- Train for more epochs (500+)
- Add more training samples
- Adjust pitch shift if gender mismatch

**Index file missing**
- Re-run "Extract Features" step
- Make sure to generate index during training

---

## File Locations

| What | Where |
|------|-------|
| Your samples | `D:\Dev Projects 2025\Voice Cloner\samples\` |
| Your input vocal | `D:\Dev Projects 2025\Voice Cloner\input\` |
| Applio models | `C:\Applio\logs\my-voice\` |
| Converted output | Applio "Inference" tab download |

---

## Your Voice Samples

These 8 files (94 MB total) are ready for training:
- isolated vocal.wav (11.2 MB)
- more singing.wav (11.2 MB)
- readin a song lyric.wav (7.1 MB)
- Sing v2.wav (1.7 MB)
- speech v2.wav (2.6 MB)
- 1 Introduction - The Symphony of Your Life.mp3 (13.5 MB)
- 2 Preface - The Symphony of Your Life.mp3 (16.7 MB)
- The Inner Chapters - Introduction.mp3 (30.1 MB)

---

## Next Steps After Prototype

Once you have a working voice clone:
1. Export the trained model (`.pth` and `.index` files)
2. Copy to this project's `models/` folder
3. We can build automation scripts and GUI later

---

**Questions?** Check [Applio Documentation](https://docs.applio.org/)
