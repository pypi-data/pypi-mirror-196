from IPython import display
from ensure import ensure_annotations
import urllib.request
from NYRenderer.custom_exception import InvalideURLException
from NYRenderer.logger import logger


@ensure_annotations
def is_valid(url: str) -> bool:
    try:
        response_status = urllib.request.urlopen(url).getcode()
        assert response_status == 200
        logger.debug("response status: %s", response_status)
        return True
    except Exception as e:
        logger.exception(e)
        return False


@ensure_annotations
def render_site(url: str, width: str = "100%", height: str = "600") -> str:
    try:
        if is_valid(url):
            response = display.IFrame(src=url, width=width, height=height)
            display.display(response)
            return "success"
        else:
            raise InvalideURLException
    except Exception as e:
        raise e
