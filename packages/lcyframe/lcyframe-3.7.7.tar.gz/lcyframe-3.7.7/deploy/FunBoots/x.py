def task1():
    """任务1"""
    pass

def task2():
    """
    任务2
    """
    pass

def task3():
    """
    任务3
    """
    pass

def task2_1():
    """
    子任务1
    异步获取结果，放入task2_2的队列中
    """
    pass

def task2_2():
    """
    子任务2
    获取
    """
    pass

[task1, [task2, [task2_1, task2_2]], task3]