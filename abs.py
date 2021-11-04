import subprocess
from pathlib import Path
import sys

APP_ID = "com.snowcorp.stickerly.android"


def prepare(backup_folder: Path):
    backup_folder.mkdir(exist_ok=True)
    (backup_folder / "apps").mkdir(exist_ok=True)


def apk_backup(app_id: str, backup_folder: Path):
    ((backup_folder / "apps") / app_id / "apks").mkdir(exist_ok=True, parents=True)
    base_apk_path: Path = Path(subprocess.run(
        ["su", "-c", f"pm path {app_id}"],
        capture_output=True
    ).stdout.decode("utf-8").split(":")[1])
    apk_folder = base_apk_path.parent
    apks = list(
        map(
            Path,
            filter(
                lambda item: item.endswith(".apk"),
                subprocess.run(
                    ["su", "-c", f"ls {apk_folder}"],
                    capture_output=True
                ).stdout.decode("utf-8").splitlines()
            )
        )
    )
    for apk in apks:
        subprocess.run(
            ["su", "-c", f"cp {apk_folder/apk} {str(backup_folder/'apps'/app_id/'apks')}"]
        )


def data_backup(app_id: str, backup_folder: Path):
    ((backup_folder / "apps") / app_id / "data").mkdir(exist_ok=True, parents=True)
    subprocess.run(
        ["su", "-c", f"tar -cvf {str(backup_folder/'apps'/app_id/'data'/(app_id+'.data.tar'))} /data/data/{app_id}"]
    )


if __name__ == "__main__":
    backup_path = Path(sys.argv[1])
    prepare(backup_path)
    apk_backup("com.snowcorp.stickerly.android", backup_path)
    data_backup("com.snowcorp.stickerly.android", backup_path)
