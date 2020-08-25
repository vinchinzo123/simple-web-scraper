import requests
from html.parser import HTMLParser
import re
import argparse
import urllib.parse

parser = argparse.ArgumentParser(
    description='Prints HTML links, email and phone numbers')
parser.add_argument('weblink', metavar='', type=str,
                    help='Weblink to parse')


def create_phone_num(*args):
    phone_num = ''
    for arg in args:
        if arg:
            phone_num += arg + "-"
    return phone_num.rstrip('-')


def main():
    x_list = []
    url = parser.parse_args().weblink

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            # x_list.append(tag)
            pass

        def handle_endtag(self, tag):
            # x_list.append(tag)
            pass

        def handle_data(self, data):
            x_list.append(data)

    email_pattern = re.compile(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone_pattern = re.compile(
        r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'

        # r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?'
    )

    website_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    parser_html = MyHTMLParser()
    r = requests.get(url)
    email_list = []
    url_list = []
    phone_list = []
    parser_html.feed(r.text.replace('\n', "").replace('\t', "").replace(
        'div', '').replace('link', '').replace('script', ''))
    for x in x_list:
        if re.findall(website_pattern, x):
            url_list.extend(re.findall(website_pattern, x))
        if re.findall(email_pattern, x):
            email_list.extend(re.findall(email_pattern, x))
        if re.findall(phone_pattern, x):
            phone_list.extend(re.findall(phone_pattern, x))

    print(f'\nList of {len(url_list)} URLs in {url}\n')
    for url_item in url_list:
        print(urllib.parse.unquote(url))
    print(f'\nList of {len(email_list)} emails in {url}\n')
    for email in email_list:
        print(email)
    print(f'\nList of {len(phone_list)} phone numbers in {url}\n')
    for phone_num in phone_list:
        print(create_phone_num(*phone_num))


if __name__ == "__main__":
    main()
