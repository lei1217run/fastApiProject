# app/application/container.py
from dependency_injector import containers, providers
from app.application.post_service import PostService
from app.infrastructure.persistences.mysql.database import Database, DatabaseSQLAlchemy
from app.infrastructure.repositories import MemoryUserRepository, MySQLPostRepository, LoggerManager
from app.infrastructure.utils.decorators import registry
import inspect

from app.infrastructure.utils.func_util import auto_register_injectables


class AppContainer(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(packages=["app.entrypoint.fastapi.routers.codes"])

    config = providers.Configuration()

    database = providers.Singleton(
        Database,
        host=config.DATABASE.mysql.host,
        user=config.DATABASE.mysql.user,
        password=config.DATABASE.mysql.password,
        database=config.DATABASE.mysql.dbname,
        port=config.DATABASE.mysql.port,
    )

    database_signal = providers.Singleton(
        DatabaseSQLAlchemy,
        host=config.DATABASE.mysql.host,
        user=config.DATABASE.mysql.user,
        password=config.DATABASE.mysql.password,
        database=config.DATABASE.mysql.dbname,
        port=config.DATABASE.mysql.port,
    )

    user_repository = providers.Factory(
        MemoryUserRepository,
        database=database,
    )

    post_repository = providers.Factory(
        MySQLPostRepository,
        database=database,
    )

    logger_manager = providers.Singleton(
        LoggerManager,
        name="application",
    )

    post_service = providers.Factory(
        PostService,
        user_repository=user_repository,
        post_repository=post_repository,
    )

def register_injectables(container: AppContainer, processed_classes=None,processing_classes=None):
    if processed_classes is None:
        processed_classes = set()
    if processing_classes is None:
        processing_classes = set()

    registries = auto_register_injectables(container.config.INJECTION())

    supported_providers = (providers.Singleton, providers.Factory)

    for module_class in registries:
        class_type = module_class.class_type
        name = module_class.name
        instance_type = module_class.instance_type
        override_target = module_class.override_target

        if class_type in processed_classes:
            continue

        if class_type in processing_classes:
            print(f"register_injectables: Circular dependency detected while processing {class_type.__name__}")
            continue

        processing_classes.add(class_type)

        constructor_params = inspect.signature(class_type.__init__).parameters
        kwargs = {}

        # Resolve constructor dependencies
        for param_name, param in constructor_params.items():
            if param_name == 'self':
                continue
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            param_class = param.annotation
            if inspect.isclass(param_class):
                # Check if the container has a provider for the required type
                matched = False
                for attr_name, existing_attr in vars(container).items():
                    if isinstance(existing_attr, supported_providers):
                        if (hasattr(existing_attr, 'provides') and
                                existing_attr.provides and issubclass(existing_attr.provides, param_class)):
                            kwargs[param_name] = existing_attr()
                            matched = True
                            break

                if not matched:
                    injectable_dep = next(
                        (cls for cls in registry if issubclass(cls.class_type, param_class)),
                        None
                    )
                    if injectable_dep:
                        if injectable_dep.class_type not in processed_classes:
                            register_injectables(container, processed_classes, processing_classes)

                        injectable_dep_name = (injectable_dep.override_target or injectable_dep.name).lower()
                        if hasattr(container, injectable_dep_name):
                            kwargs[param_name] = getattr(container, injectable_dep_name)()
                        else:
                            raise ValueError(f"Dependency '{param_name}' for {class_type.__name__} is not resolved.")
                    else:
                        raise ValueError(f"Missing dependency for '{param_name}' in class '{class_type.__name__}'.")

        # 检查是否已有相同名称的依赖，优先使用名称匹配
        target_attr_name = (override_target or name.lower()).lower()
        matched = False

        if hasattr(container, target_attr_name):
            existing_attr = getattr(container, target_attr_name)
            if isinstance(existing_attr, providers.Provider):
                existing_attr.override(
                    providers.Singleton(class_type, **kwargs) if instance_type == "singleton" else providers.Factory(
                        class_type, **kwargs)
                )
                matched = True  # 名称匹配成功

            # 如果名称未匹配，检查类型匹配
        if not matched:
            for attr_name, existing_attr in vars(container).items():
                # 过滤掉 dependency_injector 内部属性和非 Provider 对象
                if attr_name.startswith('_') or not isinstance(existing_attr, providers.Provider):
                    continue

                existing_cls = existing_attr.provides
                if existing_cls == class_type:
                    existing_attr.override(
                        providers.Singleton(class_type,
                                            **kwargs) if instance_type == "singleton" else providers.Factory(class_type,
                                                                                                             **kwargs)
                    )
                    matched = True  # 类型匹配成功
                    break  # 找到匹配的类型，立即结束循环

            # 如果名称和类型都未匹配，注册新依赖
        if not matched:
            if instance_type == "factory":
                setattr(container, target_attr_name, providers.Factory(class_type, **kwargs))
            elif instance_type == "singleton":
                setattr(container, target_attr_name, providers.Singleton(class_type, **kwargs))
            else:
                raise ValueError(f"Unknown instance type: {instance_type}")

        processed_classes.add(class_type)
        processing_classes.remove(class_type)