# 相当于一个全局的conftest.py
# 可以写钩子函数，也可以写Fixture函数
from typing import List

from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item


def pytest_addoption(parser: Parser, pluginmanager):
    parser.addoption('--priority', action='append', help='运行指定优先级的用例，可以多次使用指定多个')


def pytest_configure(config: Config):
    config.addinivalue_line('markers',
                            'priority: test priority')


def pytest_collection_modifyitems(session, config: Config, items: List[Item]):
    priorities = config.getoption('--priority')
    picked_items = []  # 要运行的用例
    deselect_items = []  # 要排除的用例
    for item in items:
        for maker in item.iter_markers('priority'):
            priority = maker.args[0]  # 异常处理
            if priority in priorities:
                picked_items.append(item)
            else:
                deselect_items.append(item)
    items[:] = picked_items  # 更新item内的用例
    # 显示排除了哪些用例
    config.hook.pytest_deselected(items=deselect_items)
