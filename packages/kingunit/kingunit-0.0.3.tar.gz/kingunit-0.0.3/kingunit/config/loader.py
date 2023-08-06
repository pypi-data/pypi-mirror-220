import os
import yaml

from kingunit.init import Init_Config

config = None

if not os.path.exists("config.yaml"):
    print("config.yaml not found.")
    print("initing...")
    Init_Config()
    os._exit(0)

# 读取配置文件(config.yaml)
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
