from dataclasses import dataclass

from pathlib import Path
import yaml


@dataclass(frozen=True)
class Paths:
    BASE_DIR: Path = Path(__file__).resolve().parent
    RESOURCES_DIR: Path = BASE_DIR.joinpath("resources")
    SECRETS_PATH: Path = BASE_DIR.joinpath("secrets.yml")


with open(Paths.SECRETS_PATH, "r", encoding="utf-8") as file:
    ENV = yaml.safe_load(file)


@dataclass(frozen=True)
class Config:
    HOST = ENV["CLOVA"]["HOST"]
    API_KEY = ENV["CLOVA"]["API_KEY"]
    PRIMARY_KEY = ENV["CLOVA"]["PRIMARY_KEY"]
    REQUEST_ID = ENV["CLOVA"]["REQUEST_ID"]
