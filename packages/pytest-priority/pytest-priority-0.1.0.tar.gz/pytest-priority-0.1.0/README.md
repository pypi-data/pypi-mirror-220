# Pytest-Priority
为用例添加优先级标记，并支持按优先级筛选用例执行

## 安装方法
```shell
pip install pytest-priority
```

## 使用方法
1. 标记优先级
```python
# test_demo.py
import pytest

@pytest.mark.priority('p0')
def test_a():
    pass

@pytest.mark.priority('p1')
def test_b():
    pass

@pytest.mark.priority('p2')
def test_c():
    pass
```
2. 筛选测试用例,例如运行优先级为p0和p1的用例
```shell
pytest test_demo.py --priority=p0 --priority=p1
```