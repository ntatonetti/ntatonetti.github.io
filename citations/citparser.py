import os
import sys
import csv
import codecs

from collections import defaultdict

# Download citations from google scholar a speadsheet (citations.csv)
# Download the citations using semantic scholar using Publish or Perish (citations_ss.csv)

fh = open('citations/citations_ss.csv', 'r')
reader = csv.reader(codecs.EncodedFile(fh, 'utf-8', 'utf-8-sig'))
header = next(reader)

title2author = dict()
for row in reader:
    citation = dict(zip(header, row))
    titlekey = citation['Title'].strip().strip('.').lower()
    title2author[titlekey] = citation['Authors']
fh.close()

fh = open('citations/citations.csv', 'r')
reader = csv.reader(codecs.EncodedFile(fh, 'utf-8', 'utf-8-sig'))

header = next(reader)

citations = defaultdict(list)
num_citations = 0
last_author_count = 0
first_author_count = 0

for order, row in enumerate(reader):
    num_citations += 1
    citation = dict(zip(header, row))
    #print(citation)

    titlekey = citation['Title'].strip().strip('.').lower()
    if not titlekey in title2author:
        raw_author_list = citation['Authors'].strip().strip(';').split(';')
    else:
        raw_author_list = title2author[titlekey].strip().split(',')

    author_list = list()
    for author in raw_author_list:
        if author.find('Tatonetti') != -1:
            author_list.append('<b>%s</b>' % author)
        else:
            author_list.append(author)

    cite_string = '\n'
    if author_list[0].find('Tatonetti') != -1:
        cite_string += '<span class="author_icon">FA</span>\n'
        first_author_count += 1

    if author_list[-1].find('Tatonetti') != -1:
        cite_string += '<span class="author_icon">LA</span>\n'
        last_author_count += 1

    cite_string += '<p class="citation">\n'
    cite_string += '\t<span class="authors">%s</span>\n' % ', '.join(author_list)
    cite_string += '\t<span class="title">%(Title)s</span>\n' % citation
    cite_string += '\t<span class="journal">%(Publication)s, <em>(%(Year)s)</em> </span>' % citation

    if citation['Volume'] != '':
        cite_string += '<span>Vol %s</span> ' % citation['Volume']
    if citation['Number'] != '':
        cite_string += '<span>No %s</span> ' % citation['Number']

    if citation['Pages'] != '':
        cite_string += '<span>Pp %s</span> ' % citation['Pages']

    cite_string += '\n'
    cite_string += '</p>\n'

    citations[citation['Year']].append( cite_string )

years = sorted(citations.keys())
years.reverse()

for year in years:
    print("<p><strong><em>%s</em></strong></p>\n" % year)
    year_cites = citations[year]
    year_cites.reverse()
    print('\n'.join(year_cites))

fh.close()

sys.stderr.write("%d total citations found, %d first author, %d last author" % (num_citations, first_author_count, last_author_count))
