import os
import re
from datetime import datetime
import importlib
import pkgutil


CUSTOM_PLACEHOLDER_VARS = {"date": datetime.now().strftime("%Y-%m-%d")}


def load_modules_from_package(package_name: str):
    """
        动态加载指定包中的所有模块。

        Args:
            package_name (str): 包名。
    """
    package = importlib.import_module(package_name)
    for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        importlib.import_module(module_name)
        if is_pkg:
            load_modules_from_package(module_name)


def auto_register_injectables(config: dict):
    from app.infrastructure.utils.decorators import registry
    """
        根据配置中的包名加载模块，并过滤 registry 中的类。

        Args:
            config (dict): 配置字典，包含 packages 列表。

        Returns:
            list: 过滤后的可注入类列表。
    """
    if not config:
        return registry
    allowed_packages = set(config.get("packages", []))  # 配置中允许的包名

    for package in allowed_packages:
        load_modules_from_package(package)

    # 过滤 registry 中的类，只保留来自配置指定包的类
    filtered_registry = [
        entry for entry in registry
        if any(entry.module.startswith(package) for package in allowed_packages)
    ]
    return filtered_registry


def get_parent_path(path: str) -> str:
    # 判断路径是否是文件
    if os.path.isfile(path):
        # 如果是文件，返回文件所在目录的上一级目录
        return os.path.dirname(os.path.dirname(path))
    else:
        # 如果是文件夹，返回文件夹的上一级目录
        return os.path.dirname(path)


def make_dirs(path: str):
    if path and not os.path.exists(path):
        os.makedirs(path)


"""
占位符替换
    Args: 
        place_holder: 占位符
        target: 替换目标
    Returns: str
"""


def replace_place_holder(target: str, place_holder: str):
    if not target or not place_holder:
        return target
    if target.index(place_holder) == -1:
        return target
    if place_holder.upper() == 'DATE':
        return target.format(date=datetime.now().strftime('%Y-%m-%d'))
    return target


# 自定义解析器，用于解析 {{}} 占位符
def resolve_placeholders(settings):
    """
    解析配置中使用 {{}} 占位符的字段
    :param settings: 配置对象
    """
    placeholder_pattern = re.compile(r"{{\s*(\w+)\s*}}")

    def resolve_value(value):
        if isinstance(value, str):
            # 替换所有 {{}} 占位符
            return placeholder_pattern.sub(
                lambda match: CUSTOM_PLACEHOLDER_VARS.get(match.group(1), match.group(0)),
                value
            )
        elif isinstance(value, dict):
            # 递归解析字典
            return {k: resolve_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            # 递归解析列表
            return [resolve_value(v) for v in value]
        return value

    return resolve_value(settings)
