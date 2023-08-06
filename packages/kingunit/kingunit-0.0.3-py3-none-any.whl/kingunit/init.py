import os


def Init_Config():
    """
    初始化配置文件
    """

    # 创建配置文件
    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w") as file:
            file.write(
                """# KingUnit 配置文件
mail: 
  host: smtp.163.com
  user: KingUnit
  pass: XXXXXXXXXXXXXXXX
  sender: KingUnit <kingunit@163.com>
  recevier: receviers

# 报告接收者列表
receviers:
  - admin@example.com

# 测试用文件名称
test_cases_file: test_cases.py

# 输出路径
output_path: ./output
                """
            )
        print("Done.")
        print("Please edit the config.yaml file.")
    else:
        print("config.yaml already exists.")