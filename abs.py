import subprocess
import shlex
from pathlib import Path
import sys

APP_ID = "com.snowcorp.stickerly.android"


def prepare(backup_folder: Path):
    backup_folder.mkdir(exist_ok=True)
    (backup_folder/"apps").mkdir(exist_ok=True)


def apk_backup(app_id: str, backup_folder: Path):
    ##
    print(app_id, backup_folder)
    ##
    ((backup_folder/"apps")/app_id).mkdir(exist_ok=True)
    base_apk_path: str = subprocess.run(
        ["pm", "path", app_id],
        capture_output=True
    ).stdout.decode("utf-8").split(":")[1]
    print("base_apk_path", base_apk_path)
    return
    subprocess.run(
        [
            "tar",
            "-cvf",
            f"{app_id}.appdata.tar",
            f"/data/app/"
        ]
    )


if __name__ == "__main__":
    backup_path = "test_bak"
    prepare(backup_path)
    apk_backup("com.whatsapp", backup_path)
