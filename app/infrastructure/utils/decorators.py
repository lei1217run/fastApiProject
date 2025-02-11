# 全局注册表，记录类和模块路径
from dataclasses import dataclass, field
from typing import Callable, Optional, List, Type, Dict, Any

__all__ = ("registry", "ModuleClassInfo")


@dataclass
class ModuleClassInfo:
    name: str
    class_type: Type
    module: str
    instance_type: str  # 新增：用于标识注入类型
    description: Optional[str] = None
    version: Optional[str] = None
    tags: List[str] = field(default_factory=list)  # 默认是空列表
    override_target: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            name=data['name'],
            class_type=data['class'],
            module=data['module'],
            instance_type=data['instance_type'],
            description=data.get('description'),
            version=data.get('version'),
            tags=data.get('tags', [])
        )

    def __repr__(self):
        return (f"<ModuleClassInfo(name='{self.name}', class_type={self.class_type.__name__}, "
                f"module='{self.module}', "
                f"instance_type='{self.instance_type}', description='{self.description}', "
                f"version='{self.version}', tags={self.tags})>, "
                f"override_target='{self.override_target}'")


# registry: List[Dict[str, str]] = []
registry: List[ModuleClassInfo] = []


def injectable(
    name: str,
    instance_type: str = "factory",
    description: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    required: bool = True,  # 控制参数是否必填
    override_target: Optional[str] = None
) -> Callable:
    """
    装饰器，用于标记类为可注入，支持自定义参数。

    Args:
        name (str): 类的标识名称（必填）。
        instance_type (str): 注入类型，如 'singleton', 'factory', 等。
        description (str, optional): 类的描述信息。
        version (str, optional): 类的版本号。
        tags (List[str], optional): 标签列表，用于分类或过滤。
        required (bool, optional): 是否强制要求 name 参数。
        override_target:

    Returns:
        Callable: 返回被装饰的类。
    """

    def decorator(cls: Type) -> Type:
        if required and not name:
            raise ValueError("The 'name' parameter is required when 'required=True'.")

        # 注册类到全局 registry
        registry.append(
            ModuleClassInfo(
                name=name,
                class_type=cls,
                module=cls.__module__,
                instance_type=instance_type,
                description=description,
                version=version,
                tags=tags or [],  # 避免默认参数陷阱
                override_target=override_target
            )
        )
        return cls

    return decorator
