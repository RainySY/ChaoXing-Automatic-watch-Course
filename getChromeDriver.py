from requests import get
from lxml.etree import HTML
from zipfile import ZipFile


def get_a_link(ChromeVersion, a_list):
    i = 0
    for a in a_list:
        if ChromeVersion < int(a.text.split('.')[0]):
            return i - 1
        i += 1
    return i - 1


def getChromeDriver():
    url = 'https://npm.taobao.org/mirrors/chromedriver/'

    ChromeVersion = int(input('请输入 chrome 版本号：').split('.')[0])

    res = get(url)

    html_code = HTML(res.text)
    a_list = html_code.xpath('/html/body/div[1]/pre/a')[1:]
    # print(a_list[0].text)
    a_unnecessary_list = [a for a in a_list if (
        'LATEST_RELEASE' in a.text) or ('index.html' == a.text) or ('icons/' == a.text)]
    a_list = [a for a in a_list if a not in a_unnecessary_list]
    download_link = 'https://npm.taobao.org/mirrors/chromedriver/' + \
        a_list[get_a_link(ChromeVersion, a_list)].text + \
        'chromedriver_win32.zip'

    # print(a_unnecessary_list[0].text)

    print(download_link)

    exe_zip = get(download_link).content
    with open('chromedriver_win32.zip', 'wb') as fp:
        fp.write(exe_zip)

    with ZipFile('chromedriver_win32.zip') as zf:
        zf.extractall()


if __name__ == "__main__":
    getChromeDriver()

