#!/usr/bin/env python
################################################################
# ENV:
#   {PACKAGE}_CONF      配置文件路径
#   PROJECT_CONF        配置文件路径
#   {PACKAGE}_ROOT      项目根路径
#   PROJECT_ROOT        项目根路径
#   {PACKAGE}_MODE      项目运行模式
#   PROEJCT_MODE        项目运行模式
################################################################
import os
import sys
import site
from functools import cache
from functools import cached_property

import yaml
from path import Path
from singleton_decorator import singleton

# from .yamlext import IncudeLoader


def yaml_include(loader, node):
    file_name = os.path.join(os.path.dirname(loader.name), node.value)
    with open(file_name, "rb") as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)


yaml.add_constructor("!include", yaml_include)


@singleton
class ConfigLoader:

    _config_paths = None
    _project_paths = None

    def __init__(self, pkgname, *, config_paths=None, project_paths=None, prefix="conf"):
        """初始化ConfigLoader
        @pkgname: 项目名称
        @config_paths: 指定搜索路径列表，会覆盖默认搜索列表
        @project_paths: 指定搜索项目路径列表，会覆盖默认搜索项目列表
        @prefix: 项目路径下的子路径，必须为相对路径，默认：conf
        """
        if pkgname:
            self.pkgname = pkgname
        assert self.pkgname
        if config_paths:
            self.config_paths = config_paths
        if project_paths:
            self.project_paths = project_paths
        self.prefix = prefix

    @cached_property
    def name(self):
        """项目名称"""
        return self.pkgname

    @cached_property
    def env_configs(self):
        """环境变量指定的配置路径"""
        envs = [f"{self.pkgname.upper()}_CONF", "PROJECT_CONF"]
        return [Path(x) for x in (os.getenv(x) for x in envs) if x]

    @cached_property
    def env_projects(self):
        """环境变量指定的项目路径"""
        envs = [f"{self.pkgname.upper()}_ROOT", "PROJECT_ROOT"]
        return [Path(x) for x in (os.getenv(x) for x in envs) if x]

    @cached_property
    def env_mode(self):
        """环境变量指定的运行模式"""
        pkgname = self.pkgname
        for x in [f"{pkgname.upper()}_MODE", "PROJECT_MODE"]:
            mode = os.getenv(x)
            if mode:
                return mode
        return None

    @property
    def project_paths(self):
        """可搜索的项目路径列表"""
        if not self._project_paths:
            pkgname = self.pkgname
            self._project_paths = [
                *self.env_projects,
                Path(site.USER_BASE) / "share" / pkgname,
                *(Path(path) / pkgname for path in ["/usr/local/share/", "/usr/local/"]),
            ]
        assert self._project_paths
        return self._project_paths

    @project_paths.setter
    def project_paths(self, paths):
        """指定搜索项目的路径列表"""
        if paths:
            if isinstance(paths, str):
                self._project_paths = [Path(paths)]
            else:
                self._project_paths = [Path(x) for x in paths]

    @property
    def config_paths(self):
        """获取搜索配置文件的路径列表"""
        if not self._config_paths:
            prefix = self.prefix
            pkgname = self.pkgname
            self._config_paths = [
                *self.env_configs,
                *[x / prefix for x in self.project_paths],
                *(Path("/etc/") / pkgname, Path(sys.prefix) / pkgname / "conf"),
            ]
        return self._config_paths

    @config_paths.setter
    def config_paths(self, paths):
        """指定搜索配置文件的路径列表"""
        if paths:
            if isinstance(paths, str):
                self._config_paths = [Path(paths)]
            else:
                self._config_paths = [Path(x) for x in paths]

    @cache
    def get_file(self, filename, *, mode=os.getenv):
        """搜索并返回第一个匹配存在的文件全路径
        @confname: 要搜索的文件
        @mode: 指定工程模式，<default> 使用MODE环境变量. None 不使用MODE. str 使用指定MODE
        """
        if mode is not None:
            mode = self.env_mode if mode is os.getenv else mode
            if mode:
                name, ext = Path(filename).splitext()
                filename = f"{name}.{mode}{ext}"
        for path in self.config_paths:
            if (path / filename).exists():
                return path / filename
        find_paths = "\n".join(self.config_paths)
        raise FileNotFoundError(f"Can not found config file {filename}.\n{find_paths}")

    @cache
    def get_yaml(self, confname="config.yaml", mode=os.getenv):
        """获取yaml配置，扩展名不存在，则自动添加扩展名"""
        assert confname
        if not Path(confname).ext or Path(confname).ext not in (".yaml", ".yml"):
            confname = f"{confname}.yaml"
        with self.get_file(confname, mode=mode).open("r", encoding="utf-8") as fp:
            # return yaml.load(fp, Loader=IncudeLoader)
            return yaml.load(fp, Loader=yaml.FullLoader)

    def get(self, confname="config.yaml", mode=os.getenv):
        """获取yaml配置，扩展名必须为yaml或yml"""
        assert confname
        assert Path(confname).ext in (".yaml", ".yml")
        return self.get_yaml(confname, mode)

    def cache_clear(self):
        self.get_file.cache_clear()
        self.get_yaml.cache_clear()


if __name__ == "__main__":
    print(ConfigLoader(__package__, project_paths=".").get("logging.yaml"))
    try:
        print(ConfigLoader(__package__).get(f"{__package__}.yaml"))
    except FileNotFoundError:
        print("Test OK")


def initialize(pkgname=None, *, config_paths=None, project_paths=None, prefix="conf"):
    ConfigLoader(pkgname, config_paths=config_paths, project_paths=project_paths, prefix=prefix)
