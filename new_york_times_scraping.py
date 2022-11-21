import argparse
import time

import pandas
import requests
import pandas as pd
import logging

__doc__ = 'get the article from the archive of the new york times'

##tesla_related_keywords = ['Musk, Elon', 'Tesla Motors Inc', 'Electric and Hybrid Vehicles']


def extract_data_from_api(year, month):
    base_url = 'https://api.nytimes.com/svc/archive/v1/' + str(year) + '/' + str(month) + '.json?api-key={}'
    requested_url = base_url.format(api_key)
    print(requested_url)
    time.sleep(10)
    print(time.ctime())
    response = requests.get(url=requested_url)
    print(response)

    if str(response.status_code)[0] == '2':
        logging.info('the request passed successfully : ' + base_url)
        return response.json()
    else:
        print('something went wrong')
        try:
            extract_data_from_api(year, month)
        except RecursionError:
            print("can not connect to server !")


def process_data(year, month) -> pandas.DataFrame:
    result = {"news": [], "date": []}
    data = extract_data_from_api(year, month)

    all_articles = data["response"]["docs"]
    len(all_articles)

    for doc in all_articles:
        title = doc["abstract"]
        keywords = doc["keywords"]
        date = doc["pub_date"]

        for keyword in keywords:
            if keyword["value"].title() in {keywords}:
                result["news"].append(title)
                result['date'].append(date)

    return pd.DataFrame(result)


def save_data_into_csv(data_as_dataframe, output_file='data.csv'):
    data_as_dataframe.to_csv(output_file, sep=',')


if __name__ == '__main__':
    final_data = None

    parser = argparse.ArgumentParser(description="link shorter")

    parser.add_argument("-k", "--keywords", dest="searched_keywords", help="give the keywords in comma separat string", default="", type=str)
    parser.add_argument("--key", dest="apikey", help="give your api key",
                        default="", type=str)
    parser.add_argument("--start_year", dest="start_year", help="year to start with",
                        default="", type=str)
    parser.add_argument("--stop_year", dest="stop_year", help="the year to stop",
                        default="", type=str)

    parser.add_argument("--output", dest="output", help="optional parameter the data will save in data.csv by default",
                        default="", type=str)
    args = parser.parse_args()

    keywords = args.searched_keywords.split(',')
    api_key = args.apikey
    start_year = args.start_year
    stop_year = args.stop_year
    output = args.output

    try :
        int(start_year)
        int(stop_year)
    except Exception:
        print("the year should not have a character ")
        exit()

    year_counter = int(start_year)

    while year_counter <= int(stop_year):
        month_counter = 1

        while month_counter <= 12:
            if year_counter == int(stop_year) and month_counter == 12:
                break

            data = process_data(year_counter, month_counter)

            if final_data is None:
                final_data = data
            else:
                final_data.append(data)

            month_counter += 1

        year_counter += 1

    if len(output) != 0:
        try:
            save_data_into_csv(final_data, output_file=output)
        except Exception:
            print("the file does not exist !")
    else:
        save_data_into_csv(final_data)

