import jinja2
from flask import Flask, request

from jinja2 import Template, Environment, FileSystemLoader
from analysis.list_index import read_all
from extraction.extract_all import run_all

app = Flask(__name__)


@app.route('/extract/all')
def extract_all():
  return str(run_all())


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
  filter = {
    'pe_min': filter_pe_min,
    'pe_max': filter_pe_max,
    'pb_min': filter_pb_min,
    'pb_max': filter_pb_max,
    'dy_min': filter_dy_min,
    'dy_max': filter_dy_max,
    'gnp_min': filter_gnp_min,
    'gnp_max': filter_gnp_max
  }
  company_candidates = read_all(sort, filter)
  j2_env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
  template = j2_env.get_template('resultlist.html')
  return template.render(company_candidates=company_candidates)


if __name__ == '__main__':
  app.run()
