import subprocess, os
W = "/home/hatch/workspace/enygma-week2-video"
SRC = "/home/hatch/workspace/user/media_library/video/61/610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa.mp4"
SEG = os.path.join(W, "segments_v2")
os.makedirs(SEG, exist_ok=True)
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd)); print(r.stderr[-1500:]); raise SystemExit(1)
    return r
# (kind, a, b/dur) — trim: (a, dur); freeze: (frame_time, dur); zoom: fixed file
PLAN = [
    ("trim", 11.0, 10.0), ("freeze", 21.0, 6.5), ("trim", 47.0, 6.0), ("trim", 55.0, 7.1),
    ("trim", 81.5, 5.1), ("trim", 86.6, 4.0), ("trim", 91.0, 5.0),
    ("trim", 96.0, 12.0), ("freeze", 106.0, 1.2), ("trim", 108.0, 4.8),
    ("trim", 120.0, 8.0), ("trim", 139.0, 6.0), ("trim", 145.0, 7.0),
    ("trim", 172.0, 4.1), ("trim", 168.0, 3.0), ("freeze", 171.0, 1.9),
    ("trim", 161.0, 4.0), ("freeze", 165.0, 5.0),
    ("trim", 206.0, 6.0), ("freeze", 212.0, 3.0),
    ("trim", 196.0, 5.0), ("freeze", 201.0, 2.1),
    ("trim", 233.0, 8.5), ("freeze", 241.5, 5.0),
    ("trim", 201.0, 5.0), ("freeze", 206.0, 4.0),
    ("trim", 183.0, 4.0), ("trim", 212.0, 3.4),
    ("trim", 215.4, 6.6), ("freeze", 222.0, 4.0),
    ("zoom", None, 19.3),
    ("trim", 176.0, 5.9), ("freeze", 181.9, 2.9),
]
clips = []
for i, (kind, a, dur) in enumerate(PLAN):
    out = os.path.join(SEG, f"c{i:02d}.mp4")
    if kind == "trim":
        run(["ffmpeg","-y","-v","error","-ss",str(a),"-i",SRC,"-t",str(dur),
             "-vf","scale=1280:720,fps=30,format=yuv420p",
             "-c:v","libx264","-preset","veryfast","-crf","20","-an",out])
    elif kind == "freeze":
        png = os.path.join(SEG, f"f{i:02d}.png")
        run(["ffmpeg","-y","-v","error","-ss",str(a),"-i",SRC,"-frames:v","1",png])
        run(["ffmpeg","-y","-v","error","-loop","1","-t",str(dur),"-i",png,
             "-vf","scale=1280:720,fps=30,format=yuv420p",
             "-c:v","libx264","-preset","veryfast","-crf","20","-an",out])
    else:  # zoom — pre-rendered standalone clip, verified no-black
        import shutil; shutil.copy(os.path.join(W,"zoom_long.mp4"), out)
    clips.append(out)
    print(f"clip {i:02d} {kind} {a} +{dur}s -> {out}")
lst = os.path.join(SEG, "list.txt")
with open(lst, "w") as f:
    for c in clips:
        f.write(f"file '{c}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lst,"-c","copy",
     os.path.join(W,"video_only_v2.mp4")])
print("concat done; total expected: %.1f s" % sum(d for _,_,d in PLAN))
