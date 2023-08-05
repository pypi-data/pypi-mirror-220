![Logo](https://gist.githubusercontent.com/OneFinalHug/919dc87b426aad4ade68de63897e91fb/raw/235ae0ae7bea0c5c551314408448de788af3c89c/imgbbb.svg)

# Imgbb public Uploader 
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/onefinalhug) 

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)

### Upload Images without API key
- Unlimited uploads
- No API limit
- Support Url & Local upload 
- Image link and delete link saved in db.txt.

⚠️ **Warning**: Do not upload private or personal pictures because this library uses the Imgbb public API

## Install
```
pip install imgbbb
```
## Example use

#### Local upload

```
from imgbbb import ImgBbUploader

upload = ImgBbUploader()
up = upload.upload_image("Drive/lol/ofh.jpg")#full image path
print(up)
```
```
>>> imgbbb -i Drive/lol/ofh.jpg
```
#### Url upload
```
from imgbbb import ImgBbUploader

upload = ImgBbUploader()
up = upload.upload_url("https://i.pinimg.com/originals/fe/ea/71/feea71eaa793b00d9e927985a9d4b199.jpg")
print(up)
```
```
imgbbb -u https://i.pinimg.com/originals/fe/ea/71/feea71eaa793b00d9e927985a9d4b199.jpg
```
