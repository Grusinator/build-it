import requests
import os


def download_threejs(destination_folder):
    # URL of the minified Three.js library from the official CDN
    threejs_url = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"

    response = requests.get(threejs_url)
    response.raise_for_status()  # Raise an error if the download fails

    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Path to save the file
    file_path = os.path.join(destination_folder, "three.min.js")

    with open(file_path, 'wb') as file:
        file.write(response.content)

    print(f"Three.js downloaded to {file_path}")


if __name__ == "__main__":
    destination = "./static"  # You can change this to your desired folder
    download_threejs(destination)
