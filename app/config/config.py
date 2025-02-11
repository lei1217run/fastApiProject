import glob
import os
from pathlib import Path

from dynaconf import Dynaconf

ROOT_DIR = Path(__file__).parent

__all__ = ("config",)


def read_files(file_path: str) -> list:
    return glob.glob(file_path, root_dir=ROOT_DIR)


os.environ["APP_ENV"] = "development"

confs = read_files("default/*.yml")
confs = [f for f in confs if f.endswith("default.yml") or f.endswith(f"{os.getenv('APP_ENV')}.yml")]

config = Dynaconf(
    settings_files=confs,  # path/glob
    core_loadrs=["YAML"],
    load_dotenv=True,
    root_path=ROOT_DIR,
)
