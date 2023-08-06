from logging import getLogger, Logger, StreamHandler, Formatter
import sys
from threemystic_common.base_class.base_common import base



class helper_type_logging(base): 
  """This is a set of library wrappers to help around expending dictionary libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_logging", *args, **kwargs)
  
  def get_child_logger(cls, child_logger_name, logger: Logger = None, *args, **kwargs):
    if logger is None:
      logger = getLogger()
    
    return logger.getChild(child_logger_name)

  # set_logger_info
  def set_logger_level(cls, logger: Logger, level, *args, **kwargs):
    logger.setLevel(level= level)

  # set_logger_level_stdout
  def add_handler_logger_stdout(cls, logger: Logger, level, *args, **kwargs):
    handler_name = f"Log STDOUT - {level}"

    if logger.hasHandlers():
      for handler in logger.handlers:
        if handler.name == handler_name:
          return

    handler = StreamHandler(sys.stdout)
    handler.set_name(f"Log STDOUT - {level}")
    handler.setLevel(level)

    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)