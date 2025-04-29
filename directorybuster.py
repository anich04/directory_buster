import requests
import argparse
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from collections import deque
from colorama import Fore, Style, init

init(autoreset=True)

def check_directory(base_url, word, headers, status_filter):
    url = urljoin(base_url, word)
    try:
        response = requests.get(url, headers=headers, timeout=5)
        status = response.status_code
        if status in status_filter:
            if status == 200:
                color = Fore.GREEN
            elif status in [301, 302]:
                color = Fore.YELLOW
            elif status == 403:
                color = Fore.RED
            else:
                color = Fore.CYAN
            print(f"{color}[{status}] {url}{Style.RESET_ALL}")
            if url.endswith('/'):
                return url  # Return directory for recursion
    except requests.RequestException:
        pass
    return None

def load_wordlist(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def recursive_bust(base_url, wordlist, headers, status_filter, max_threads):
    visited = set()
    queue = deque([base_url])

    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        print(Fore.CYAN + f"\n[+] Scanning: {current_url}" + Style.RESET_ALL)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {
                executor.submit(check_directory, current_url, word, headers, status_filter): word
                for word in wordlist
            }

            for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning"):
                result = future.result()
                if result and result not in visited:
                    queue.append(result)

def main():
    parser = argparse.ArgumentParser(description="Recursive Directory Buster")
    parser.add_argument("url", help="Base URL to scan (e.g., https://example.com/)")
    parser.add_argument("wordlist", help="Path to wordlist file")
    parser.add_argument("--threads", type=int, default=20, help="Number of threads (default: 20)")
    parser.add_argument("--status", nargs="+", type=int, default=[200, 301, 302], help="Status codes to include")
    parser.add_argument("--user-agent", default="DirBuster/1.0", help="User-Agent header")
    parser.add_argument("--referer", help="Referer header")
    args = parser.parse_args()

    headers = {"User-Agent": args.user_agent}
    if args.referer:
        headers["Referer"] = args.referer

    wordlist = load_wordlist(args.wordlist)
    recursive_bust(args.url, wordlist, headers, args.status, args.threads)

if __name__ == "__main__":
    main()
