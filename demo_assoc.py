# -*- coding: utf-8 -*-
"""
demo_assoc.py — ассоциация для .zst и .dem файлов CS2
Автор: @dykomenko

pip install zstandard pyperclip
pyinstaller --onefile --noconsole demo_assoc.py
"""

import sys, os, subprocess, shutil, tempfile
from pathlib import Path

try:
    import zstandard as zstd
    import pyperclip
except ImportError:
    print("Установите зависимости:\n   pip install zstandard pyperclip")
    sys.exit(1)

CONFIG_FILE = "cs2_path.txt"
GAME_SUBPATH = Path("game") / "csgo"

def get_self_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

def read_cs2_path():
    cfg = get_self_dir() / CONFIG_FILE
    if not cfg.exists():
        print(f"❌ Не найден файл {CONFIG_FILE}")
        sys.exit(1)
    p = Path(cfg.read_text(encoding="utf-8").strip())
    if not p.exists():
        print(f"❌ Путь не существует: {p}")
        sys.exit(1)
    return p

def decompress_zst(src: Path, dst: Path):
    dctx = zstd.ZstdDecompressor()
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        dctx.copy_stream(fin, fout)

def copy_to_clipboard(text: str):
    try:
        pyperclip.copy(text)
    except Exception:
        pass

def open_in_explorer(path: Path):
    subprocess.run(["explorer", str(path)], shell=True)

def copy_demo(src: Path, dst_dir: Path):
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    copy_to_clipboard(f"playdemo {src.name}")
    print(f"✅ Скопировано: {dst}")
    print(f"💬 В буфер: playdemo {src.name}")

def handle_zst(zst_file: Path, demos_dir: Path):
    dem_name = zst_file.name[:-4]
    if not dem_name.endswith(".dem"):
        print("⏭ В архиве нет .dem — пропуск.")
        return
    tmp_dem = Path(tempfile.gettempdir()) / dem_name
    try:
        decompress_zst(zst_file, tmp_dem)
    except Exception as e:
        print("❌ Ошибка распаковки:", e)
        return
    if tmp_dem.exists() and tmp_dem.stat().st_size > 0:
        dst = demos_dir / dem_name
        shutil.move(str(tmp_dem), str(dst))
        copy_to_clipboard(f"playdemo {dem_name}")
        print(f"✅ Распаковано: {dst}")
        print(f"💬 В буфер: playdemo {dem_name}")
    else:
        print("❌ Файл пуст или не .dem")

def main():
    cs2_path = read_cs2_path()
    demos_dir = cs2_path / GAME_SUBPATH
    demos_dir.mkdir(parents=True, exist_ok=True)

    # без аргументов — открыть папку
    if len(sys.argv) == 1:
        open_in_explorer(demos_dir)
        return

    f = Path(sys.argv[1])
    if not f.exists():
        print("❌ Файл не найден:", f)
        return

    ext = f.suffix.lower()
    if ext == ".zst":
        handle_zst(f, demos_dir)
    elif ext == ".dem":
        copy_demo(f, demos_dir)
    else:
        print("⏭ Неподдерживаемое расширение:", ext)

if __name__ == "__main__":
    main()
