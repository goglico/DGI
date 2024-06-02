from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import wave

app = FastAPI()

@app.get("/get_files")
async def get_files():
    files_info = []
    for file in os.listdir("Audio_Items"):
        if file.endswith(".wav"):
            with wave.open(f"Audio_Items/{file}", "rb") as wav_file:
                params = wav_file.getparams()
                files_info.append({
                    "filename": file,
                    "sample_rate": params.framerate,
                    "num_of_channels": params.nchannels,
                    "bits_per_sample": params.sampwidth * 8,
                    "audio_data_size": params.nframes * params.sampwidth,
                })
    return files_info

@app.get("/get_file/{filename}")
async def get_file(filename: str):
    file_path = f"Audio_Items/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


