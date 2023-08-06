#coding=utf-8
from . import __path__
from . import base
from buildz import confz
import re
import os
import sys
import buildz
import web

"""
[
(url, id),
(url, id, []),
(url, id, [], {}),
]
"""

def listdirs(dirpaths, suffixs=[], excepts=[]):
    if type(dirpaths) == str:
        dirpaths = [dirpaths]
    rst = []
    for dirpath in dirpaths:
        k = listfiles(dirpath, suffixs, excepts)
        rst += k
    return rst

pass

def listfiles(dirpath, suffixs=[], excepts=[]):
    files = os.listdir(dirpath)
    files = [os.path.join(dirpath, fp) for fp in files]
    if len(suffixs)>0:
        rst = []
        for fp in files:
            for sfx in suffixs:
                if len(fp)<len(sfx):
                    continue
                if fp[-len(sfx):] == sfx:
                    rst.append(fp)
                    break
        files = rst
    if len(excepts)>0:
        rst = []
        for fp in files:
            find = False
            for exp in excepts:
                if len(fp)<len(sfx):
                    continue
                if fp[-len(sfx):] == sfx:
                    find = True
                    break
            if not find:
                rst.append(fp)
        files = rst
    return files

pass

import traceback
class Config:
    def add_file(self, filepath):
        self.filepaths.append(filepath)
        self.reset()
    def add_url_data(self, datas, url, path, args, maps):
        urls = url.split("/")
        urls = [k.strip() for k in urls if k.strip()!=""]
        for key in urls:
            _maps = datas[1]
            if key not in _maps:
                _maps[key] = [[], {}]
            datas = _maps[key]
        datas[0].append([url, path, args, maps])
    def add_order(self, level, url, path, args, maps):
        if level not in self.orders:
            self.orders.append(level)
            self.orders.sort()
            self.order_maps[level] = [[], {}]
        datas = self.order_maps[level]
        return self.add_url_data(datas, url, path, args, maps)
    def reset(self, config_type = None):
        if config_type is None:
            config_type = self.config_type
        else:
            config_type = config_type.lower()
            self.config_type = config_type
        print("config_type:", config_type)
        if config_type == 'dict':
            self._fc = ConfigWebMap
        elif config_type == 'list':
            self._fc = ConfigWeb
        elif config_type == 'order':
            self._fc = ConfigWebMap
        else:
            raise Exception("ERROR config_type:"+config_type)
        if config_type == 'order':
            self.reset_order()
        else:
            self.reset_base()
    def order_sort(self, datas):
        datas[0].sort()
        for lv in datas[0]:
            maps = datas[1][lv]
            for key in maps:
                self.order_sort(maps[key])
    def reset_order(self):
        filepaths = self.filepaths
        if type(filepaths) == str:
            filepaths = [filepaths]
        self.filepaths = filepaths
        rst = []
        self.orders = []
        self.order_maps = {}
        for fp in self.filepaths:
            data = confz.loadfile(fp)
            if type(data[0])!= list:
                data = [data]
            rst += data
        for obj in rst:
            if len(obj)!=2:
                print("Error Config:", obj)
                continue
            level = int(obj[0])
            vals = obj[1]
            for val in vals:
                if len(val)<2:
                    print("Error Config Val:", val)
                    continue
                if len(val) == 2:
                    val.append([])
                if len(val) == 3:
                    val.append({})
                url, path, args, maps = val
                self.add_order(level, url, path, args, maps)
    def reset_base(self):
        filepaths = self.filepaths
        if type(filepaths) == str:
            filepaths = [filepaths]
        self.filepaths = filepaths
        rst = []
        self.urls = []
        self.orders = [0]
        self.order_maps = {0:[[],{}]}
        for fp in self.filepaths:
            rst += confz.loadfile(fp)
        for val in rst:
            if len(val)<2:
                print("Error Config:", val)
                continue
            if len(val) == 2:
                val.append([])
            if len(val) == 3:
                val.append({})
            url, path, args, maps = val
            if self.config_type == 'list':
                self.urls.append([url, path, args, maps])
            elif self.config_type == 'dict':
                self.add_url_data(self.order_maps[0], url, path, args, maps)
            else:
                raise Exception("Error config_type in reset")
    def __init__(self, builds, filepaths, root = None, config_type = 'list'):
        super(Config, self).__init__()
        self.builds = builds
        self.filepaths = filepaths
        if root is not None:
            sys.path.append(root)
        config_type = config_type.lower()
        self.config_type = config_type
        self.reset()
    def deal(self):
        cw = self._fc(self)
        cw._set(self)
        cw.init()
        cw.deal()
    def GET(self, url):
        return self._fc(self).GET(url)
    def POST(self, url):
        return self._fc(self).POST(url)

pass
class ConfigMap(Config):
    def __init__(self, builds, filepaths, root = None):
        super(ConfigMap, self).__init__(builds, filepaths, root, 'dict')

pass

class ConfigOrderMap(Config):
    def __init__(self, builds, filepaths, root = None):
        super(ConfigMap, self).__init__(builds, filepaths, root, 'order')

pass

class ConfigWebMap(base.Base):
    def __init__(self, config):
        super(ConfigWebMap, self).__init__()
        self.config = config
    def single(self, datas):
        config = self.config
        type = self.input.type
        for pt, obj, args, maps in datas:
            obj = config.builds.get(obj)
            obj._set(self)
            try:
                obj.init(*args, **maps)
                if type == base.GET:
                    obj.get()
                elif type == base.POST:
                    obj.post()
            except Exception as exp:
                traceback.print_exc()
                print("Exp:", exp)
                self.output.set_str(str(exp))
                self.output.finish(True)
            if self.output.finish():
                return True
        return False
    def deal(self):
        config = self.config
        url = self.input.url
        urls = url.split("?")[0].split("/")
        urls = [k.strip() for k in urls if k.strip()!=""]
        urls.append(None)
        mark_fin = False
        for level in config.orders:
            datas = config.order_maps[level]
            for key in urls:
                if self.single(datas[0]):
                    mark_fin = True
                    break
                if key not in datas[1]:
                    break
                datas = datas[1][key]
            if mark_fin:
                break
        if self.output() is None:
            raise web.HTTPError("404")

pass
class ConfigWeb(base.Base):
    def __init__(self, config):
        super(ConfigWeb, self).__init__()
        self.config = config
    def deal(self):
        config = self.config
        url = self.input.url
        type = self.input.type
        for pt, obj, args, maps in config.urls:
            if len(pt)==0 or pt[0]!="^":
                pt = "^"+pt
            if len(re.findall(pt, url))== 0:
                continue
            obj = config.builds.get(obj)
            obj._set(self)
            try:
                obj.init(*args, **maps)
                if type == base.GET:
                    obj.get()
                elif type == base.POST:
                    obj.post()
                else:
                    pass
            except Exception as exp:
                traceback.print_exc()
                print("Exp:", exp)
                self.output.set_str(str(exp))
                self.output.finish(True)
            if self.output.finish():
                break
        if self.output() is None:
            raise web.HTTPError("404")
pass
def run(profilepaths):
    dirpath = os.path.join(__path__[0], "profiles", "base.confz")
    default_profiles = [dirpath]
    profilepaths += default_profiles
    builder = buildz.Builder(0, default_import = "buildz.base", ref_this = "buildz.this")
    for filepath in profilepaths:
        builder.add_file(filepath)
    builder.run("webz.main")
    
pass


