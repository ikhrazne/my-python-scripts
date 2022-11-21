import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

__author__ = 'Gruppe 1'
__doc__ = 'extract news header from reuters using selenium'


def register_driver():
    my_driver = webdriver.Chrome(r'C:\driver\chromedriver')
    my_driver.implicitly_wait(20)
    my_driver.maximize_window()

    return my_driver


def extract_data():
    data = {}

    start_url = 'https://www.reuters.com/site-search/?query={}'.format(searched_word)

    pages_number = 0

    while pages_number <= 2848:

        url = "https://www.reuters.com/site-search/?query=tesla&offset={}".format(pages_number)

        driver = register_driver()
        try:
            driver.get(url)
            print(url)
            file.write(url + '\n')
        except Exception:
            print('no page exist anymore', Exception)

        counter = 1
        while counter <= 20:

            header_selector = "/html[1]/body[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/ul[1]/li[{}]".format(
                str(counter))
            try:
                news_header_info_list = driver.find_element(By.XPATH, header_selector).text
                ## split the header
                news_header_info_list = news_header_info_list.split('\n')

                data['category'] = news_header_info_list[0]
                data['title'] = news_header_info_list[1]
                data['date'] = news_header_info_list[-1]

                log_file.write(','.join(news_header_info_list) + '\n')
            except Exception:
                pass

            counter += 1

        driver.close()
        pages_number += 20

    return data


def prepross_data():

    df = pd.DataFrame(extract_data())

    df.to_csv('scraped_data.csv', sep=',')

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="link shorter")

    parser.add_argument("-w", "--word", dest="searched_word", help="the word you are looking for", default="", type=str)

    args = parser.parse_args()

    searched_word = args.searched_word

    file = open('save.txt', "a", encoding='utf-8')
    log_file = open('text.txt', 'a', encoding='utf-8')

    prepross_data()

    file.close()
    log_file.close()
