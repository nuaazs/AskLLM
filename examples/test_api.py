import requests
import torchaudio
import torch
import tempfile
from pydub import AudioSegment
import io

def test(user_audio,session_id):
    url = "http://localhost:8765/chat"
    response = requests.post(url, files={"audio": open(user_audio, "rb")}, data={"session_id": session_id}, stream=True)
    output = []
    i = 0
    format = "wav"
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            i += 1
            file_path = f"{tempfile.gettempdir()}/{i}.{format}"
            print(file_path)
            segment = AudioSegment.from_raw(io.BytesIO(chunk), sample_width=2, frame_rate=32000, channels=1)
            segment.export(file_path, format="wav")
            audio_data,sr = torchaudio.load(file_path)
            output.append(audio_data.reshape(-1))
    output = torch.cat(output)
    output = output.reshape(1,-1)
    torchaudio.save(f"api_output.wav", output, sr)
    return

if __name__ == "__main__":
    test('init.wav', "zs130")

