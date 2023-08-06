import requests
from lxml import etree


def booting(key: str):
    try:
        tree = etree.HTML(requests.get('https://booting.lofter.com/').text)
        hrefs = tree.xpath('//*[@id="main"]/div/div/div[2]/a[2]/@href')
        dictionary = {}
        for href in hrefs:
            data = etree.HTML(requests.get(href).text)
            key_cell = data.xpath('//*[@id="main"]/div[1]/div/h2/a/text()')[0]
            value_cell = data.xpath('//*[@id="main"]/div[1]/div/div[1]/p/text()')[0]
            dictionary.update({key_cell: value_cell})
        if key in dictionary:
            return dictionary[key]
        else:
            return False

    except Exception as error:
        print(error)