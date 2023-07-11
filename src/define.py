import json
import os
import re
import sys
import webbrowser
import click

import requests
from colorama import Fore, Style

from src import config_util

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# Removes all tags that would only be rendered in html
def clean_html(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    clean_text = re.sub(cleanr, '', raw_html)
    return clean_text


# prints the result, limited to about 75 characters and only the first paragraph
def pretty_print(input):
    maxWidth = 75
    currentPos = 0
    for letter in input:
        currentPos += 1
        if letter == "\n":
            break  # this is the end of the ->short<- description
        if currentPos >= maxWidth and letter == " ":
            letter = "\n"
            currentPos = 0
        print(letter, end='')
    print()


# Loads the search results for the term as json
def get_request(api_url, custom_headers):
    try:
        response = requests.get(api_url, headers=custom_headers)
    except:
        print(
            "There was a problem getting some information. The internet connection may be interrupted or a specified language code is invalid.")
        exit(-1)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def construct_search(lang, id=""):
    searchterm = " ".join(sys.argv)
    searchterm = searchterm[1:len(searchterm)]
    api_url_base_search = "https://" + lang + ".wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=intitle:" + searchterm
    api_url_base_retrieve = "https://" + lang + ".wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&pageids=" + str(
        id)
    headers = {'Content-Type': 'application/json'}
    return [api_url_base_search, api_url_base_retrieve, headers]


# checks if provided arguments are valid
def setup():
    if len(sys.argv) < 2:
        print("Please provide a search term.")
        exit(-1)
    sys.argv[0] = ""

    if sys.argv[1] == "-setlang":
        if len(sys.argv) != 3:
            print("please provide a language code")
            exit(-1)
        else:
            userhome = os.getenv("HOME")
            stdlangf = open(userhome + "/wikipedia-define-cli/stdlang", "w")
            stdlangf.write(sys.argv[2])
            print("New language was set.")
            exit()


# todo: this needs to be cleaned up
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('term', nargs=-1)
@click.option('--language', '-l', default=config_util.get_default_lang(), help='Language of the definition.')
def cli(term, language):
    setup()
    search = construct_search(language)
    result = get_request(search[0], search[2])
    if result:
        num_rows = result["query"]["searchinfo"]["totalhits"]
        if num_rows < 1:
            if language == "en":
                print("No results match your query.")
                exit(-1)
            else:  # the default language is not english, perhaps we can find an english article instad
                search = construct_search("en")
                result = get_request(search[0], search[2])
                if result and result["query"]["searchinfo"]["totalhits"] != 0:
                    language = "en"
                    print(
                        Fore.RED + "There was no article in your preferred language, but this one in english might help:" + Style.RESET_ALL)
                else:
                    print("No results match your query.")
                    exit(-1)

        page_id = result["query"]["search"][0]["pageid"]
        search = construct_search(language, page_id)
        article_result = get_request(search[1], search[2])
        title = clean_html(result["query"]["search"][0]["title"])

        print(Fore.BLUE + title + ":" + Style.RESET_ALL)
        pretty_print(clean_html(article_result["query"]["pages"][str(page_id)]["extract"]))

        if input(Fore.BLUE + "(o): open \n" + Style.RESET_ALL) == "o":
            webbrowser.open("https://" + language + ".wikipedia.org/wiki/" + title.replace(" ", "_"))
        exit()
    print("Something went wrong")
    exit(-1)


if __name__ == '__main__':
    cli()
