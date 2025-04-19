import hashlib
import os
import shutil

QUARANTINE_FOLDER = "quarantine"
RESTORE_FOLDER = "restored"

def hash_file(filepath):
    sha1 = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                sha1.update(chunk)
        return sha1.hexdigest()
    except:
        return None

def load_signatures():
    with open("virus_signatures.txt", "r") as file:
        return set(line.strip() for line in file.readlines())

def scan_folder(path, callback=None):
    signatures = load_signatures()
    infected = []
    
    for root, _, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            file_hash = hash_file(full_path)
            if file_hash in signatures:
                infected.append(full_path)
                if callback:
                    callback(full_path)
    
    return infected

def quarantine(files):
    os.makedirs(QUARANTINE_FOLDER, exist_ok=True)
    for file in files:
        try:
            shutil.move(file, os.path.join(QUARANTINE_FOLDER, os.path.basename(file)))
        except:
            pass

def restore_from_quarantine():
    os.makedirs(RESTORE_FOLDER, exist_ok=True)
    count = 0
    for file in os.listdir(QUARANTINE_FOLDER):
        src = os.path.join(QUARANTINE_FOLDER, file)
        dst = os.path.join(RESTORE_FOLDER, file)
        try:
            shutil.move(src, dst)
            count += 1
        except:
            pass
    return count
