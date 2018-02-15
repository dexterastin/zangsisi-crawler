import os
import urllib
import requests

from bs4 import BeautifulSoup


class zangsisiCrawler:
    def __init__(self, p):
        self.url = 'http://zangsisi.net/?p=' + str(p)
        pass

    def crawling(self):
        req = requests.get(self.url)
        data = req.text

        soup = BeautifulSoup(data, 'html.parser')
        title = soup.select('.title')

        dir = title[1].string
        os.mkdir(dir)

        for link in soup.select('#post > div > p > a'):
            page = BeautifulSoup(requests.get(link.get('href')).text, 'html.parser')

            title = page.select('.title')[1].string
            images = page.select('.contents > p > a')
            count = 0

            path = './' + dir + '/' + title
            os.mkdir(path)

            for image in images:
                count += 1
                imageUrl = image.get('href')
                urllib.urlretrieve(imageUrl, path + '/' + os.path.basename(imageUrl))
                pass
            pass
        pass


if __name__ == '__main__':
    zangsisi = zangsisiCrawler(11962)
    zangsisi.crawling()
    pass
