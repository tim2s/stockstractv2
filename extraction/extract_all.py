import json
import os
import urllib

from extraction.extractor import Extractor
from extraction.indexer import Indexer
from extraction.url_builder import company_details_url

index_pages = [
#sdax
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159191",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=159191&sektion=portrait&sortierung=descriptionShort&offset=50",
#mdax
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159090",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=159090&sektion=portrait&sortierung=descriptionShort&offset=50",
#dax
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159096",
#eurostoxx
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159194",
#stoxx europe
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159196",
#dow jones
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=849973",
# s & p 500
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=849976",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=50",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=100",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=150",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=200",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=250",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=300",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=350",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=400",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=450",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=500",

#nasdaq
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=149002",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=149002&sektion=portrait&sortierung=descriptionShort&offset=50",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=149002&sektion=portrait&sortierung=descriptionShort&offset=100"

#Nikkei
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=148429",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=50",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=100",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=150",
  "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=200"
]

def run_single(notion):

  url = company_details_url(notion)
  with urllib.request.urlopen(url) as html_file:
    extractor = Extractor(html_file.read(), url)
    stock_main_data = extractor.content()

  with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
    json.dump(stock_main_data, json_file)


def run_index_page(index_page):

  notions = []

  success_count = 0

  with urllib.request.urlopen(index_page) as html_file:
    indexer = Indexer(html_file)
    notions = indexer.get_links()

  for notion in notions:

    url = company_details_url(notion)
    with urllib.request.urlopen(url) as html_file:

      extractor = Extractor(html_file.read(), url)
      stock_main_data = extractor.content()

      if stock_main_data is not None:

        with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
           json.dump(stock_main_data, json_file)
        success_count += 1
  return success_count

def run_all():
  success_count = 0
  if not os.path.exists('data'):
    os.mkdir('data')
  for index_page in index_pages:
    success_count += run_index_page(index_page)
  return success_count
