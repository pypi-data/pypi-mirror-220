"""
  KingUnit 命令行工具
  KingUnit 提供了一个命令行工具，可以通过命令行来生成测试用例、生成测试报告、预览测试报告、删除测试报告、发送测试报告等。
"""

from kingunit.generator import *
from kingunit.config import config
import typer


app = typer.Typer()

@app.command()
def gen(file: str):
    """
    生成测试用例并输出测试报告
    """
    Gen_Cases(file)
    # 读取测试数据
    api_file = utils.LoadJson(file)
    Gen_Report(api_file["name"], use_allure=True)
    print("Done.")
    print(f"Use 'kingunit pre {api_file['name']}' to preview the report.")

@app.command()
def gen_case(file: str):
    """
    生成测试用例
    """
    Gen_Cases(file)

@app.command()
def gen_report(case: str):
    """
    生成测试报告
    """
    Gen_Report(case, use_allure=True)

@app.command("check")
def check_case(case: str, endpoint: str):
    """
    对测试用例的具体某个测试点进行测试
    """
    Test_Case(case, endpoint)

@app.command("pre")
def preview_report(case: str):
    """
    预览测试报告
    """
    Preview_Allure_Report(case)

@app.command("del")
def delete_report(case: str):
    """
    删除测试报告
    """
    Delete_Report(case) 


@app.command("send")
def send_report(case: str):
    """
    邮件发送测试报告
    """
    Send_Repoprt_By_Mail(case, config["receviers"])
    


