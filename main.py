#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os, sys, csv, re
import requests


CHUNK_SIZE = 4096


def clean_file_name(s):
    s = re.sub('[\W_]', ' ', s)
    s = '_'.join(s.split()).lower()

    return s


def save_to_file(url, fname):
    r = requests.get(url)
    with open(fname, 'wb') as f:
        for chunk in r.iter_content(CHUNK_SIZE):
            f.write(chunk)


def fetch_files(row, dest_dir):

    fname = clean_file_name(row['media'])
    print 'Processing %s,' % fname
    if row['pdf']:
        to_pdf = os.path.join(dest_dir,
                              '{0}.{1}'.format(fname, 'pdf'))
        save_to_file(row['pdf'], to_pdf)

    if row['mp3']:
        to_mp3 = os.path.join(dest_dir,
                              '{0}.{1}'.format(fname, 'mp3'))
        save_to_file(row['mp3'], to_mp3)



if __name__ == '__main__':

    usage = 'python %s /source/file.csv /dest/dir/' % sys.argv[0]

    if len(sys.argv) < 3:
        print usage
        sys.exit(0)

    filename = sys.argv[1]
    dest_dir = sys.argv[2]

    with open(filename, 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            fetch_files(row, dest_dir)

