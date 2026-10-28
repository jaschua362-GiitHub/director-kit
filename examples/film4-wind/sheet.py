import sys,subprocess,numpy as np
from PIL import Image,ImageDraw
f,out=sys.argv[1],sys.argv[2]; frames=[int(x) for x in sys.argv[3].split(',')]; W=int(sys.argv[4]) if len(sys.argv)>4 else 480
ims=[]
for n in frames:
    r=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'select=eq(n\,{n}),scale={W}:-2','-vframes','1','-f','image2pipe','-vcodec','png','-'],capture_output=True)
    import io; im=Image.open(io.BytesIO(r.stdout)).convert('RGB'); d=ImageDraw.Draw(im); d.text((6,6),str(n),fill=(255,255,0)); ims.append(im)
c=3; w,h=ims[0].size; rows=(len(ims)+c-1)//c
S=Image.new('RGB',(w*c,h*rows))
for i,im in enumerate(ims): S.paste(im,((i%c)*w,(i//c)*h))
S.save(out)
