import requests
from PIL import Image
from pathlib import Path

def get_data(url):
    response = requests.get(url, stream=True)
    return(response.content)

def download_image(url: str, dest: Path):
    img_data = get_data(url)
    file = dest / url.split("/")[-1]
    file.write_bytes(img_data)
    return(file.absolute())


if __name__ == "__main__":
    url = "https://cdn-adventures-live.azureedge.net/adventurescache/5/f/d/f/f/8/5fdff8d957e7be6eb341f8c0beee8dd37b9579c9.jpg"

    path = Path()

    print("Downloading image...")
    download_image(url, path)
    print("Done")
