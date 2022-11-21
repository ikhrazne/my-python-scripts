import hashlib
import webbrowser
import argparse

import json

# is the domain of the provider (in this case is a localhost)
base_link = 'https://localhost/'
## chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
fire_fox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'  ### firefox is the browser by default


def generate_short_link(link):
    ## using hashlib to generate the link
    path = hashlib.md5(link.encode())
    return base_link + str(path.hexdigest()[:8])


def save_links(link, short_link):
    file = open('data.json', 'r', encoding='utf-8')
    data = file.read()
    file.close()
    data = json.loads(data)
    data[short_link] = link

    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


def retrieve_link(short_link):
    file = open('data.json', 'r', encoding='utf-8')
    data = file.read()
    file.close()
    data = json.loads(data)

    return data[short_link]


# open the link on the browser
def launch_mozilla(url, browser_path=fire_fox_path):
    try:
        webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))
        webbrowser.get('browser').open(url)
    except Exception:
        print("Please be sure that firefox is installed in this path : {}".format(fire_fox_path))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="link shorter")

    parser.add_argument("-l", "--link", dest="link", help="Give the link", default="", type=str)
    parser.add_argument("-s", "--short", dest="short_link", help="give the short link", default="", type=str)

    args = parser.parse_args()

    link = args.link
    short_link = args.short_link

    if len(link) != 0 and len(short_link) == 0:
        short_link_value = generate_short_link(link)
        save_links(link, short_link_value)
        print(short_link_value)
    elif len(link) == 0 and len(short_link) != 0:
        launch_mozilla(retrieve_link(short_link))
    else:
        print('please give the link or short link as parameter !')
