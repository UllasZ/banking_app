import logging
from pathlib import Path

from src.banking_app.utils.file_operator import FileOperator


class Logger:
    project_base_path = Path(__file__).parent.parent.parent

    log_file_path = f"{project_base_path}/logs"
    file_operator = FileOperator(folder_path=log_file_path)
    file_operator.create_folder()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        filename=f"{log_file_path}/banking_app.log",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


logger = Logger()
log = logging
log.info("Logger initiated!")
