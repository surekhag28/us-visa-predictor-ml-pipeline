import sys
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)50s:%(lineno)4s - %(funcName)25s() ] - ( %(levelname)5s ) %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)