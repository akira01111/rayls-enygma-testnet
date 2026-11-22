import re

# (canonical subtitle text, whisper start, whisper end) — times are VO seconds.
# Text follows the VO script; token written $RLS per Anara 21:19 WIB; receiver @kittynim per on-screen footage.
SENTS = [
 ("How do private blockchain payments actually work?", 0.00, 2.84),
 ("What does a private payment actually leave behind on a public blockchain?", 3.42, 6.88),
 ("I wanted to find out what really happens beyond the usual payment successful message,", 7.62, 12.28),
 ("not just what the sender sees, but what the receiver gets, and what eventually appears on the blockchain.", 12.86, 18.06),
 ("So, I tested it using two registered Enygma public testnet accounts.", 18.82, 22.94),
 ("@anara was the sender, and @kittynim was the receiver.", 23.50, 26.82),
 ("The sender already had shielded $RLS, so I could go straight to the payment process without performing another shield transaction.", 27.28, 34.16),
 ("I opened the send page, selected the shielded balance, chose $RLS, entered @kittynim's username, and set the amount to 6 $RLS.", 34.78, 43.50),
 ("Before proving, I checked the fee breakdown.", 44.12, 46.36),
 ("The wallet showed 3.84 $RLS for gas, and 0.58 $RLS for the Rayls Foundation fee, bringing the displayed total to 4.42 $RLS.", 47.04, 58.78),
 ("After confirming with my passkey, Enygma started preparing the payment.", 59.56, 63.20),
 ("It selected the notes, encrypted the payment, and generated a zero-knowledge proof directly in the browser.", 63.86, 69.60),
 ("The interface reported a 256-byte proof, generated in 10 seconds in this tab.", 70.28, 76.70),
 ("And then, the transaction went through!", 77.32, 79.50),
 ("6 $RLS were sent privately from @anara to @kittynim.", 80.08, 84.06),
 ("When I checked the receiver's activity, it showed 6 $RLS received!", 84.06, 87.98),
 ("The receiver's shielded balance increased from 321.4 to 327.4 $RLS.", 88.56, 95.26),
 ("On the sender side, the shielded balance moved from 14.324 to 3.908 $RLS.", 95.84, 103.70),
 ("That's a difference of 10.416 $RLS.", 104.20, 107.46),
 ("6 $RLS for the payment, plus the 4.416 $RLS fee shown in the detailed activity explanation.", 108.00, 114.88),
 ("Now, let's look at what the blockchain actually recorded.", 115.48, 118.56),
 ("The Explorer shows a successful transfer V2 call to SharedVault, included in Block 24,825,928.", 119.26, 128.10),
 ("The public transaction sender is the Relayer, not @anara.", 128.60, 132.18),
 ("And there's another detail worth noticing.", 132.56, 135.02),
 ("The value field shows 0 USDR.", 135.41, 138.40),
 ("That isn't the amount of the private $RLS payment.", 138.84, 141.22),
 ("The receiver's activity is where we can confirm the 6 $RLS received.", 142.00, 145.86),
 ("The Explorer explanation also shows commitments and encrypted notes, rather than a conventional public transfer displaying 6 $RLS moving directly between the two usernames.", 146.30, 157.24),
 ("So, the transaction itself isn't invisible.", 157.66, 161.24),
 ("The blockchain still records that it happened.", 161.84, 164.10),
 ("Which block included it, and which Relayer submitted it.", 164.10, 167.68),
 ("But the payment information isn't presented like an ordinary public transfer between two wallet addresses.", 168.12, 173.48),
 ("And that's what I wanted to examine.", 174.14, 175.82),
 ("The receiver can confirm the payment, while the public transaction record shows a different picture of what happened behind the scenes.", 176.48, 183.20),
]
VO_OFFSET = 0.8  # VO starts 0.8 s into the video
TOP_SENTENCES = {9, 17}  # sentence indices rendered top-aligned (bottom would cover key data)

