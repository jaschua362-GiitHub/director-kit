"""Per-shot luma report (BT.709 Y, % of full scale) for a WIND film file. usage: python -I work/luma_report.py <video> [label]"""
import sys, cv2, numpy as np
SH=[('S1',0,83),('S2',84,131),('S3',132,157),('S4',158,221),('S5',222,271),('S6a',272,307),('S6b',308,333),('S6c',334,367),
    ('S7',368,425),('S8',426,473),('S9',474,519),('S13',520,577),('S14',578,673)]
cap=cv2.VideoCapture(sys.argv[1]); Y=[]
while len(Y)<674:
    ok,f=cap.read()
    if not ok: break
    f=f[::4,::4].astype(np.float32)/255; Y.append(f@np.array([0.0722,0.7152,0.2126],np.float32))
print(sys.argv[2] if len(sys.argv)>2 else sys.argv[1]); print('shot   mean   p2    p50   p98   p99.9')
allm=[]
for n,a,b in SH:
    y=np.stack(Y[a:b+1])*100; allm.append(y.mean())
    print(f'{n:5s} {y.mean():5.1f} {np.percentile(y,2):5.1f} {np.percentile(y,50):5.1f} {np.percentile(y,98):5.1f} {np.percentile(y,99.9):5.1f}')
print(f'film APL {np.mean(allm):.1f}')
