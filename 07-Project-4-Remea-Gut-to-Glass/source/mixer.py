def read_audio(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar','48000','-f','f32le','-']),np.float32).copy()
narr=read_audio(p/'assets/narration.wav');narr*=10**(-18/20)/max(np.sqrt(np.mean(narr*narr)),1e-7)
voice=np.zeros(round(duration*48000),np.float32);voice[:len(narr)]=narr;fx=np.zeros_like(voice)
for t,name,limit,db in cue:
    a=read_audio(p/'assets/sfx'/f'{name}.wav')[:round(limit*48000)]
    a*=10**(db/20)/max(np.sqrt(np.mean(a*a)),1e-7);a*=min(1,.46/max(np.max(np.abs(a)),1e-7))
    edge=min(1500,len(a)//4);a[:150]*=np.linspace(0,1,150);a[-edge:]*=np.linspace(1,0,edge)
    start=round(t*48000);end=min(len(fx),start+len(a));fx[start:end]+=a[:end-start]
mix=voice+fx;mix*=min(1,.96/max(np.max(np.abs(mix)),1e-7))
for name,a in [('mix.wav',mix),('effects.wav',fx)]:
    with wave.open(str(p/'assets'/name),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
(p/'sound-cues.json').write_text(json.dumps(cue,indent=2))