HIGHLIGHTS = ["@kittynim", "@anara", "6 $RLS", "4.42 $RLS", "4.416 $RLS", "3.84 $RLS",
              "0.58 $RLS", "shielded $RLS", "256-byte proof", "zero-knowledge proof",
              "10 seconds", "Block 24,825,928", "transfer V2", "SharedVault", "Relayer",
              "0 USDR", "321.4 $RLS", "327.4 $RLS", "14.324 $RLS", "3.908 $RLS", "10.416 $RLS",
              "321.4", "327.4", "14.324", "3.908", "10.416"]
AMBER = r"{\c&H3DC5FF&}"   # #FFC53D in ASS BGR
WHITE = r"{\c&HFFFFFF&}"
_pat = re.compile("|".join(re.escape(h) for h in sorted(HIGHLIGHTS, key=len, reverse=True)))

def tokenize(text):
    """Split sentence into tokens; highlight phrases are single atomic tokens."""
    toks = []  # (text, is_highlight)
    pos = 0
    for m in _pat.finditer(text):
        if m.start() > pos:
            toks += [(w, False) for w in text[pos:m.start()].split()]
        toks.append((m.group(0), True))
        pos = m.end()
    if pos < len(text):
        toks += [(w, False) for w in text[pos:].split()]
    return toks

def pack_lines(toks, maxlen=46):
    """Greedy-pack tokens into lines (never splits a token)."""
    lines, cur = [], []
    curlen = 0
    for t, hl in toks:
        add = len(t) + (1 if cur else 0)
        if cur and curlen + add > maxlen:
            lines.append(cur)
            cur, curlen = [(t, hl)], len(t)
        else:
            cur.append((t, hl))
            curlen += add
    if cur:
        lines.append(cur)
    return lines

def render(lines):
    out = []
    for line in lines:
        s = ""
        for t, hl in line:
            piece = (AMBER + t + WHITE) if hl else t
            if s and not re.fullmatch(r"[.,!?;:)\'\"]+", t):
                s += " "
            s += piece
        out.append(s)
    return "\\N".join(out)

def plain_len(lines):
    return sum(len(t) for line in lines for t, _ in line)

def fmt(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

cues = []  # (t0, t1, text, style)
for si, (text, s0, s1) in enumerate(SENTS):
    toks = tokenize(text)
    lines = pack_lines(toks)
    groups = [lines[i:i+2] for i in range(0, len(lines), 2)]
    total_chars = plain_len(lines)
    pos = 0
    for g in groups:
        chars = plain_len(g)
        t0 = s0 + (pos / total_chars) * (s1 - s0)
        t1 = s0 + ((pos + chars) / total_chars) * (s1 - s0)
        if t1 - t0 < 0.7:
            t1 = t0 + 0.7
        cues.append((t0 + VO_OFFSET, t1 + VO_OFFSET, render(g), "Top" if si in TOP_SENTENCES else "Default"))
        pos += chars
for i in range(len(cues) - 1):
    if cues[i][1] > cues[i+1][0] - 0.04:
        cues[i] = (cues[i][0], cues[i+1][0] - 0.04, cues[i][2], cues[i][3])

header = """[Script Info]
Title: Enygma Week 2 - Private Payment Experiment
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,24,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,2,60,60,32,1
Style: Top,Liberation Sans,24,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,8,60,60,84,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open("/home/hatch/workspace/enygma-week2-video/subs.ass", "w") as f:
    f.write(header)
    for t0, t1, txt, style in cues:
        f.write(f"Dialogue: 0,{fmt(t0)},{fmt(t1)},{style},,0,0,0,,{txt}\n")
print("cues:", len(cues))
plain = open("/home/hatch/workspace/enygma-week2-video/subs.ass").read()
print("bare RLS occurrences:", len(re.findall(r'(?<!\$)RLS', plain)))
print("$RLS occurrences:", plain.count("$RLS"))
print("@kittynim:", plain.count("@kittynim"), "@kittymin:", plain.count("@kittymin"))
print("NBSP in file:", "\u00a0" in plain)
