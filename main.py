# very simple debian package manager

import requests
import urllib.request
import subprocess
from pathlib import Path

package = input("enter package name: ")

try:
    response = requests.get(f"https://nuribegg.github.io/mirror/{package}")
    html = response.text.lower()

    if response.status_code == 404:
        print("package does not exist on the mirror")

    elif any(text in html for text in [
        "404 not found",
        "page not found",
        "404 - not found",
        "the page you requested could not be found"
    ]):
        print("package probably does not exist")

    elif response.status_code == 200:
        print("package exists, downloading...")
        filename = Path(package).name
        if not filename.endswith(".deb"):
            filename += ".deb"
        download_path = Path.cwd() / filename
        urllib.request.urlretrieve(f"https://nuribegg.github.io/mirror/{package}", download_path)
        subprocess.run(["sudo", "dpkg", "-i", str(download_path)])

    else:
        print(f"http status: {response.status_code}")

except requests.RequestException as e:
    print(f"error: {e}")
