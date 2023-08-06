from kingunit.config import config
from kingunit.utils import mail
from kingunit import utils
import datetime
import zipfile
import shutil
import os


def Gen_Cases(api_file_path: str):
    """
    生成测试用例
    """

    # 读取测试数据
    api_file = utils.LoadJson(api_file_path)

    # 创建测试文件夹，检查是否存在
    if not os.path.exists(f"{config['output_path']}"):
        os.mkdir(f"{config['output_path']}")
    if not os.path.exists(f"{config['output_path']}/{api_file['name']}"):
        os.mkdir(f"{config['output_path']}/{api_file['name']}")

    # 生成测试文件
    with open(
        f"{config['output_path']}/{api_file['name']}/{config['test_cases_file']}", "w"
    ) as file:
        file.write("from kingunit_inspector.inspector import *\n")
        for case in api_file["apis"]:
            file.write("\n")
            file.write("\n")
            file.write(f"def test_{case['name']}():\n")
            file.write(f"    inspector('{api_file['baseUrl']}', {str(case)})\n")

    # 使用black格式化代码
    # 检查是否安装了black
    if os.system("black --version") == 0:
        os.system(f"black {config['output_path']}/{api_file['name']}/{config['test_cases_file']}")


def Gen_Report(case_name: str, use_allure: bool = False):
    """
    生成测试报告
    """

    # 检查pytest是否安装
    if os.system("pytest --version") == 0:
        allure_path = f"--alluredir={config['output_path']}/{case_name}/allure-jsons"
        os.system(
            f"pytest {config['output_path']}/{case_name}/{config['test_cases_file']} --html={config['output_path']}/{case_name}/report.html {allure_path if use_allure else ''}"
        )
    else:
        raise Exception("Pytest not found.")


def Test_Case(case_name: str, endpoint: str):
    """
    对测试用例的具体某个测试点进行测试
    """

    # 检查pytest是否安装
    if os.system("pytest --version") == 0:
        os.system(
            f"pytest {config['output_path']}/{case_name}/{config['test_cases_file']} -k {endpoint}"
        )
    else:
        raise Exception("Pytest not found.")


def Preview_Allure_Report(path: str):
    """
    预览测试报告
    """
    if os.system("allure --version") == 0:
        os.system(f"allure serve {config['output_path']}/{path}/allure-jsons")
    else:
        raise Exception("Allure not installed.")


def Delete_Report(path: str):
    """
    删除测试报告
    """
    shutil.rmtree(f"{config['output_path']}/{path}")


def Send_Repoprt_By_Mail(case: str, receivers: list):
    """
    通过邮件发送测试报告
    """
    # 打包report目录为zip文件
    zip_path = f"{config['output_path']}/report.zip"
    f = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    for dirpath, _, filenames in os.walk(f"{config['output_path']}/{case}"):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()

    # 发送邮件
    mail.send_email_with_zip(
        receivers,
        f"KingUnit测试报告({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
        "请查收附件。",
        f"{zip_path}",
    )

    # 删除report.zip
    os.remove(f"{zip_path}")
            
