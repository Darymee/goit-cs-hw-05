import logging
from aiopath import AsyncPath
import aioshutil
import asyncio

logging.basicConfig(
    filename="file_sorter.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def copy_file(file_path: AsyncPath, output_dir: AsyncPath):
    try:
        extension = file_path.suffix[1:] or "no_extension"
        target_dir = output_dir / extension
        await target_dir.mkdir(parents=True, exist_ok=True)
        await aioshutil.copy(file_path, target_dir / file_path.name)
        print(f"Copied {file_path} to {target_dir}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


async def read_folder(source_dir: AsyncPath, output_dir: AsyncPath):
    try:
        tasks = []
        async for item in source_dir.iterdir():
            if await item.is_dir():
                tasks.append(read_folder(item, output_dir))
            elif await item.is_file():
                tasks.append(copy_file(item, output_dir))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error reading folder {source_dir}: {e}")
