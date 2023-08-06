import os
import re

import pytesseract
from PIL import Image, ImageFilter

from . import consts
from .page_factory import factory
from .screenshot import screenshot
from .utils.log import logger
from .utils.track_data import track_data


class LogManager:
    log_texts = None
    log_text_index = 0

    @classmethod
    def get_text(cls):
        if not cls.log_texts:
            cls.log_texts = []
            with open("logs/race.log") as file:
                lines = file.readlines()
            for line in lines:
                match = re.search(r"'text':\s*'(.*?)'", line)
                match1 = re.search(r"'text':\s*\"(.*?)\"", line)
                if match:
                    text = match.group(1)
                    cls.log_texts.append(text)
                elif match1:
                    text = match1.group(1)
                    cls.log_texts.append(text)
        text = cls.log_texts[cls.log_text_index]
        cls.log_text_index += 1
        return text


class OCR:
    filename = "output.jpg"

    @classmethod
    def get_text(cls):
        debug = os.environ.get("A9_DEBUG", 0)
        if debug:
            text = LogManager.get_text()
        else:
            text = cls._get_text(config="--psm 11", replace=True)
        return text

    @classmethod
    def get_page(cls):
        """获取匹配页面"""
        screenshot()
        text = cls.get_text()
        page = factory.create_page(text)
        logger.info(f"ocr page dict = {page.dict}")
        return page

    @classmethod
    def get_track(cls):
        """识别赛道"""
        text = cls._get_text(crop=(0, 0, 600, 300), replace=True)
        logger.info(f"ocr page map result = {text}")
        for track in track_data:
            if track["tracken"] in text:
                logger.info(f"Get track = {track}")
                return track

    @classmethod
    def get_progress(cls):
        """识别进度"""
        screenshot()
        text = cls._get_text(crop=(150, 80, 400, 140), replace=True)
        pattern = r"\b\d{1,3}\b"
        match = re.search(pattern, text)
        if match:
            return int(match.group())
        return -1

    @classmethod
    def has_play(cls, mode):
        """是否有PLAY按钮"""
        if mode in [consts.car_hunt_zh, consts.legendary_hunt_zh]:
            crop = (1550, 900, 1675, 1080)
        else:
            crop = (1600, 900, 1750, 1080)
        text = cls._get_text(
            crop=crop,
            filter=ImageFilter.SHARPEN,
            convert="L",
            replace=True,
        )
        return "PLAY" in text

    @classmethod
    def has_next(cls):
        """是否有NEXT按钮"""
        text = cls._get_text(
            crop=(1460, 900, 1750, 1040),
            filter=ImageFilter.SHARPEN,
            replace=True,
        )
        return "NEXT" in text
    
    @classmethod
    def get_ticket(cls):
        """获取票数"""
        text = cls._get_text(
            crop=(1650, 250, 1755, 300),
            filter=ImageFilter.SHARPEN,
            convert="L",
            replace=True,
        )
        r = re.findall("(\d+)/10")
        if r:
            return int(r[0])
        return -1

    @classmethod
    def _get_text(
        cls, crop=None, filter=None, convert=None, replace=None, config="--dpi 72"
    ):
        img = Image.open(cls.filename)
        if crop:
            img = img.crop(crop)
        if filter:
            img = img.filter(filter)
        if convert:
            img = img.convert(convert)
        text: str = pytesseract.image_to_string(img, lang="eng", config=config)
        img.close()
        if replace:
            text = text.replace("\n", " ")
        return text


if __name__ == "__main__":
    OCR.get_text()
