class ConfigException(BaseException):
    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self) -> str:
        return f"Не найден ключ {self.key}"
