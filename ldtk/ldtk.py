import requests

def get_latest():
    r = requests.head('https://github.com/deepnight/ldtk/releases/latest', allow_redirects=True)
    v = r.url[r.url.rindex('/')+1:] # get the latest version number from the url
    print(v)
