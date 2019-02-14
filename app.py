import os
import json
import urllib.request
import urllib.parse

from gi.repository import Gio


API_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
BING_URL = 'https://www.bing.com'
PATH = os.path.dirname(os.path.abspath(__file__))

def run():
    resp = urllib.request.urlopen(API_URL)
    if resp.status == 200:
        data = json.loads(resp.read())
        set_wallpaper(data)

def set_wallpaper(data):
    if data.get('images'):
        _img = data['images'][0]['url']
        _, ext = os.path.splitext(_img)
        img_url = urllib.parse.urljoin(BING_URL, _img)
        dl_name = 'today{}'.format(ext)
        wp_path = os.path.join(PATH, dl_name)
        urllib.request.urlretrieve(img_url, wp_path)                        
        gsettings = Gio.Settings.new('org.cinnamon.desktop.background')
        gsettings.set_string('picture-uri', 'file://{}'.format(wp_path))
        gsettings.apply()

if __name__ == "__main__":
    run()