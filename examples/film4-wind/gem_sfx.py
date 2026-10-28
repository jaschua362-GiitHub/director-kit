"""Synthesised third-eye sound (replaces SFX13). Glass 'tink' per strobe blink (pitch rising), then a clean
crystalline lock-on: inharmonic bell partials + soft sub swell + airy shimmer. Timeline = S7 source frames."""
import numpy as np, wave
SR=48000
import sys
OFF=int(sys.argv[1]) if len(sys.argv)>1 else 34; f0=int(sys.argv[2]) if len(sys.argv)>2 else 30
blinks=[OFF+x for x in [0,6,11,15,19,22,24,26,28]]   # ruby-onset frames of work/gem_strobe.py
lock=OFF+29
T=(lock+27-f0)/24+1.0; n=int(T*SR); t=np.arange(n)/SR; y=np.zeros(n)
def tink(at,freq,amp):
    i=int(at*SR); m=int(0.35*SR); tt=np.arange(m)/SR
    parts=[(1,1),(2.76,.45),(5.40,.22),(8.93,.10)]
    s=sum(a*np.sin(2*np.pi*freq*r*tt)*np.exp(-tt*(18+6*r)) for r,a in parts)
    s*=np.minimum(1,tt/0.002); seg=y[i:i+m]; seg+=amp*s[:len(seg)]
for j,b in enumerate(blinks):
    tink((b-f0)/24, 1900*2**(j/14), 0.22+0.03*j)
L=(lock-f0)/24; i=int(L*SR); m=n-i; tt=np.arange(m)/SR
bell=sum(a*np.sin(2*np.pi*660*r*tt+0.3*r)*np.exp(-tt*d) for r,a,d in [(1,1,1.2),(2.01,.5,1.6),(2.76,.35,2.2),(4.07,.2,3),(5.43,.12,4)])
sub=np.sin(2*np.pi*48*tt)*np.minimum(1,tt/0.08)*np.exp(-tt*1.4)
shim=np.random.default_rng(3).normal(0,1,m); shim=np.convolve(shim,np.ones(6)/6,'same')*np.exp(-tt*2.5)*np.minimum(1,tt/0.01)
lock_s=0.30*bell+0.55*sub+0.025*shim
lock_s*=np.minimum(1,tt/0.004)
y[i:]+=lock_s
# pre-swell before lock
pi=int((L-0.6)*SR); pt=np.arange(int(0.6*SR))/SR
y[pi:pi+len(pt)]+=0.18*np.sin(2*np.pi*48*pt)*(pt/0.6)**2
y=y/np.abs(y).max()*0.9
st=np.stack([y,np.roll(y,int(0.0007*SR))],1)
w=wave.open('raw/sfx/14_gem_clean.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype('<i2').tobytes());w.close()
print('ok',T)
