import glob
from pathlib import Path

from dynaconf import Dynaconf

ROOT_DIR = Path(__file__).parent

__all__ = ("config",)


def read_files(file_path: str) -> list:
    return glob.glob(file_path, root_dir=ROOT_DIR)


confs = read_files("default/*.yml")

config = Dynaconf(
    settings_files=confs,  # path/glob
    core_loadrs=["YAML"],
    load_dotenv=True,
    root_path=ROOT_DIR,
)

# print(config.app)
