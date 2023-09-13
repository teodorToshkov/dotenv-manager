import os
import json
from dotenv import load_dotenv
from dotenv_manager.logger import logger
from dotenv_manager.singleton import Singleton

class EnvManager:
    """
A decorator for defining a set of environment variables.
Uses the python-dotenv package to load additional variables from .env

The dotenv manager ensures the environment variables used in the project are set and have the correct types.

    Usage:
    
@EnvManager()
class CONFIG:
    KEY1: str
    KEY2: str
    INT_KEY: int

@EnvManager(prefix="AWS_")
class AWS_CONFIG:
    SECRET: str
    ENDPOINT: str

Using strict=False, an error message is printed to the terminal, instead of throwing an error.

@EnvManager(strict=False)
class CONFIG:
    NOT_FOUND_KEY: str
    ENDPOINT: str
    """
    
    def __init__(self, /, *, prefix: str = "", strict=True) -> None:
        self.prefix = prefix
        self.strict = strict

    def __call__(parent, cls: type) -> object:

        def try_parse(T: type, value: str) -> object:
            try:
                value = T(value)
            except Exception as e:
                if parent.strict:
                    raise e
                logger.error(f"Could not convert \"{value}\" to {T}")
                value = None
            return value
        
        class BaseEnv(metaclass=Singleton):
            def __init__(self) -> None:
                logger.info("LOADING ENVIRONMENT VARIABLES FROM .env") 
                if load_dotenv():
                    self.__load_env()
                else:
                    logger.error(f"Unable to load .env")

            def __load_env(self) -> None:
                for env_name, (key, T) in zip(self.keys, self.__annotations__.items()):
                    value = os.getenv(env_name)
                    if value != None:
                        value = try_parse(T, value)
                    else:
                        if parent.strict:
                            raise AttributeError(f"Environment variable {key} was not found")
                        logger.error(f"Environment variable {key} was not found")
                    if value != None:
                        setattr(self, key, value)

            def dump(self) -> str:
                return {
                    key: getattr(self, key)
                    for key in self.keys
                }

            def __str__(self) -> str:
                return json.dumps(self.dump())

            def __repr__(self) -> str:
                return f"{self.__class__.__name__}({self.__str__()})"

        class NewEnvClass(cls, BaseEnv):
            pass

        NewEnvClass.__name__ = cls.__name__
        NewEnvClass.__qualname__ = cls.__qualname__
        NewEnvClass.__annotations__ = cls.__annotations__
        NewEnvClass.keys = [f"{parent.prefix}{key}" for key in cls.__annotations__.keys()]
        
        return NewEnvClass()
