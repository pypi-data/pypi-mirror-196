from IPython import display
from ensure import ensure_annotations
from NYRenderer.custom_exception import InvalideURLException
from NYRenderer.logger import logger
from py_youtube import Data


@ensure_annotations
def get_time_info(URL: str) -> int:  # type: ignore
    def _verify_vid_id_len(vid_id, __expected_len=11):
        len_of_vid_id = len(vid_id)
        if len_of_vid_id != __expected_len:
            raise InvalideURLException(
                f"Invalid video id with length: {len_of_vid_id}, expected: {__expected_len}"
            )
    try:
        split_val = URL.split('=')
        if len(split_val) > 3:
            raise InvalideURLException
        if "watch" in URL:
            if ("&t" in URL):
                vid_id, time = split_val[-2][:-2], int(split_val[-1][:-1])
                _verify_vid_id_len(vid_id)
                logger.info("video starts at: %s", time)
                return time
            else:
                vid_id, time = split_val[-1], 0
                _verify_vid_id_len(vid_id)
                logger.info("video starts at: %s", time)
                return time
        else:
            if "=" in URL and "?t" in URL:
                vid_id, time = split_val[0].split('/')[-1][:-2], int(split_val[-1])
                _verify_vid_id_len(vid_id)
                logger.info("video starts at: %s", time)
                return time
            else:
                vid_id, time = URL.split('/')[-1], 0
                _verify_vid_id_len(vid_id)
                logger.info("video starts at: %s", time)
                return time
    except Exception:
        raise InvalideURLException


@ensure_annotations
def render_youtube_video(URL: str, width: int = 780, height: int = 600) -> str:  # type: ignore
    try:
        if URL is None:
            raise InvalideURLException("URL can not be None")
        data = Data(URL).data()
        if data["publishdate"] is not None:
            time = get_time_info(URL)
            vid_ID = data["id"]
            embed_URL = f"https://www.youtube.com/embed/{vid_ID}?start={time}"
            logger.info("embed URL: %s", embed_URL)
            iframe = f"""<iframe 
            width="{width}" height="{height}" 
            src="{embed_URL}" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; 
            autoplay; clipboard-write; 
            encrypted-media; gyroscope; 
            picture-in-picture; web-share" 
            allowfullscreen></iframe>
            """
            display.display(display.HTML(iframe))
            return "success"
        else:
            raise InvalideURLException

    except Exception as e:
        raise e
