#!usr/bin/python
"""
Program to scrape health.pa.gov/topics/disease/coronavirus/Pages/Archives.aspx
for data on daily testing rate in comparison with covid-19 cases
"""

# Not sure why vscode is still flagging lxml.  It is working now...
# steps to fix module not found error:  pip3 install instead of pip install
from lxml import html
import requests

page = requests.get('https://www.health.pa.gov/topics/disease/coronavirus/Pages/Archives.aspx')
tree = html.fromstring(page.content)

def is_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False


# I'm not sure why these paths are picking up two entries like negative_test='Adams', positive_test=(low number)

negative_tests = tree.xpath("//td/strong[text()='Deaths']/following::tr[1]/td[1]")
negative_tests = [int(n.text.replace(",", "")) for n in negative_tests if is_int(n.text.replace(",", ""))]

positive_tests = tree.xpath("//td/strong[text()='Positive']/following::td/strong[text()='Deaths'][1]/following::tr[1]/td[2]")
positive_tests = [int(n.text.replace(",", "")) for n in positive_tests if is_int(n.text.replace(",", ""))]
positive_tests = [n for n in positive_tests if n > 50]

deaths = tree.xpath("//td/strong[text()='Positive']/following::td/strong[text()='Deaths'][1]/following::tr[1]/td[3]")
deaths = [int(n.text) for n in deaths if is_int(n.text)]


for n, p, d in zip(negative_tests, positive_tests, deaths):
  s = 'Negative: {} Positive: {}, Deaths: {}'.format(n, p, d)
  print(s)



