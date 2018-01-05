#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 05/01/2018 2:12 PM
# @Project : main
# @Author  : Li Yao
# @File    : ena.py
from __future__ import print_function
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
import json
import os
import getopt
import sys


def get_download_link(acc, field="fastq_ftp"):
    """
    Get download link from EBI ENA
    :param acc: str
    :param field: str
    :return:
    """
    links = list()
    if acc[2] == "A":
        keyword = "submission_accession"
    elif acc[2] == "S":
        keyword = "sample_accession"
    elif acc[2] == "P":
        keyword = "study_accession"
    elif acc[2] == "X":
        keyword = "experiment_accession"
    elif acc[2] == "R":
        keyword = "run_accession"
    else:
        print("Unsupported accession type %s" % acc)
        return []
    api_bus = 'https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query="%s=%s"&fields=%s&format=json' % (keyword, acc, field)
    res_data = urlopen(api_bus)
    ret = res_data.read()
    if ret:
        res = json.loads(ret)
        for run in res:
            print("Run accession: %s" % run["run_accession"])
            print(run[field])
            links.extend(run[field].split(";"))
            return links
    else:
        return []


def get_accession(query):
    """
    Get accession ID from EBI Search
    :param query:
    :return:
    """
    api_bus = "http://www.ebi.ac.uk/ebisearch/ws/rest/nucleotideSequences?query=%s&fieldurl=true&viewurl=true&format=json" % query
    sra_list = list()
    try:
        res_data = urlopen(api_bus)
        res = json.loads(res_data.read())
        if res["hitCount"] == 0:
            return 0
        for entry in res["entries"]:
            sra_list.append(entry["id"])
        return sra_list
    except Exception as e:
        print(e)
        return 0


def downloader(url):
    """
    Download a file
    :param url: str
    :return:
    """
    os.system("wget %s" % url)


def download_fastq_from_ebi(query):
    """
    Wrapper and interface
    :param query: str
    :return:
    """
    all_links = list()
    fl = get_accession(query)
    for r in fl:
        all_links.extend(get_download_link(r))
    for file in all_links:
        downloader(file)


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "q:", ["query="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit()

    if len(opts) == 0:
        sys.exit()