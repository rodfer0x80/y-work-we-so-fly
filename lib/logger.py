import logging

class Logger:
    def __init__(self, filename="", level="DEBUG"):
        if empty(filename):
            logging.basicConfig(level=logging.f"{level}")
        else:
            logging.basicConfig(
                    level=logging.f"{level}",
                    format="%(asctime)s %(levelname)s %(message)s"
                    datefmt="%Y-%m-%d %H:%M:%S"
                    filename=filename
            )
    def debug(msg: str) -> bool:
        try: 
            logging.debug(f"{msg}")
            return True
        except:
            return False
    
    def info(msg: str) -> bool:
        try: 
            logging.info(f"{msg}")
            return True 
        except:
            return False
    
    def warning(msg: str) -> bool:
        try: 
            logging.warning(f"{msg}")
            return True
        except:
            return False

    def error(msg: str) -> bool:
        try:
            logging.error(f"{msg}")
            return True
        except:
            return False

    def critical(msg: str) -> bool:
        try:
            logging.critical(f"{msg}")
            return True
        except:
            return False
