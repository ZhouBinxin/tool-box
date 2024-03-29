import requests
import urllib.parse
import os
from dotenv import load_dotenv


class ImageDriver:
    def __init__(self, driver='bing'):
        self.driver = driver

    def get_image_url(self):
        """
        获取图片链接
        :return:
        """
        if self.driver == 'bing':
            return self.get_daily_image()
        return None

    def get_daily_image(self):
        """
        获取每日一图
        :return:
        """
        daily_image_url = ('https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1'
                           '&uhdwidth=3840&uhdheight=2160&setmkt=zh_cn&setlang=zh')
        try:
            r = requests.get(daily_image_url)
            r = r.json()
            return 'https://global.bing.com/' + r['images'][0]['url']
        except Exception as e:
            print(f'获取{self.driver}壁纸失败：{e}')


def download_image(image_url):
    """
    下载图片
    :param image_url: 图片链接
    :return:
    """
    image_id = image_url.split('id=')[1].split('_')[0]
    image_path = f'images/{image_id}.jpg'
    if not os.path.exists(image_path):
        urllib.request.urlretrieve(image_url, image_path)
        print(f'壁纸下载成功：{image_path}')
    else:
        print(f'壁纸已存在：{image_path}')


def main():
    load_dotenv()
    try:
        driver = os.environ['DRIVER']
    except Exception as e:
        print(f'获取DRIVER失败：{e}')
        driver = 'bing'

    image_driver = ImageDriver(driver)
    image_url = image_driver.get_image_url()
    if image_url:
        download_image(image_url)
    else:
        print('获取壁纸链接失败')


if __name__ == '__main__':
    main()
