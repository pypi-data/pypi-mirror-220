import json


def LoadJson(file_path: str) -> dict:
    """
    读取 JSON 文件
    """
    with open(file_path, "r") as file:
        data = json.load(file)
        return data
