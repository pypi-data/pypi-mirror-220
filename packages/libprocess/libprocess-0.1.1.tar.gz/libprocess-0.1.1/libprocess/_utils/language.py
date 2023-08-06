from typing import Union

import langcodes
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0


def detect_iso6393(lang_str: str) -> Union[str, None]:
    """
    Detect language and return ISO 639-3 code.
    The detection is not 100% accurate.
    """

    try:
        language = detect(lang_str)
    except LangDetectException:
        return None

    return langcodes.Language.get(language).to_alpha3()
