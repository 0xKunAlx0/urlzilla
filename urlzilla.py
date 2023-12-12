import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from requests.exceptions import RequestException

print(" _    _ _____  _      _______ _ _       ")
print("| |  | |  __ \| |    |___  (_) | |      ")
print("| |  | | |__) | |       / / _| | | __ _ ")
print("| |  | |  _  /| |      / / | | | |/ _` |")
print("| |__| | | \ \| |____ / /__| | | | (_| |")
print(" \____/|_|  \_\______/_____|_|_|_|\__,_|") 
print("                                        ")
print("                                      - Created By KunAl ")                               

def get_links_with_parameters(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            # Add any other headers as needed
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except RequestException as e:
        print(f"An error occurred: {e}")
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for a_tag in soup.find_all('a', href=True):
        link = urljoin(url, a_tag['href'])
        links.add(link)

    return links

def crawl_with_parameters(url, max_depth, output_file=None):
    visited = set()
    to_visit = [(url, 0)]
    output_data = []

    try:
        while to_visit:
            current_url, depth = to_visit.pop()
            if current_url in visited or depth > max_depth:
                continue

            print(f"Crawling: {current_url}")
            output_data.append(current_url)

            links = get_links_with_parameters(current_url)
            new_links = [link for link in links if link not in visited]
            for link in new_links:
                to_visit.append((link, depth + 1))

            visited.add(current_url)

    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")
    except RequestException as e:
        print(f"An error occurred: {e}")
        if output_file:
            save_output(output_file, output_data)

def save_output(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write("%s\n" % item)

def main():
    parser = argparse.ArgumentParser(description="Web Crawler made by KunAl")
    parser.add_argument("-u", "--url", required=True, help="Website URL (predefined with 'https://' or 'http://')")
    parser.add_argument("-d", "--depth", type=int, default=3, help="Maximum depth for crawling (default: 3)")
    parser.add_argument("-o", "--output", help="Output file to save the results")
    args = parser.parse_args()

    # Ensure the URL starts with "https://" or "http://"
    if not args.url.startswith("https://") and not args.url.startswith("http://"):
        args.url = "https://" + args.url

    # Example usage
    crawl_with_parameters(args.url, max_depth=args.depth, output_file=args.output)

if __name__ == "__main__":
    main()
