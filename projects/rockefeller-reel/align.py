"""Forced-align the spoken words (romanised Tanglish, one entry per caption line) to the voice track.

Run with an environment that has torch + torchaudio (MMS_FA) and uroman:
  python align.py <voice.wav> <out.json>
Writes, per line: start, end and every word's start/end in seconds.
"""
import json
import re
import sys

import soundfile as sf
import torch
import torchaudio
from torchaudio.pipelines import MMS_FA

LINES = [
    'ulagathula highest profit margin company edhu theriyuma',
    'apple illa nvidia illa',
    'endha oru oil company um kidaiyadhu',
    'indha company ippo unga pocket la irukku',
    'unga purse thirandhu paarunga',
    'visa or mastercard',
    'visa makes fifty percent net profit on every dollar it makes',
    'idhula interesting vishayam enna theriyuma',
    'visa ungalukku debit card credit card kudukkala bank thaan kudukkudhu',
    'visa ungalukku loan kudukkala bank thaan kudukkudhu',
    'visa ku endha oru risk um illama easy profits',
    'avanga oru bridge maari',
    'ulagathula enga panam transfer pannalum indha bridge moolama thaan transfer aagudhu',
    'neenga ovvoru thadavaiyum card swipe pannumbodhu oru chinna fee',
    'every day silently billions of transactions around the world and they make profits out of it',
    'ippo dubai real estate laium idhe maari oru silent opportunity irukku',
    'adhu thaan commercial real estate',
    'thirteen crores invest panni one point three crore rupees varikum rentals edukalam indha project la',
    'christian a rockefeller business tower',
    'idhu four hundred meters tall eighty seven floors irukku sheikh zayed road la',
    'idhu thaan dubai oda tallest commercial tower',
    'ulagathoda first billionaire rockefeller family oda sixth generation christian rockefeller is the brand',
    'easy fifty fifty payment plan',
    'office thirteen crores la start aagudhu',
    'visa maari silent massive profits venumna',
    'indha project unga watch list la irukkanum',
    'idha pathi more information therinjikka rockefeller nu comment pannunga',
    'illa screen la theriyura number la contact pannunga',
    'ill get in touch',
]

wav, sr = sf.read(sys.argv[1], dtype='float32')
if wav.ndim > 1:
    wav = wav.mean(axis=1)
waveform = torch.from_numpy(wav).unsqueeze(0)
if sr != MMS_FA.sample_rate:
    waveform = torchaudio.functional.resample(waveform, sr, MMS_FA.sample_rate)

model = MMS_FA.get_model(with_star=False)
tokenizer = MMS_FA.get_tokenizer()
aligner = MMS_FA.get_aligner()
dictionary = MMS_FA.get_dict(star=None)

words, owner = [], []
for li, line in enumerate(LINES):
    for w in line.split():
        w = re.sub(r'[^a-z]', '', w.lower())
        w = ''.join(c for c in w if c in dictionary)
        if w:
            words.append(w)
            owner.append(li)

with torch.inference_mode():
    emission, _ = model(waveform)
    spans = aligner(emission[0], tokenizer(words))

frames = emission.shape[1]
sec_per_frame = waveform.shape[1] / frames / MMS_FA.sample_rate
out = [{'text': l, 'words': []} for l in LINES]
for w, li, span in zip(words, owner, spans):
    out[li]['words'].append({'w': w, 's': round(span[0].start * sec_per_frame, 3), 'e': round(span[-1].end * sec_per_frame, 3)})
for line in out:
    line['start'] = line['words'][0]['s']
    line['end'] = line['words'][-1]['e']
json.dump(out, open(sys.argv[2], 'w'), indent=1)
for line in out:
    print(f"{line['start']:6.2f}-{line['end']:6.2f}  {line['text']}")
