# KingUnit

## 安装依赖

```bash
pip install -r requirements.txt
```

## 安装allure

确保已经安装了JDK（1.8+），然后根据操作系统安装allure。

Windows:

打开 <https://github.com/allure-framework/allure2/releases> 下载最新版本的allure，解压到任意目录，进入bin文件下，运行allure.bat，闪现一下说明安装成功，之后将bin目录添加到环境变量。

Mac:

```bash
brew install allure
```

## 运行测试

```bash
from kingunit import KingUnit

if __name__ == '__main__':
    KingUnit.run()
```
