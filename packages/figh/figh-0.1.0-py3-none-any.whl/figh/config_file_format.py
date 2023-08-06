from enum import Enum


class ConfigFileFormat(Enum):
    YAML = "yaml"

    def matched(self, file_path: str) -> bool:
        if self == ConfigFileFormat.YAML:
            return file_path.endswith(".yaml") or file_path.endswith(".yml")
        raise ValueError("unsupported file format to check match")

    def __str__(self):
        return self.value

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(self.name)
