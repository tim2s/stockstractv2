import json
import string
import urllib

from bs4 import BeautifulSoup

from analysis.list_index import exists
from extraction.extractor import Extractor


class LetterIndexer:

  def __init__(self, skip_existing='False'):
    self.links = self.generate_all_links()
    self.references = []
    self.skip_existing = skip_existing in ['true', 'True', 'yes'] or False
    print("Starting off with skip existing set to ", skip_existing)

  def generate_all_links(self):
    links = []
    letters = list(string.ascii_uppercase)
    max_count = range(5)
    for letter in letters:
      for count in max_count:
        links.append(self.build_url(letter, count))
    return links

  def extract_references(self):
    for url in self.links:
      print('NOW READING FROM PAGE: ' + url)
      self.extract_from_url(url)
    return self.references

  def build_url(self, letter, page):
    return f'https://kurse.boerse.ard.de/ard/aktien_profile.htn?suche=1&letter={letter}&offset={page * 25}'


  def extract_from_url(self, url):
    with urllib.request.urlopen(url) as html_file:
      if html_file is not None:
        soup = BeautifulSoup(html_file, 'html.parser')
        table = soup.tbody
        if table is not None:
          rows = table("tr")
          for row in rows:
            self.extract_company_from_row(row)
          else:
            print('Table Empty on page, Skipping it: ' + url)
      else:
        print("this page was empty - ", url)

  def extract_company_from_row(self, row):
    cols = row("td")
    ref_url = cols[0].strong.contents[0].attrs['href']
    isin = cols[1].string
    sector = cols[2].string
    reference = {
      'url': ref_url,
      'isin': isin,
      'sector': sector
    }
    if (not self.skip_existing) or (not exists(isin)):
      self.process_reference(reference)
      self.references.append(reference)
    else:
      print('Skip = true so wont update existing value:', isin)

  def process_reference(self, reference):
    with urllib.request.urlopen(reference['url']) as html_file:
      extractor = Extractor(html_file.read(), reference['url'])
      stock_main_data = extractor.content()

      if stock_main_data is not None:
        stock_main_data['head'].update({'sector': reference['sector']})
        with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
          json.dump(stock_main_data, json_file)
        reference.update({'status': 'success'})
      else:
        reference.update({'status': 'failed'})
