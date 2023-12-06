import shutil
import os
from pathlib import Path
import uuid
import hashlib
from checksumdir import dirhash
from pylinhsu import log
from pylinhsu.os import run_command


def is_dir(path):
    return Path(path).is_dir()


def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def exists(path):
    return Path(path).exists()


def copy(src, dst):
    if is_dir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def remove(path):
    if is_dir(path):
        shutil.rmtree(path)
    else:
        Path(path).unlink()


def poweshell_remove(path):
    run_command(f"powershell Remove-Item -Recurse -Force -Confirm:$false '{path}'")


def move(src, dst):
    if os.path.exists(dst) and os.path.samefile(src, dst):
        return
    shutil.move(src, dst)


def poweshell_move(src, dst):
    run_command(
        f"powershell Move-Item -Force -Confirm:$false -Path '{src}' -Destination '{dst}'"
    )


def backup(path):
    path_backup = path
    while exists(path_backup):
        id = str(uuid.uuid4())
        path_backup = f"{path}.bak.{id}"
    copy(path, path_backup)
    return path_backup


def backups(paths):
    results = {}
    for path in paths:
        results[path] = backup(path)
    return results


def recover_backup(path, backup):
    remove(path)
    move(backup, path)


def recover_backups(paths, backups):
    for path in paths:
        recover_backup(path, backups[path])


def md5(path):
    if not exists(path):
        return None
    if is_dir(path):
        return dirhash(path, "md5")
    else:
        return hashlib.md5(open(path, "rb").read()).hexdigest()


def md5s(paths):
    results = {}
    for path in paths:
        results[path] = md5(path)
    return results


def compare_md5s(keys, a, b):
    no_same = True
    for k in keys:
        if a[k] == b[k]:
            log.warning(f"MD5 of {k} didn't change: f{a[k]}")
            no_same = False
    return no_same


def insert_tag(path, tag):
    # 'test.txt' -> 'test' + '.txt'
    root, ext = os.path.splitext(path)
    result = f"{root}.{tag}{ext}"
    return result


def replace_ext(path, ext):
    root, _ = os.path.splitext(path)
    result = f"{root}.{ext}"
    return result


join = os.path.join


FILESIZE_STR_BASE_1024_MAX_LEN = 11
FILESIZE_STR_BASE_1000_MAX_LEN = 10


def filesize_str(filesize, base_1024_T_or_1000_F=True):
    base = 1024 if base_1024_T_or_1000_F else 1000
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "BiB"]
    unit_index = 0
    while filesize >= base:
        filesize /= base
        unit_index += 1
    unit = units[unit_index]
    unit_len = 3
    if not base_1024_T_or_1000_F:
        unit = unit.replace("i", "")
        unit_len = 2
    unit = f"{unit:>{unit_len}}"
    if unit_index == 0:
        return f"{filesize} {unit}"
    return f"{filesize:.2f} {unit}"


def path_filesize_str(path, base_1024_T_or_1000_F=True):
    return filesize_str(os.path.getsize(path), base_1024_T_or_1000_F)
