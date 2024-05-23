import pathlib
import sys
import numpy as np
import librosa
from pathlib import Path

from tqdm import tqdm

SAMPLE_RATE = 8000

dir_path = str(Path(__file__).parent)
WAV = dir_path + f"/data/{sys.argv[1]}.wav"


if __name__ == "__main__":

    wav_input, sample_rate = librosa.load(WAV, sr=SAMPLE_RATE)
    data_length = len(wav_input)
    np.set_printoptions(threshold=np.inf)
    outtxt = []
    for n in tqdm(wav_input):
        outtxt.append(f"{n*32768:.2f}") # scale up 32768 for 

    pathlib.Path("./data.txt").write_text('\n'.join(outtxt))
    # pathlib.Path(WAV[:-4]+".txt").write_text('\n'.join(outtxt))
