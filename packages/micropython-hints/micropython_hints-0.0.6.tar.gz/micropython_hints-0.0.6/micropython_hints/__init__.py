import os
import meo
import sys

# TGT_DIR = os.path.join(os.path.split(os.path.abspath(os.__file__))[0], "site-packages")
TGT_DIR = os.path.abspath(os.curdir)
DIR = meo.utils.script_path(__file__)

def issame(p1, p2):
    return meo.load_file(p1) == meo.load_file(p2)

def run():
    print(f"\033[31m[WARNING]: Please note that this package will be installed at `{TGT_DIR}` in a destructive manner. \
        \n\rIt is strongly recommended to install it within a virtual environment.\033[0m", end='')

    if input("continue? [y/N]: ").strip() not in ['yes', 'Y', 'y']:
        exit()

    from tqdm import tqdm
    from shutil import copyfile
    for name in tqdm(os.listdir(DIR)):
        if name.startswith("__") and (name.endswith("__.py") or name.endswith("__")):
            continue
        fpath = os.path.join(DIR, name)
        tpath = os.path.join(TGT_DIR, name)
        if os.path.exists(tpath):
            if issame(fpath, tpath):
                continue
            overwrite = False
            while True:
                confirm = input(f"Overwrite {tpath} [y/n]: ").lower()
                if confirm == 'y':
                    overwrite = True
                    break
                elif confirm == 'n':
                    break
            if not overwrite:
                continue
        copyfile(fpath, tpath)
    print("done")

def remove():
    if input("remove? [y/N]: ").strip() not in ['yes', 'Y', 'y']:
        exit()
    from tqdm import tqdm
    for name in tqdm(os.listdir(DIR)):
        if name.startswith("__") and (name.endswith("__.py") or name.endswith("__")):
            continue
        fpath = os.path.join(DIR, name)
        tpath = os.path.join(TGT_DIR, name)
        if os.path.exists(tpath) and issame(tpath, fpath):
            os.remove(tpath)
    print("done")
