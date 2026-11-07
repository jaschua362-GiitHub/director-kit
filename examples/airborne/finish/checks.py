"""TEST-021 pre-assembly checks (frame count/size, dark-frame guard, flicker) + per-shot luma measurement."""
import cv2, numpy as np, json, pathlib
EXP = pathlib.Path(__file__).resolve().parent.parent
N = [74,60,62,97,136,44,64,72,39,54]
def frames(p):
    c = cv2.VideoCapture(str(p)); out=[]
    while True:
        ok,f = c.read()
        if not ok: break
        out.append(f)
    return out
def luma(f): return cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
res = {'shots':{}, 'check1':'PASS','check2':'PASS','check3':'PASS','flag_dark':[],'flag_flicker':[],'flag_flicker_strict_only':[]}
meas = {}
for i in range(10):
    s = f'S{i+1:02d}'
    U = frames(EXP/f'upscale/shots_1080/{s}.mkv'); S = frames(EXP/f'upscale/shots_480/{s}.mkv')
    r = {'src_frames':len(S),'up_frames':len(U),'expected':N[i],'src_size':list(S[0].shape[1::-1]),'up_size':list(U[0].shape[1::-1])}
    if not (len(U)==len(S)==N[i] and r['up_size']==[1080,1920] and r['src_size']==[480,854]): res['check1']='FAIL'; r['count_ok']=False
    else: r['count_ok']=True
    ul = [luma(f) for f in U]; sl = [luma(f) for f in S]
    um = np.array([x.mean() for x in ul]); sm = np.array([x.mean() for x in sl])
    ratio = um/np.maximum(sm,1e-6)
    r['luma_ratio_min']=round(float(ratio.min()),4); r['luma_ratio_max']=round(float(ratio.max()),4)
    for k in np.where((ratio<0.85)|(ratio>1.15))[0]:
        res['flag_dark'].append({'shot':s,'frame':int(k),'src_luma':round(float(sm[k]),2),'up_luma':round(float(um[k]),2),'ratio':round(float(ratio[k]),3)}); res['check2']='FAIL'
    ud = np.array([np.abs(ul[k]-ul[k-1]).mean() for k in range(1,len(ul))])
    sd = np.array([np.abs(sl[k]-sl[k-1]).mean() for k in range(1,len(sl))])
    # same-resolution variant: upscaled downscaled to 480x854 (area) for a like-for-like diff
    ulm = [cv2.resize(x,(480,854),interpolation=cv2.INTER_AREA) for x in ul]
    udm = np.array([np.abs(ulm[k]-ulm[k-1]).mean() for k in range(1,len(ulm))])
    r['flicker_ratio_max_native']=round(float((ud/np.maximum(sd,1e-6)).max()),3)
    r['flicker_ratio_max_matched']=round(float((udm/np.maximum(sd,1e-6)).max()),3)
    for k in np.where(ud>1.6*sd)[0]:
        e={'shot':s,'frame':int(k+1),'src_diff':round(float(sd[k]),3),'up_diff':round(float(ud[k]),3),'up_diff_at480':round(float(udm[k]),3),'ratio':round(float(ud[k]/max(sd[k],1e-6)),3)}
        res['flag_flicker'].append(e); res['check3']='FAIL'
    res['shots'][s]=r
    # grade measurement on upscaled (pre-grade)
    a = np.stack([x[::4,::4] for x in ul])   # subsampled for percentiles
    meas[s]={'apl_pct':round(float(um.mean()/2.55),2),'p2_pct':round(float(np.percentile(a,2)/2.55),2),'p50_pct':round(float(np.percentile(a,50)/2.55),2),'p98_pct':round(float(np.percentile(a,98)/2.55),2),'p99.9_pct':round(float(np.percentile(a,99.9)/2.55),2)}
    if s=='S03': cv2.imwrite(str(EXP/'finish/_S03_f28.png'),U[28]); cv2.imwrite(str(EXP/'finish/_S03_f28_src.png'),S[28])
    if s=='S09': cv2.imwrite(str(EXP/'finish/_S09_f20.png'),U[20]); cv2.imwrite(str(EXP/'finish/_S09_f20_src.png'),S[20])
    print(s, r, meas[s], flush=True)
res['measure_pregrade_ungraded_upscaled']=meas
(EXP/'upscale/CHECKS.json').write_text(json.dumps(res,indent=1))
print({k:res[k] for k in ['check1','check2','check3']}, len(res['flag_dark']), len(res['flag_flicker']))
