from app.utils.file_utils import LOGS_DIR


def load_log_file(filename: str) -> list[str]:
    file_path = LOGS_DIR / filename

    with open(file_path, "r") as file:
        logs = file.readlines()

    return [log.strip() for log in logs]


def load_all_logs() -> dict:
    all_logs = {}

    for file_path in LOGS_DIR.glob("*.log"):
        with open(file_path, "r") as file:
            logs = [line.strip() for line in file.readlines()]

        all_logs[file_path.name] = logs

    return all_logs