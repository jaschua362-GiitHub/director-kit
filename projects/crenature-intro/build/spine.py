"""Extract the dragon's spine (medial axis, tail -> nose) and its radius profile from parts/body.png.
Writes parts/spine.npz: pts (N,2) in 2x layout px, resampled every 1 px of arc length, radius (N,)."""
import numpy as np, heapq
from PIL import Image, ImageDraw
from scipy import ndimage
from skimage.morphology import skeletonize

A = np.asarray(Image.open('parts/body.png'))[..., 3] > 127
dist = ndimage.distance_transform_edt(A)
sk = skeletonize(ndimage.binary_opening(A, iterations=2))
ys, xs = np.nonzero(sk)
idx = {(y, x): i for i, (y, x) in enumerate(zip(ys, xs))}
nb = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
adj = [[] for _ in ys]
for i, (y, x) in enumerate(zip(ys, xs)):
    for dy, dx in nb:
        j = idx.get((y+dy, x+dx))
        if j is not None: adj[i].append((j, (dy*dy+dx*dx) ** 0.5))
ends = [i for i in range(len(ys)) if len(adj[i]) == 1]

def dijkstra(src):
    d = np.full(len(ys), np.inf); prev = np.full(len(ys), -1); d[src] = 0; q = [(0, src)]
    while q:
        c, i = heapq.heappop(q)
        if c > d[i]: continue
        for j, w in adj[i]:
            if c + w < d[j]: d[j] = c + w; prev[j] = i; heapq.heappush(q, (c + w, j))
    return d, prev

# nose = the skeleton endpoint nearest the eye; tail = the endpoint geodesically farthest from it
E = np.asarray(Image.open('parts/eye.png'))[..., 3] > 127
ey, ex = np.argwhere(E).mean(0)
e1 = min(ends, key=lambda e: np.hypot(xs[e]-ex, ys[e]-ey))
d1, _ = dijkstra(e1)
e0 = max((e for e in ends if np.isfinite(d1[e])), key=lambda e: d1[e])
print('endpoints:', [(int(xs[e]), int(ys[e])) for e in ends])
print('tail', (int(xs[e0]), int(ys[e0])), '-> nose', (int(xs[e1]), int(ys[e1])), 'len', round(d1[e0]))
_, prev = dijkstra(e0)
path = [e1]
while path[-1] != e0: path.append(prev[path[-1]])
path = path[::-1]
P = np.stack([xs[path], ys[path]], 1).astype(float)
R = dist[ys[path], xs[path]]
# smooth + resample at 1 px arc length
P = np.stack([ndimage.gaussian_filter1d(P[:, k], 6, mode='nearest') for k in (0, 1)], 1)
R = ndimage.gaussian_filter1d(R, 2, mode='nearest')
s = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
u = np.arange(0, s[-1], 1.0)
P = np.stack([np.interp(u, s, P[:, 0]), np.interp(u, s, P[:, 1])], 1); R = np.interp(u, s, R)
np.savez('parts/spine.npz', pts=P, radius=R)
print('spine samples', len(P), 'radius min/max', R.min().round(1), R.max().round(1))
# debug image: skeleton, chosen spine, reconstruction
im = Image.new('RGB', A.shape[::-1], (30, 30, 30)); dr = ImageDraw.Draw(im)
rec = Image.new('L', A.shape[::-1], 0); dr2 = ImageDraw.Draw(rec)
for (x, y), r in zip(P[::2], R[::2]): dr2.ellipse([x-r, y-r, x+r, y+r], fill=255)
rec = np.asarray(rec) > 0
dbg = np.zeros(A.shape + (3,), np.uint8); dbg[A] = (90, 90, 90); dbg[rec] = (200, 200, 200); dbg[A & ~rec] = (220, 80, 80)
dbg[sk] = (80, 160, 255)
for (x, y) in P.astype(int): dbg[y-1:y+2, x-1:x+2] = (255, 220, 0)
x0, x1 = P[:,0].min()-150, P[:,0].max()+150
Image.fromarray(dbg[600:1600, 380:1400]).save('stills/spine_debug.png')
np.save('parts/recon_mask.npy', rec)
