import logging

class Logger:
    def __init__(self, filename=""):
        if not filename:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename=filename
            )

    def debug(self, msg: str) -> int:
        try: 
            logging.debug(f"{msg}")
            return 0
        except:
            return 1
    
    def info(self, msg: str) -> int:
        try: 
            logging.info(f"{msg}")
            return 0
        except:
            return 1
    
    def warning(self, msg: str) -> int:
        try: 
            logging.warning(f"{msg}")
            return 0
        except:
            return 1

    def error(self, msg: str) -> int:
        try: 
            logging.error(f"{msg}")
            return 0
        except:
            return 1
    
    def critical(self, msg: str) -> int:
        try: 
            logging.critical(f"{msg}")
            return 0
        except:
            return 1
    
