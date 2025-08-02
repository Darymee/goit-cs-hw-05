import logging
import shutil
import os
from pathlib import Path
import asyncio
import functools

logging.basicConfig(
    filename="file_sorter.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def copy_file(file_path: Path, output_dir: Path):
    try:
        extension = file_path.suffix[1:] or "no_extension"
        target_dir = output_dir / extension

        loop = asyncio.get_running_loop()
        mkdir = functools.partial(os.makedirs, target_dir, exist_ok=True)
        await loop.run_in_executor(None, mkdir)

        await loop.run_in_executor(
            None, shutil.copy2, file_path, target_dir / file_path.name
        )
        print(f"Copied {file_path} to {target_dir}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


async def read_folder(source_dir: Path, output_dir: Path):
    tasks = []
    try:
        for item in source_dir.iterdir():
            if item.is_dir():
                tasks.append(read_folder(item, output_dir))
            elif item.is_file():
                tasks.append(copy_file(item, output_dir))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error reading folder {source_dir}: {e}")
