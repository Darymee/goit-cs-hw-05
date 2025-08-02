import argparse
import asyncio
import logging
from pathlib import Path
from sorter import read_folder

logging.basicConfig(
    filename="file_sorter.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def main():
    print("Sorting...")

    parser = argparse.ArgumentParser(
        description="Асинхронне сортування файлів за розширенням."
    )
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до цільової папки")
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    output_path = Path(args.output).resolve()

    if not source_path.exists() or not source_path.is_dir():
        logging.error("Вихідна папка не існує або не є директорією.")
        print("❌ Вихідна папка не існує або не є директорією.")
        return

    await read_folder(source_path, output_path)
    print("Sorting has been completed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Помилка при виконанні: {e}")
        print(f"❌ Помилка при виконанні: {e}")
