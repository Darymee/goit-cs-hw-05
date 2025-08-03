import requests
import re
import matplotlib.pyplot as plt
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import os


def map_function(text_chunk):
    words = re.findall(r"\b\w+\b", text_chunk.lower())
    return Counter(words)


def reduce_counters(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter


def visualize_top_words(word_counts, top_n=10):
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)

    plt.figure(figsize=(10, 5))
    plt.barh(words[::-1], counts[::-1], color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.tight_layout()
    plt.show()


def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def main():
    url = "https://dgoldberg.sdsu.edu/515/harrypotter.txt"
    text = download_text(url)

    num_chunks = os.cpu_count() or 4
    chunk_size = len(text) // num_chunks
    text_chunks = [
        text[i * chunk_size : (i + 1) * chunk_size] for i in range(num_chunks)
    ]

    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        map_results = list(executor.map(map_function, text_chunks))

    word_counts = reduce_counters(map_results)
    visualize_top_words(word_counts, top_n=10)


if __name__ == "__main__":
    main()
