import json
import os

from analysis.companyanalysis import CompanyAnalysis


def gn_to_price(company_candidates):
  return sorted(company_candidates, key=lambda company: company.gn_to_price())


def dividend_yield(company_candidates):
  return sorted(company_candidates, key=lambda company: company.dividend_yield(), reverse=True)


def price_to_earnings(company_candidates):
  return sorted(company_candidates, key=lambda company: company.pe())


def price_to_book(company_candidates):
  return sorted(company_candidates, key=lambda company: company.price_to_book())


def filter_pe(company_candidates, minimum, maximum):
  minimum, maximum = min_max_params(minimum, maximum)
  return list(filter(lambda company: minimum < company.pe() < maximum, company_candidates))


def filter_pb(company_candidates, minimum, maximum):
  minimum, maximum = min_max_params(minimum, maximum)
  return list(filter(lambda company: minimum < company.price_to_book() < maximum, company_candidates))


def filter_dy(company_candidates, minimum, maximum):
  minimum, maximum = min_max_params(minimum, maximum)
  return list(filter(lambda company: minimum < company.dividend_yield() < maximum, company_candidates))


def min_max_params(minimum, maximum):
  if minimum is None:
    minimum = -9999
  if maximum is None:
    maximum = 9999
  return float(minimum), float(maximum)


sort_methods = {
  'dividend-yield': dividend_yield,
  'price-to-book': price_to_book,
  'price-to-earnings': price_to_earnings,
  'graham_to_price': gn_to_price
}

def read_all(sort, value_filters):
  company_candidates = []
  for company_json_file in os.listdir('data'):
    with open('data/' + company_json_file, 'r') as file:
      company_record = json.load(file)
      company_analysis = CompanyAnalysis(company_record)
      company_candidates.append(company_analysis)
  company_candidates = list(filter(lambda company: company.is_valid(), company_candidates))
  company_candidates = filter_pe(company_candidates, value_filters['pe_min'], value_filters['pe_max'])
  company_candidates = filter_pb(company_candidates, value_filters['pb_min'], value_filters['pb_max'])
  company_candidates = filter_dy(company_candidates, value_filters['dy_min'], value_filters['dy_max'])
  if sort is not None and sort in sort_methods.keys():
    company_candidates = sort_methods.get(sort)(company_candidates)
  return company_candidates
