import time

from .. import consts, globals, tasks
from ..actions import process_race
from ..controller import Buttons, pro
from ..ocr import OCR
from ..utils.log import logger
from ..tasks import TaskManager


def world_series_reset():
    division = globals.DIVISION
    if not division:
        division = "青铜"
    config = globals.CONFIG["多人一"][division]
    level = config["车库等级"]
    left_count_mapping = {"青铜": 4, "白银": 3, "黄金": 2, "铂金": 1}
    pro.press_group([Buttons.DPAD_UP] * 4, 0)
    pro.press_group([Buttons.DPAD_RIGHT] * 6, 0)
    pro.press_group([Buttons.DPAD_LEFT] * 1, 0)
    pro.press_group([Buttons.DPAD_DOWN] * 1, 0)
    pro.press_group([Buttons.DPAD_LEFT] * left_count_mapping.get(level), 0)
    time.sleep(1)
    pro.press_a(2)


def default_reset():
    pass


def other_series_reset():
    pro.press_button(Buttons.ZL, 0)


def carhunt_reset():
    pro.press_button(Buttons.ZR, 0)
    pro.press_button(Buttons.ZL, 1)


def default_positions():
    positions = []
    for row in [1, 2]:
        for col in [1, 2, 3]:
            positions.append({"row": row, "col": col})
    return positions


def world_series_positions():
    division = globals.DIVISION
    if not division:
        division = "青铜"
    config = globals.CONFIG["多人一"][division]
    return config["车库位置"]


def mp3_position():
    return globals.CONFIG["多人三"]["车库位置"]


def other_series_position():
    return globals.CONFIG["多人二"]["车库位置"]


def carhunt_position():
    return globals.CONFIG["寻车"]["车库位置"]


def legendary_hunt_position():
    return globals.CONFIG["传奇寻车"]["车库位置"]


def get_race_config():
    mode = globals.MODE if globals.MODE else globals.CONFIG["模式"]
    logger.info(f"Get mode {mode} config.")
    if mode in [consts.mp_zh, consts.mp1_zh]:
        if globals.CONFIG["模式"] == consts.mp3_zh:
            return mp3_position(), other_series_reset, consts.mp3_zh
        elif globals.CONFIG["模式"] == consts.mp2_zh:
            return other_series_position(), other_series_reset, consts.mp2_zh
        else:
            return world_series_positions(), world_series_reset, consts.mp1_zh
    elif mode == consts.car_hunt_zh:
        return carhunt_position(), carhunt_reset, mode
    elif mode == consts.legendary_hunt_zh:
        return legendary_hunt_position(), carhunt_reset, mode
    else:
        return default_positions(), default_reset, mode


def move_to_position(positions, reset, mode):
    if globals.SELECT_COUNT[mode] >= len(positions):
        globals.SELECT_COUNT[mode] = 0
    if positions:
        reset()
        position = positions[globals.SELECT_COUNT[mode]]
        logger.info(
            f"Start try position = {position}, count = {globals.SELECT_COUNT[mode]}"
        )
        for i in range(position["row"] - 1):
            pro.press_button(Buttons.DPAD_DOWN, 0)

        for i in range(position["col"] - 1):
            pro.press_button(Buttons.DPAD_RIGHT, 0)

    time.sleep(2)


def select_car():
    # 选车
    logger.info("Start select car.")
    while globals.G_RUN.is_set():
        positions, reset, mode = get_race_config()
        move_to_position(positions, reset, mode)
        # 进入车辆详情页
        pro.press_group([Buttons.A], 2)
        page = OCR.get_page()
        # 如果没有进到车辆详情页面, router到默认任务
        if page.name != consts.car_info:
            TaskManager.task_enter(globals.CONFIG["模式"], page)
            return
        # 如果车辆详情页有段位信息，说明车库段位与实际段位不匹配
        if  page.has_text(
                "BRONZE|SILVER|GOLD|PLATINUM"
            ):
            globals.DIVISION = ""
        # 判断是否有play按钮
        if not OCR.has_play(mode):
            pro.press_b()
            globals.SELECT_COUNT[mode] += 1
            continue
        # 判断寻车是否有票
        if mode in [consts.car_hunt_zh, consts.legendary_hunt_zh] and OCR.get_ticket() == 0:
            pro.press_a(2)
            pro.press_button(Buttons.DPAD_DOWN, 2)
            pro.press_a(2)
            pro.press_b(2)
        pro.press_a(2)
        break
    process_race()
    tasks.TaskManager.set_done()
