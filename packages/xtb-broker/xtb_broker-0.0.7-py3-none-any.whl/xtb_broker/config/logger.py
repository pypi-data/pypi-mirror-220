import logging
from config.constants import LOG_LEVEL

logger = logging.getLogger("xtb-broker")
logger.setLevel(getattr(logging, LOG_LEVEL))

FORMAT = '[%(asctime)-15s][%(thread)d][%(levelname)s][%(module)s::%(funcName)s:%(lineno)d] - %(message)s'
logging.basicConfig(format=FORMAT)


