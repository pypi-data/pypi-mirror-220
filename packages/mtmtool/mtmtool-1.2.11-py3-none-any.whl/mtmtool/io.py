import pickle
import json
import yaml
import os
# 加载yaml模块
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# 获取桌面路径
try:
    import winreg

    def get_desktop():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]
except:
    pass


def read_pkl(path):
    with open(path, "rb") as f:
        res = pickle.load(f)
    return res


def write_pkl(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def read_txt(path, encoding="utf8"):
    with open(path, "r", encoding=encoding) as f:
        data = f.read()
    return data


def write_txt(path, data, encoding="utf8"):
    with open(path, "w", encoding=encoding) as f:
        f.write(data)


def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.read()
    res = json.loads(data)
    return res


def write_json(path, data):
    with open(path, "w") as f:
        f.write(json.dumps(data, separators=(',', ':')))


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=Loader)
    return data


def auto_make_dirs(path, isdir=True):
    """根据路径创建父文件夹，如果没有文件夹，自动创建文件夹。当isdir参数为True时，路径即为要创建的文件夹"""
    path = os.path.abspath(path)
    if isdir:
        obj_path = path
    else:
        obj_path = os.path.dirname(path)
    if not os.path.exists(obj_path):
        os.makedirs(obj_path)