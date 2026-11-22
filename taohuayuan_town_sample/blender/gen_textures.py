"""生成可平铺的程序化纹理：草地柔和噪声 + 水面极淡波纹（无需外部素材）。
python gen_textures.py  -> ../project/assets/textures/*.png
"""
import math, os, random
from PIL import Image

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "project", "assets", "textures"))
os.makedirs(OUT, exist_ok=True)

def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def tileable_waves(n, waves, seed=7):
    """整数频率正弦叠加 -> 天然无缝。返回 0..1 场。"""
    rng = random.Random(seed)
    specs = [(rng.randint(1, 6), rng.randint(1, 6), rng.random()*math.tau, rng.random()*math.tau, a)
             for a in waves]
    f = [[0.0]*n for _ in range(n)]
    for y in range(n):
        ry = 2*math.pi*y/n
        row = f[y]
        for x in range(n):
            rx = 2*math.pi*x/n
            row[x] = sum(a*math.sin(kx*rx+px)*math.cos(ky*ry+py) for kx,ky,px,py,a in specs)
    lo = min(min(r) for r in f); hi = max(max(r) for r in f)
    return [[(v-lo)/(hi-lo) for v in r] for r in f]

def ramp(v, stops):
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            t = max(0.0, min(1.0, (v-p0)/(p1-p0)))
            t = t*t*(3-2*t)  # smoothstep
            return tuple(int(c0[i]+(c1[i]-c0[i])*t) for i in range(3))
    return stops[-1][1]

def gen_grass():
    n = 256
    f = tileable_waves(n, [0.40, 0.24, 0.10, 0.04], seed=20261122)
    # 三色柔和 ramp：暗绿 -> 主绿 -> 暖黄绿（压低明度防荧光）
    stops = [(0.0, hexrgb("5A8058")), (0.52, hexrgb("759961")), (1.0, hexrgb("8AAC6C"))]
    img = Image.new("RGB", (n, n))
    img.putdata([ramp(f[y][x], stops) for y in range(n) for x in range(n)])
    img.save(os.path.join(OUT, "grass_noise.png"), optimize=True)
    print("GRASS", img.size)

def gen_wave():
    n = 128
    f = tileable_waves(n, [0.55, 0.32, 0.16], seed=19)
    # 近白（0.90~1.0）极淡波纹，作为 albedo 细节叠加，不产生杂乱
    img = Image.new("RGB", (n, n))
    img.putdata([(int(232+v*23), int(240+v*15), int(240+v*15)) for v in
                 [f[y][x] for y in range(n) for x in range(n)]])
    img.save(os.path.join(OUT, "water_ripple.png"), optimize=True)
    print("WAVE", img.size)

if __name__ == "__main__":
    gen_grass(); gen_wave()
