"""سرویس صوت تیروتیر: تولید WAV و پخش ترتیبی یک sequence با backend موجود."""
from pathlib import Path
import math, shutil, struct, subprocess, sys, wave

class AudioBackendUnavailable(RuntimeError): pass

def _frequency(note):
    notes={'دو':261.63,'ر':293.66,'رِ':293.66,'می':329.63,'فا':349.23,'سل':392.00,'لا':440.00,'سی':493.88}
    try:return float(note)
    except (TypeError,ValueError):
        key=str(note).strip(); value=notes.get(key)
        if value is None: raise ValueError(f'نت «{key}» شناخته نشد.')
        return value

def render_sequence(notes, path='tirotir-note.wav', rate=44100):
    """notes iterable of (frequency/name, duration); writes one contiguous WAV."""
    frames=[]
    for note,duration in notes:
        freq=_frequency(note); count=max(1,int(rate*float(duration)))
        frames.extend(struct.pack('<h',int(12000*math.sin(2*math.pi*freq*i/rate))) for i in range(count))
    target=Path(path)
    with wave.open(str(target),'wb') as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(rate); out.writeframes(b''.join(frames))
    return str(target)

def play_file(path: str|Path, *, wait=True) -> str:
    path=str(Path(path).resolve()); commands=[]
    if sys.platform.startswith('win'):
        commands=[['powershell','-NoProfile','-Command',f'(New-Object Media.SoundPlayer "{path}").PlaySync()']]
    elif sys.platform == 'darwin': commands=[['afplay',path]]
    else:
        for name in ('aplay','paplay','ffplay'):
            if shutil.which(name): commands.append([name,'-nodisp','-autoexit',path] if name=='ffplay' else [name,path])
    if not commands: raise AudioBackendUnavailable('پخش‌کنندهٔ صوتی پیدا نشد؛ فایل WAV تولید شده است.')
    last=None
    for command in commands:
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            return path
        except (OSError, subprocess.SubprocessError) as exc: last=exc
    raise AudioBackendUnavailable('پخش صوت ناموفق بود؛ فایل WAV تولید شده است.') from last
