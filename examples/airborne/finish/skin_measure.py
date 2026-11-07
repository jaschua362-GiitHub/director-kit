"""Skin-luma measurement (BT.601 gray % of full scale) on boxes (x0,y0,x1,y1) in 1080x1920. Usage: skin_measure.py <video-or-png-dir-mode>"""
import cv2, numpy as np, json, sys, pathlib
EXP = pathlib.Path(__file__).resolve().parent.parent
BOX = {'S03':{'cheek_nose_mouth':(450,1000,700,1290),'forehead':(380,590,660,680)},
       'S09':{'right_face':(650,560,900,900),'left_face_eyes':(130,500,420,700)}}
def meas(f, b):
    g = cv2.cvtColor(f[b[1]:b[3], b[0]:b[2]], cv2.COLOR_BGR2GRAY)/2.55
    return round(float(np.median(g)),2), round(float(g.mean()),2)
def run(src, tag):
    out={}
    for s,fr in (('S03',28),('S09',20)):
        c = cv2.VideoCapture(str(src(s))); fs=[]
        while True:
            ok,f=c.read()
            if not ok: break
            fs.append(f)
        out[s]={}
        for name,b in BOX[s].items():
            out[s][name]={'frame_median_mean':meas(fs[fr],b),'shot_median_of_frame_medians':round(float(np.median([meas(f,b)[0] for f in fs])),2)}
    print(tag, json.dumps(out)); return out
if __name__=='__main__':
    p = sys.argv[1]
    run(lambda s: p.format(s=s), sys.argv[2])
