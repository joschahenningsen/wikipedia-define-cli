import json
import requests
import sys
import re
import webbrowser
import colorama
from colorama import Fore, Style

if(len(sys.argv)<2):
    print("Please provide a search term.")
    exit(-1)
sys.argv[0]=""
lang="en" # default language
if sys.argv[len(sys.argv)-1].startswith("-"):
    lang = sys.argv[len(sys.argv)-1].replace("-", "")
    sys.argv[len(sys.argv)-1] = ""

searchterm = " ".join(sys.argv)
api_url_base_search = "https://"+lang+".wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=intitle:"
api_url_base_retrieve = "https://"+lang+".wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&pageids="
headers = {'Content-Type': 'application/json'}

# Removes all tags that would only be rendered in html
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# prints the result, limited to about 75 characters and only the first paragraph
def pretty_print(input):
    maxWidth = 75
    currentPos = 0
    for letter in input:
        currentPos += 1
        if letter == "\n":
            break # this is the end of the ->short<- description
        if currentPos>=maxWidth and letter == " ":
            letter="\n"
            currentPos=0
        print(letter, end='')
    print()

def get_request(url, query):
    api_url = url + str(query)
    try:
        response = requests.get(api_url, headers=headers)
    except:
        print("There was a problem retrieving some information, perhaps your internet is disconnected or a provided language code is invalid.")
        exit(-1)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

result = get_request(api_url_base_search, searchterm)
if(result):
    numrows = (result["query"]["searchinfo"]["totalhits"])
    if(numrows<1):
        print("no results match your query")
        exit(-1)
    else:
        page_id = result["query"]["search"][0]["pageid"]
        article_result = get_request(api_url_base_retrieve, page_id)
        title = cleanhtml(result["query"]["search"][0]["title"])
        print(Fore.BLUE+title+":")
        print(Style.RESET_ALL)
        pretty_print(cleanhtml(article_result["query"]["pages"][str(page_id)]["extract"]))
        if(input(Fore.BLUE+"(o): open \n"+Style.RESET_ALL)=="o"):
            webbrowser.open("https://"+lang+".wikipedia.org/wiki/"+title.replace(" ", "_"))
        exit()
print("Something went wrong")
exit(-1)
