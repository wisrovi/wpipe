import copy
import yaml


class LoadConfig:
    NAME = __name__
    VERSION = "1.0.1"

    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path

    def merge_dict(self, dict1: dict, dict2: dict) -> dict:
        if not dict1:
            return dict2
        if not dict2:
            return dict1

        return {
            **dict1,
            **{
                key: (
                    self.merge_dict(dict1[key], value)
                    if isinstance(value, dict) and key in dict1
                    else value
                )
                for key, value in dict2.items()
            },
        }

    def __call__(self, args_dict: dict) -> dict:
        try:
            with open(self.yaml_path, "r") as file:
                yaml_data = yaml.safe_load(file)

        except yaml.YAMLError as e:
            raise ValueError(f"Error loading the YAML file: {e}")

        merge_dicts = self.merge_dict(copy.deepcopy(yaml_data), args_dict)

        return merge_dicts
