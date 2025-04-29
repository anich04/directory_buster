# Directory Buster Tool

A simple yet powerful recursive directory buster tool built in Python. This tool helps in discovering hidden directories and files on a target website by using a wordlist. It supports multithreading for faster scanning and offers CLI-based control over various settings like status codes, threads, and headers.

## Features

- **Multithreading:** Scans faster with **ThreadPoolExecutor**.
- **Recursive Scanning:** Automatically scans discovered directories.
- **CLI Control:** Customize with arguments for URL, wordlist, status codes, threads, and headers.
- **Color-Coded Output:** Makes results easier to read with **colorama**.
- **Custom Headers:** Set custom User-Agent and Referer headers.

## Installation

### Requirements

- Python 3.x
- `requests` library
- `tqdm` library (for progress bars)
- `colorama` library (for color output)

Install required libraries using:

```bash
pip install -r requirements.txt

``` usage 
python directory_buster.py <URL> <WORDLIST> [options]
