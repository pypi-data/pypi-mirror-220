from .. import consts, globals, ocr
from ..controller import Buttons, pro
from ..utils.log import logger


def process_race(race_mode=0):
    logger.info("Start racing.")
    track = None
    progress = None
    for i in range(60):
        if track:
            progress = ocr.OCR.get_progress()
            logger.info(f"Current progress is {progress}")
            if progress < 0 and ocr.OCR.has_next():
                break
        else:
            page = ocr.OCR.get_page()
            if page.name == consts.loading_race:
                track = ocr.OCR.get_track()
                if track:
                    logger.info(f"Current track is {track['trackcn']}")
            if page.name in [
                consts.race_score,
                consts.race_results,
                consts.race_reward,
                consts.system_error,
                consts.connect_error,
                consts.no_connection,
            ]:
                break

        pro.press_button(Buttons.Y, 0.7)
        pro.press_button(Buttons.Y, 0)

    globals.FINISHED_COUNT += 1
    logger.info(f"Already finished {globals.FINISHED_COUNT} times loop count = {i}.")
