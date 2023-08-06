from __future__ import print_function
import os, sys
import click
"""
从命令行获取参数
 Python 标准库模块 argparse 可用于解析命令行参数~ 但由于 argparse 使用复杂，add_argument 方法参数众多。为此，第三方库模块 click 应运而生，极大地改善了 argparse 的易用性。

注：Click 第三方库由 Flask 的作者 Armin Ronacher 开发。Click 相较于 argparse 较好比 requests 相较于 urllib。

使用 click 之前，需要先进行安装：

pip install click
Click 模块构建 Python 命令行，分以下 2 步走：

使用 @click.command() 装饰器，使被装饰的函数成为命令行接口；
使用 @click.option() 等装饰器，添加命令行选项。
————————————————
版权声明：本文为CSDN博主「ITROOKIEIS」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_15256443/article/details/122420933
"""
import click


@click.command()
@click.option('--count', default=1, help='Number of grettings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times.
    command 使得函数 hello 作为命令行接口；
    option 添加命令行选项；
    click.echo 主要是从兼容性考虑：Python2 的 print 是语句，而 Python3 中则为函数。
    Click 库提供的装饰器 @click.option 通过指定命令行选项的名称，从命令行读取参数值，再将其传递给函数。其中，option 常用的设置参数如下：

    default 设置命令行参数的默认值；
    help 参数说明；
    type 指定参数类型，如 string int float ；
    prompt 当命令行未指定相应参数时，会根据 prompt 提示用户输入；
    nargs 指定命令行参数接受的值的个数。

    """
    for x in range(count):
        click.echo('Hello %s' % name)


# 选择: python score --subject=chinese
@click.command()
@click.option('--subject', type=click.Choice(['math', 'chinese', 'english']))
def score(subject):
    click.echo('{} score: 100'.format(subject))

# 交互式地输入密码
# 在 argparse 模块中，输入密码只能像普通参数一样设置，这将带来一定的安全隐患：使用 history 就可以轻易获取到我们的密码。
# 在 click 中，上述问题得到了非常优美的解决：只需要设置 prompt=True ，就能够交互式地输入密码；
# 设置 hide_input=True 即可隐藏我们的命令行输入；
# 设置 confirmation_prompt=True 就可以进行密码的两次验证。
from werkzeug.security import generate_password_hash
@click.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def encrypt(password):
    click.echo('Encrypting password to %s' % generate_password_hash(password))


# 在编辑器中编辑输入的数据
# 熟悉 Linux 系统的用户，很可能使用过命令 fc，在编辑长命令时非常便捷。
# 输入 fc 命令并回车会打开一个编辑器，改编辑器已经保存了上一条命令的内容。
# 我们只需要在编辑器中修复错误内容，然后保存并退出，刚才编辑的命令将会自动执行。
def edit():
    message = click.edit()
    print(message)
    print(os.system(message))

if __name__ == '__main__':
    # hello()

    # 密码
    # 命令行下运行： python shell_command_params2.py

    # 编辑器
    edit()