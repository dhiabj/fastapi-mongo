import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


def fetch_free_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    proxies = []
    table = soup.find("table", class_="table table-striped table-bordered")
    for row in table.tbody.find_all("tr"):
        cols = row.find_all("td")
        # Filter for proxies that support HTTPS destinations
        if cols[6].text == "yes":
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"http://{ip}:{port}")
    return proxies


def test_proxy(proxy):
    test_url = "https://httpbin.org/ip"
    try:
        response = requests.get(
            test_url,
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ {proxy} works! IP: {response.json()['origin']}")
            return proxy
    except Exception as e:
        print(f"❌ {proxy} failed: {str(e)}")
    return None


def test_proxies(proxies, max_workers=10):
    working_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(test_proxy, proxies)
        for result in results:
            if result:
                working_proxies.append(result)
    return working_proxies


if __name__ == "__main__":
    print("Fetching proxies...\n")
    proxies = fetch_free_proxies()
    print("Testing proxies...\n")
    working_proxies = test_proxies(proxies)

    print("\nResults:")
    if working_proxies:
        print(f"🟢 Working proxies ({len(working_proxies)}):")
        for proxy in working_proxies:
            print(f" - {proxy}")
        # Save working proxies to a file
        with open("working_proxies.txt", "w") as f:
            f.write("\n".join(working_proxies))
        print("\nSaved working proxies to 'working_proxies.txt'")
    else:
        print("🔴 No working proxies found.")
