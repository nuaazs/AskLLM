import requests
import torchaudio
import torch
import tempfile
from pydub import AudioSegment
import io

def test(session_id):
    url = "http://localhost:8765/chat"
    response = requests.post(url, data={"openid": session_id,"text":"查询余额"})
    r = response.json()
    print(r)
    return r

if __name__ == "__main__":
    test("zs132")

