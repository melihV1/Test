"""claude_story.py'deki hikayeyi animasyonlu MP4 videoya çevirir.

Gereksinim: pip install pillow imageio-ffmpeg
Çalıştırmak için: python3 make_video.py  ->  claude_story.mp4
"""

import math
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

from claude_story import STORY, Anthropic

W, H, FPS = 1280, 720, 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

BG1, BG2 = (24, 20, 30), (58, 34, 44)
ACCENT = (217, 119, 87)
CREAM = (245, 238, 228)
MUTED = (170, 160, 160)

INTRO, CHAPTER, OUTRO = 3.0, 4.0, 3.5


def font(path, size):
    return ImageFont.truetype(path, size)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def background(shift):
    img = Image.new("RGB", (W, H), BG1)
    px = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        k = y / H
        c = tuple(int(BG1[i] + (BG2[i] - BG1[i]) * k) for i in range(3))
        px.rectangle([0, y, W, y + 4], fill=c)
    # yüzen parçacıklar
    for i in range(28):
        x = (i * 97 + shift * (10 + i % 5 * 4)) % W
        y = (i * 53 + math.sin(shift * 0.05 + i) * 30) % H
        r = 2 + i % 4
        px.ellipse([x - r, y - r, x + r, y + r], fill=(90, 60, 66))
    return img


def centered(d, text, y, f, fill, alpha=1.0, dx=0):
    fill = tuple(int(BG1[i] + (fill[i] - BG1[i]) * alpha) for i in range(3))
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2 + dx, y), text, font=f, fill=fill)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def timeline(d, idx, progress):
    n = len(STORY)
    x0, x1, y = 140, W - 140, H - 70
    d.line([x0, y, x1, y], fill=(80, 60, 66), width=4)
    filled = x0 + (x1 - x0) * (idx + ease(progress)) / max(1, n - 1)
    d.line([x0, y, min(filled, x1), y], fill=ACCENT, width=4)
    for i, ch in enumerate(STORY):
        x = x0 + (x1 - x0) * i / (n - 1)
        active = i <= idx
        r = 9 if i == idx else 6
        d.ellipse([x - r, y - r, x + r, y + r], fill=ACCENT if active else (80, 60, 66))
        f = font(FONT, 15)
        w = d.textlength(ch.year, font=f)
        d.text((x - w / 2, y + 18), ch.year, font=f, fill=CREAM if active else MUTED)


def frame_intro(t, f):
    img = background(f)
    d = ImageDraw.Draw(img)
    a = ease(t / 1.0)
    centered(d, "Claude'un Hikayesi", 250 + (1 - a) * 40, font(BOLD, 72), CREAM, a)
    centered(d, "kod ile anlatım", 345, font(MONO, 30), ACCENT, ease((t - 0.6) / 0.8))
    centered(d, f"Anthropic · {Anthropic.founded}", 430, font(FONT, 22), MUTED, ease((t - 1.2) / 0.8))
    return img


def frame_chapter(idx, t, f):
    ch = STORY[idx]
    img = background(f)
    d = ImageDraw.Draw(img)
    out = ease((t - (CHAPTER - 0.5)) / 0.5)  # çıkış solması
    vis = 1 - out

    d.text((110 + (1 - ease(t / 0.7)) * -80, 110), ch.year,
           font=font(BOLD, 110), fill=tuple(int(BG1[i] + (ACCENT[i] - BG1[i]) * ease(t / 0.7) * vis) for i in range(3)))
    d.text((115, 250), ch.title, font=font(BOLD, 48),
           fill=tuple(int(BG1[i] + (CREAM[i] - BG1[i]) * ease((t - 0.3) / 0.6) * vis) for i in range(3)))

    # kod tarzı daktilo efekti
    code = f'Chapter("{ch.year}", "{ch.title}")'
    shown = code[: int(max(0, t - 0.5) * 30)]
    d.text((115, 325), shown + ("▌" if int(t * 3) % 2 == 0 else ""), font=font(MONO, 22),
           fill=tuple(int(BG1[i] + (ACCENT[i] - BG1[i]) * vis) for i in range(3)))

    body = font(FONT, 30)
    for i, line in enumerate(wrap(d, ch.text, body, W - 260)):
        a = ease((t - 1.0 - i * 0.25) / 0.6) * vis
        col = tuple(int(BG1[j] + (CREAM[j] - BG1[j]) * a) for j in range(3))
        d.text((115, 395 + i * 46 + (1 - ease((t - 1.0 - i * 0.25) / 0.6)) * 20), line, font=body, fill=col)

    timeline(d, idx, min(1.0, t / 1.2))
    return img


def frame_outro(t, f):
    img = background(f)
    d = ImageDraw.Draw(img)
    a = ease(t / 0.8)
    centered(d, "Değerlerim", 190, font(BOLD, 44), MUTED, a)
    for i, v in enumerate(["yardımsever", "dürüst", "zararsız"]):
        aa = ease((t - 0.5 - i * 0.5) / 0.6)
        centered(d, v, 270 + i * 80 + (1 - aa) * 25, font(BOLD, 56), ACCENT if i % 2 == 0 else CREAM, aa)
    centered(d, "Voldi Creative için hazırdır.", 560, font(FONT, 26), MUTED, ease((t - 2.3) / 0.8))
    return img


def main(out="claude_story.mp4"):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen(
        [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out],
        stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    f = 0

    def push(img):
        proc.stdin.write(img.tobytes())

    for i in range(int(INTRO * FPS)):
        push(frame_intro(i / FPS, f)); f += 1
    for idx in range(len(STORY)):
        for i in range(int(CHAPTER * FPS)):
            push(frame_chapter(idx, i / FPS, f)); f += 1
    for i in range(int(OUTRO * FPS)):
        push(frame_outro(i / FPS, f)); f += 1

    proc.stdin.close()
    proc.wait()
    print(f"{out} hazır — {f / FPS:.1f} sn")


if __name__ == "__main__":
    main()
