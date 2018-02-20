import os
import urllib
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup


def unwrap_self_f(arg, **kwarg):
    return zangsisiCrawler.get_contents(*arg, **kwarg)


class zangsisiCrawler:
    def __init__(self, p):
        self.directory = ""
        self.links = []
        self.url = 'http://zangsisi.net/?p=' + str(p)
        pass

    def get_links(self):
        req = requests.get(self.url)
        data = req.text

        soup = BeautifulSoup(data, 'html.parser')
        title = soup.select('.title')

        self.directory = title[1].string
        os.mkdir(self.directory)

        for link in soup.select('#post > div > p > a'):
            self.links.append(link.get('href'))
            pass
        pass

    def get_contents(self, link):
        page = BeautifulSoup(requests.get(link).text, 'html.parser')

        title = page.select('.title')[1].string
        images = page.select('.contents > p > a')
        count = 0

        path = './' + self.directory + '/' + title
        os.mkdir(path)

        print("<< START >>\t" + title)

        for image in images:
            count += 1
            imageUrl = urllib.quote(image.get('href').encode('utf8'), ':/')
            urllib.urlretrieve(imageUrl, path + '/' + os.path.basename(imageUrl))
            pass

        print("<<  END  >>\t" + title)
        pass

    def run(self):
        print("==== crawling start ====")

        self.get_links()
        pool = Pool(processes=4)
        pool.map(unwrap_self_f, zip([self] * len(self.links), self.links))
        pool.close()

        print("==== crawling end ====")
        pass


if __name__ == '__main__':
    zangsisi = zangsisiCrawler(11959)
    zangsisi.run()
    pass
