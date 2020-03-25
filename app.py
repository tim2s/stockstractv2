from flask import Flask, request

from jinja2 import Environment, FileSystemLoader
from analysis.list_index import read_all, read_filtered
from extraction.letter_indexer import LetterIndexer
from datetime import date, datetime

app = Flask(__name__)


@app.route('/refresh/')
def refresh():
  company_candidates = read_all()
  read_count = 0
  for candidate in company_candidates:
    last_update = datetime.strptime(candidate.company_record['head']['timestamp'], "%Y-%m-%d %H:%M:%S")
    if (datetime.today() - last_update).days > 1:

      reference = {
        'url': candidate.url(),
        'isin': candidate.isin,
        'sector': candidate.sector
      }
      try:
        LetterIndexer().process_reference(reference)
        read_count += 1
      except Exception as ex:
        print(ex)
    else:
      print("skipping {0} because it was already updated on {1}".format(candidate.isin, last_update))
  return "Renewed " + str(read_count) + " / " + str(len(company_candidates))


@app.route('/refresh-single/')
def refresh_single():
    reference = {
      'url': 'https://kurse.boerse.ard.de/ard/kurse_einzelkurs_profil.htn?i='+request.args.get('i'),
      'sector': request.args.get('sector')
    }
    LetterIndexer().process_reference(reference)
    return "Done." + str(reference)


@app.route('/extract/all')
def extract_all():
  skip = request.args.get('skip')
  letterIndexer = LetterIndexer(skip)
  references = letterIndexer.extract_references()
  return str(references)


@app.route('/results/')
def view_all():
  sort = request.args.get('sort')
  filter_pe_min = request.args.get('pe_min')
  filter_pe_max = request.args.get('pe_max')
  filter_pb_max = request.args.get('pb_max')
  filter_pb_min = request.args.get('pb_min')
  filter_gnp_max = request.args.get('gnp_max')
  filter_gnp_min = request.args.get('gnp_min')
  filter_dy_max = request.args.get('dy_max')
  filter_dy_min = request.args.get('dy_min')
  filter_sector = request.args.get('sector')
  filter = {
    'pe_min': filter_pe_min,
    'pe_max': filter_pe_max,
    'pb_min': filter_pb_min,
    'pb_max': filter_pb_max,
    'dy_min': filter_dy_min,
    'dy_max': filter_dy_max,
    'gnp_min': filter_gnp_min,
    'gnp_max': filter_gnp_max,
    'sector': filter_sector
  }
  company_candidates = read_filtered(sort, filter)
  j2_env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
  template = j2_env.get_template('resultlist.html')
  return template.render(company_candidates=company_candidates)


if __name__ == '__main__':
  app.run()
