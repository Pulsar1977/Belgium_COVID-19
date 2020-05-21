#!/usr/bin/env python3
import os
import requests
import zipfile


def download(url, dest_dir='.'):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_dir, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
    return r.ok


def unzip(zfile, dest_dir='.'):
    if not zfile.endswith('.zip'):
        return False
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)  # create folder if it does not exist
    with zipfile.ZipFile(zfile, "r") as zf:
        zf.extractall(dest_dir)
    return True
