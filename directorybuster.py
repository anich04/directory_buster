import os
import requests
import threading
import time
import json
from queue import Queue
from tqdm import tqdm  # Progress bar library

# Function to check the URL with the wordlist
def check_directory(target, word, queue, headers, delay):
    url = f"{target}/{word}"
    try:
        # Adding delay to prevent overwhelming the server
        time.sleep(delay)
        
        response = requests.get(url, headers=headers)
        queue.put((url, response.status_code, response.elapsed.total_seconds()))
        print(f"Checked: {url} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        queue.put((url, 'Error', None))

# Function to run the scan
def scan_directories(target, wordlist, headers, status_codes, threads=10, delay=1):
    queue = Queue()
    threads_list = []
    total_words = len(wordlist)

    # Create progress bar
    with tqdm(total=total_words, desc="Scanning Directories", ncols=100) as pbar:
        for word in wordlist:
            # Start a thread for each directory to scan
            thread = threading.Thread(target=check_directory, args=(target, word, queue, headers, delay))
            threads_list.append(thread)
            thread.start()

            # Limit number of threads
            if len(threads_list) >= threads:
                for t in threads_list:
                    t.join()
                threads_list = []

            pbar.update(1)

        for t in threads_list:
            t.join()

    # Collect results
    results = []
    while not queue.empty():
        url, status, response_time = queue.get()
        if status in status_codes:
            results.append({
                "url": url,
                "status": status,
                "response_time": response_time
            })

    return results

# Save results to JSON
def save_results(results):
    with open("scan_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n✅ Scan complete. Results saved to 'scan_report.json'.")

# Main function
def main():
    target = input("Enter target URL (e.g., http://example.com): ")
    wordlist_file = input("Enter wordlist file path: ")

    if not os.path.exists(wordlist_file):
        print("Wordlist file not found!")
        return

    # Input for HTTP Headers
    user_agent = input("Enter custom User-Agent (leave blank for default): ")
    referer = input("Enter Referer header (leave blank for default): ")

    headers = {
        'User-Agent': user_agent if user_agent else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': referer if referer else ''
    }

    # Status codes to filter
    status_codes = input("Enter status codes to filter (comma separated, e.g., 200,301): ").split(",")
    status_codes = [int(code.strip()) for code in status_codes]

    # Input for delay between requests
    delay = float(input("Enter delay between requests (in seconds, e.g., 1): "))

    with open(wordlist_file, 'r') as file:
        wordlist = [line.strip() for line in file.readlines()]

    results = scan_directories(target, wordlist, headers, status_codes, delay=delay)

    # Save results to JSON
    save_results(results)

if __name__ == "__main__":
    main()
