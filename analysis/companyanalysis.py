from functools import reduce

from math import sqrt


class CompanyAnalysis:

  def __init__(self, company_record):
    self.company_record = company_record
    self.isin = company_record['head']['isin']
    self.name = company_record['head']['title']
    if 'sector' in company_record['head'].keys():
      self.sector = company_record['head']['sector']
    else:
      self.sector = '--'
    self.price = float(company_record['head']['current_price']['value'])

  def url(self):
    return self.company_record['head']['url']

  def eps_values(self):
    return list(map(lambda eps: eps['value'], self.eps_details()))

  def eps_details(self):
    return self.company_record['kpi']['earningsPerShare']

  def average_eps(self):
    return reduce((lambda x, y: x + y), self.eps_values()) / len(self.eps_values())

  def pe(self):
    eps = self.average_eps()
    if eps == 0:
      return 999
    else:
      return self.price / self.average_eps()

  def dividend_details(self):
    return self.company_record['kpi']['dividendPerShare']

  def dividend_values(self):
    return list(map(lambda eps: eps['value'], self.dividend_details()))

  def average_dividend(self):
    return reduce((lambda x, y: x + y), self.dividend_values()) / len(self.dividend_values())

  def dividend_yield(self):
    return self.average_dividend() / self.price

  def price_to_book(self):
    return self.current_book() / self.price

  def current_book(self):
    return self.book_values()[0]

  def book_values(self):
    return list(map(lambda book: book['value'], self.book_details()))

  def book_details(self):
    return self.company_record['kpi']['bookValuePerShare']

  def graham_number(self):
    if self.average_eps() * self.current_book() > 0:
      return sqrt(self.average_eps() * self.current_book() * 22.5)
    else:
      return 0

  def gn_to_price(self):
    gn = self.graham_number()
    if gn == 0:
      return 999
    else:
      return self.price / self.graham_number()

  def is_valid(self):
    return self.price > 0 \
           and 'dividendPerShare' in self.company_record['kpi'].keys() \
           and 'earningsPerShare' in self.company_record['kpi'].keys() \
           and 'bookValuePerShare' in self.company_record['kpi'].keys()

  def dividend_growth(self):
    end = self.dividend_values()[:2]
    start = self.dividend_values()[-2:]
    start_avg = reduce((lambda x, y: x + y), start) / len(start)
    end_avg = reduce((lambda x, y: x + y), end) / len(end)
    if start_avg != 0:
      return (end_avg - start_avg) / start_avg
    else:
      return 0

  def __repr__(self):
    return f'{self.isin}:{self.name:<30} PRICE:{self.price:.2f} | GN:{self.graham_number():.1f}({self.gn_to_price():.1%}) | PE:{self.pe():.1f} | PB:{self.price_to_book():.1f} | DY:{self.dividend_yield():.2%} | URL:{self.url()}'
