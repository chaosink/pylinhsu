
import shutil
from pathlib import Path
import uuid
import hashlib
from checksumdir import dirhash
from pylinhsu import log


def is_dir(path):
    return Path(path).is_dir()


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


def move(src, dst):
    shutil.move(src, dst)


def backup(path):
    path_backup = path
    while exists(path_backup):
        id = str(uuid.uuid4())
        path_backup = f'{path}.bak.{id}'
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
        return dirhash(path, 'md5')
    else:
        return hashlib.md5(open(path, 'rb').read()).hexdigest()


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
    p = Path(path)
    result = f'{p.stem}.{tag}'
    if p.suffix:
        result += '.' + p.suffix
    return result
