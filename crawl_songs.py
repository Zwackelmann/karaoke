import requests
from HTMLParser import HTMLParser
from lxml import html
from lxml import etree
import requests
import re
import string
import time
import io

def process_string(s):
  encoded = unicode(s)
  substituted = re.sub('\s+', ' ', encoded).replace(
                       u"\u00B4", '\'').replace(
                       u"\u0060", '\'').replace(
                       u"\u0092", '\'').replace(
                       u"\u012B", 'i').replace(
                       u"\u0148", 'n').replace(
                       u"\u0112", "E").replace(
                       u"\u00C2", "A").replace(
                       ";", "")
  
  return string.capwords(substituted.strip())

urls = [
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_a.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_b.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_c.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_d.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_e.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_f.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_g.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_h.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_i.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_j.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_k.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_l.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_m.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_n.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_o.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_p.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_q.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_r.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_s.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_t.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_u.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_v.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_w.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_x.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_y.html',
  'http://www.wildgeese.de/KaraokeBs/KaraokeBr_z.html'
]

f = io.open("songs.csv", "w", encoding="utf-8")
for url in urls:
  print "crawl " + url
  page = requests.get(url)
  tree = html.fromstring(page.content)
  
  elems = tree.xpath('//table//table//table//table/tr[td/font]')
  
  pairs = []
  for elem in elems:
    interpret_tds = elem.xpath('td[1]')
    title_tds = elem.xpath('td[2]')
    
    if len(interpret_tds) == 1 and len(title_tds) == 1:
      interpret_td = interpret_tds[0]
      title_td = title_tds[0]
      
      interpret = process_string(" ".join(interpret_td.xpath('.//text()')))
      
      title = process_string(" ".join(title_td.xpath('.//text()')))
      pairs.append([interpret, title])
    else:
      print "more than one interpet tds or title tds"
      print etree.tostring(elem, pretty_print=True)
  
  for pair in pairs:
    f.write(pair[0] + ";" + pair[1] + "\n")
    
  time.sleep(2)
  f.flush()
f.close()