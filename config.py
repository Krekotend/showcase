from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Operator:
    operator: str

@dataclass
class Admins:
    admins: str


@dataclass
class PsQL:
    host: str
    port: str
    userb: str
    password: str
    db_name: str


@dataclass
class Config:
    tg_bot: TgBot
    db: PsQL
    operator: Operator
    admins: Admins

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  operator=Operator(operator=env('OPERATOR')),
                  admins=Admins(admins=env('ADMINS')),
                  db=PsQL(host=env('HOST'),
                          port=env('PORT'),
                          userb=env('USERB'),
                          password=env('PASSWORD'),
                          db_name=env('DB_NAME')))
