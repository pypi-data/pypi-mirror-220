import time
from ..controller import pro, Buttons
from .. import globals


def connect_controller():
    """连接手柄"""
    pro.press_buttons([Buttons.L, Buttons.R], down=1)
    time.sleep(1)
    pro.press_buttons([Buttons.A], down=0.5)


def restart():
    """重启游戏"""
    # 回到主页
    pro.press_button(Buttons.HOME, 3)
    # 切到第二个游戏
    pro.press_button(Buttons.DPAD_RIGHT, 1)
    # 按一下确认打开，再按一下确认关闭
    pro.press_group([Buttons.A] * 2, 1)
    pro.press_button(Buttons.B, 1)
    # 回到A9
    pro.press_button(Buttons.DPAD_LEFT, 1)
    # 进入游戏
    pro.press_group([Buttons.A] * 2, 2)


def demoted():
    """降级"""
    globals.DIVISION = ""
    pro.press_button(Buttons.B, 3)


def set_eng():
    pass


def _add_task():
    if globals.task_queue.empty():
        globals.task_queue.put(globals.CONFIG["模式"])


def system_error():
    pro.press_group([Buttons.A] * 3, 3)
    _add_task()


def loading_game():
    _add_task()
