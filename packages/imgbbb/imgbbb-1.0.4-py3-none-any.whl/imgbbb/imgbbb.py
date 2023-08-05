import os
import re
import time
import requests
import argparse
from fake_useragent import UserAgent
from requests_toolbelt.multipart.encoder import MultipartEncoder

def data_save(data):
    try:
        with open("db.txt", "x") as file:
            file.write(data)
    except FileExistsError:
        with open("db.txt", "a") as file:
            file.write(data)
    except Exception as e:
        print("Error creating or appending to the file:", str(e))

class ImgBbUploader:
    def __init__(self):
        self.ua = UserAgent()
        self.user_agent = self.ua.random
        self.auth_token = self._get_auth_token()
        self.image_url = None
        self.viewer_url = None
        self.delete_url = None
        self.display_url = None
        self.contact = "https://t.me/OneFinalHug"

    def _get_auth_token(self):
        req = requests.get("https://imgbb.com/")
        if req.status_code == 200:
            HUG = re.search(r'[a-zA-Z0-9]{40}', req.text)
            OneFinalHug = HUG[0]
        else:
            OneFinalHug = "6e7d410cb153b3757a3edc0d035f630b051b5e94"
        return OneFinalHug

    def upload_image(self, image_path):
        file_name = os.path.basename(image_path)
        
        headers = {
            'authority': 'imgbb.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://imgbb.com',
            'referer': 'https://imgbb.com/',
            'user-agent': self.user_agent,
        }

        try:
            with open(image_path, "rb") as image_file:
                file_content = image_file.read()
        except FileNotFoundError:
            print("Image Not Found")
            return

        data = {
            'source': (file_name, file_content, 'image/jpeg'),
            'type': 'file',
            'action': 'upload',
            'timestamp': str(int(time.time() * 1000)),
            'auth_token': self.auth_token
        }
        m = MultipartEncoder(fields=data)

        headers['Content-Type'] = m.content_type

        response = requests.post('https://imgbb.com/json', headers=headers, data=m)
        if response.status_code == 200:
            re_data = response.json()["image"]
            self.image_url = re_data["url"]
            self.viewer_url = re_data["url_viewer"]
            self.delete_url = re_data["delete_url"]
            self.display_url = re_data["url"]
            url_to_append = f"Image: {self.display_url}\nDelete: {self.delete_url}\n"
            data_save(url_to_append)
            return re_data
        else:
            return "Oops! Unable to upload the image."

    def upload_url(self, url):
        headers = {
            'Accept': 'application/json',
            'Referer': 'https://imgbb.com/',
            'User-Agent': self.user_agent
        }

        payload = MultipartEncoder(
            fields={
                'source': url,
                'type': 'url',
                'action': 'upload',
                'timestamp': str(int(time.time() * 1000)),
                'auth_token': self.auth_token
            }
        )
        headers['Content-Type'] = payload.content_type

        response = requests.post('https://imgbb.com/json', headers=headers, data=payload)

        if response.status_code == 200:
            re_data = response.json()["image"]
            self.image_url = re_data["url"]
            self.viewer_url = re_data["url_viewer"]
            self.delete_url = re_data["delete_url"]
            self.display_url = re_data["url"]
            url_to_append = f"Image: {self.display_url}\nDelete: {self.delete_url}\n"
            data_save(url_to_append)
            return re_data
        else:
            return "Oops! Unable to upload the image."

def main():
    parser = argparse.ArgumentParser(description='Upload an image to ImgBB without API key\n it\'s using public API so don\'t use personal or private photos :)')
    parser.add_argument('-i', '--image', help='path to image file to upload')
    parser.add_argument('-u', '--url', help='URL of image to upload')
    args = parser.parse_args()

    uploader = ImgBbUploader()

    if args.image:
        result = uploader.upload_image(args.image)
        print(result)
    elif args.url:
        result = uploader.upload_url(args.url)
        print(result)
    else:
        print("Please provide either an image file or a URL to upload.")

if __name__ == "__main__":
    main()
