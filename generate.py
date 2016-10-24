from datetime import datetime
import glob
import json
import os
import sys
import re
from jinja2 import Environment, PackageLoader

if sys.version_info.major < 3:
    exit("This code requires Python 3.\nThis is {}".format(sys.version))

def main():
    conferences = read_files()
    #print(conferences)
    generate_pages(conferences)

def read_files():
    conferences = []

    for filename in glob.glob("data/*.txt"):
        print("Reading {}".format(filename))
        conf = {}
        try:
            this = {}
            nickname = os.path.basename(filename)
            nickname = nickname[0:-4]
            #print(nickname)
            this['nickname'] = nickname
            with open(filename, encoding="utf-8") as fh:
                for line in fh:
                    line = line.rstrip('\n')
                    if re.search(r'\A\s*#', line):
                        continue
                    if re.search(r'\A\s*\Z', line):
                        continue
                    k,v = re.split(r'\s*:\s*', line, maxsplit=1)
                    this[k] = v
            conferences.append(this)
        except Exception as e:
            exit("ERROR: {} in file {}".format(e, filename))
 
    return sorted(conferences, key=lambda x: x['start_date'])

def generate_pages(conferences):
    env = Environment(loader=PackageLoader('conf', 'templates'))
    if not os.path.exists('html/'):
        os.mkdir('html/')

#    event_template = env.get_template('event.html')
#    if not os.path.exists('html/e/'):
#        os.mkdir('html/e/')
#        for event in conferences:
#            try:
#                with open('html/e/' + e['nickname'], 'w', encoding="utf-8") as fh:
#                    fh.write(source_template.render(
#                        event = event,
#                ))
#            except Exception as e:
#                print("ERROR: {}".format(e))
           
    now = datetime.now().strftime('%Y-%m-%d')
    #print(now)
    future = list(filter(lambda x: x['start_date'] >= now, conferences))
    #print(future)
    main_template = env.get_template('index.html')
    with open('html/index.html', 'w', encoding="utf-8") as fh:
        fh.write(main_template.render(
            h1          = 'Tech related conferences',
            title       = 'Tech related conferences',
            conferences = future,
        ))

    with open('html/conferences', 'w', encoding="utf-8") as fh:
        fh.write(main_template.render(
            h1          = 'Tech related conferences',
            title       = 'Tech related conferences',
            conferences = conferences,
        ))

main()

# vim: expandtab
