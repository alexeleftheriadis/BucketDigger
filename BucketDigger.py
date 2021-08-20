"""""""""""""""""""""""""""""""""""""""

@author:        Eleftheriadis Alexanros
@license:       The MIT License (MIT)
@contact:       aelevthe@protonmail.com
                github.com/alexeleftheriadis

"""""""""""""""""""""""""""""""""""""""

import wget
import xml.etree.ElementTree as ET
import os
import urllib.request
from requests.utils import requote_uri
import shutil
import argparse
import PyPDF2
import re
import time

start_time = time.time()

##################################################################################################
#    Supported so far .txt, .pdf, .json, .js .css .md
##################################################################################################

xml_list = []
final_res = {}
allfound = {'txt': [], 'js': [], 'pdf': [], 'json': [], 'css': [], 'md': [], 'csv': [], 'jpg': []}


#Getting information about how many file per extension exists.
def file_classification(urllist):
    for _ in range(len(urllist)):
        clist = ['.txt', '.csv', '.jpg', '.pdf', '.js', '.json', '.css', '.md']
        for tagdot in clist:
            tag = tagdot.replace('.', '')
            if tagdot in urllist[_]:
                allfound[tag].append(urllist[_])


def size(file):
    site = urllib.request.urlopen(file)
    return site.length


class Type:
    def __init__(self, tag, found, maxsize, keyword, url):
        if len(tag) > 0:
            for _ in range(0, len(found)):
                url_check = url + found[_]
                url_check = requote_uri(url_check)
                url_size = size(url_check)
                newname = str(found[_]).replace("/", ".")
                if url_size < maxsize or maxsize is None:
                    urllib.request.urlretrieve(url_check, newname)
                    if tag == 'pdf':
                        pdf_parse(newname, keyword, tag, url_check)
                    else:
                        text_type_parse(newname, keyword, tag, url_check)
                else:
                    print('The file size exceeds the limit has been set')
        else:
            print(f'No {tag} files found')


def pdf_parse(newname, keyword, tag, url):
    cr_object = PyPDF2.PdfFileReader(newname)
    numpages = cr_object.getNumPages()
    deleteflag = True
    for i in range(0, numpages):
        pageobj = cr_object.getPage(i)
        text = pageobj.extractText()
        for key in keyword:
            ressearch = re.findall(key, text)
            if len(ressearch) > 0:
                deleteflag = False
                print(f'{len(ressearch)} strings containing "{key}" found in page {i + 1} at {url}')
                final_res[str(key)][str(tag)] += 1
    if deleteflag is True:
        remove(newname)
    else:
        save_found_file(newname)


def text_type_parse(newname, keyword, tag, url):
    textfile = open(newname, 'r', encoding="utf8")
    filetext = textfile.read()
    textfile.close()
    deleteflag = True
    for key in keyword:
        ressearch = re.findall(key, filetext)
        if ressearch:
            print(f'{len(ressearch)} strings containing "{key}" found at {url}.')
            deleteflag = False
            final_res[str(key)][str(tag)] += 1
    if deleteflag is True:
        remove(newname)
    else:
        save_found_file(newname)


## Saving the file containing a keyword.
def save_found_file(newname):
    try:
        shutil.move(newname, f"saved/{ newname}")
    except:
        print('cannot save file, maybe already exists')


#Checking the extension(s) selected on input method.
def call_type(args, keyword):
    supported = ['txt', 'js', 'json', 'css', 'md', 'pdf']
    if args.typeofsearch == 'all':
        for tag in supported:
            Type(tag, allfound[tag], args.maxsize, keyword, args.url)
    elif args.typeofsearch in supported:
        Type(args.typeofsearch, allfound[args.typeofsearch], args.maxsize, keyword, args.url)
    else:
        print("Wrong input of -t, please select on of the supported types or 'all'")


def makedir(name):
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    try:
        os.mkdir(name)
    except OSError:
        print("Creation of the directory %s failed, already exists?" % path)
    else:
        print("Successfully created the directory %s " % path)


def downloadxml(args):
    wget.download(args.url, 'xmldownload.xml')
    tree = ET.parse('xmldownload.xml')
    root = tree.getroot()
    urllist = []
    for elem in root:
        for subelem in elem:
            findxmltag = subelem.tag.split('}')
            if findxmltag[1] == 'Key':
                urllist.append(subelem.text)
    return urllist


def remove(file):
    os.remove(file)


def results_update(tag):
    s_all = {'txt': 0, 'js': 0, 'pdf': 0, 'json': 0, 'css': 0, 'md': 0}
    final_res.update({tag: s_all})


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--typeofsearch", type=str, help="Type of the file to search",  default="txt")
    parser.add_argument("-ms", "--maxsize", type=int, help="The max size of files", default=500000000)
    parser.add_argument('-url', "--url", type=str, help="The url of the bucket")
    parser.add_argument('-kw', "--keywordfile", type=str, help="The file containing the word(s) to search to")
    args = parser.parse_args()

    if args.url.endswith('/') is False:
        args.url = args.url + '/'
    return args


def main():
    args = arguments()
    urllist = downloadxml(args)
    makedir('saved')
    file_classification(urllist)
    wordfile = open(args.keywordfile, 'r')
    keyword_count = 0
    keyword_list = []
    while True: #Loopes through every keyword given.
        keyword_count += 1
        line = wordfile.readline()
        if not line:
            break
        keyword_list.append(line.strip())
        results_update(str(line.strip()))

    call_type(args, keyword_list)
    wordfile.close()
    xml_delete = 'xmldownload.xml'
    remove(xml_delete)

    print(f'Searching for {keyword_list}')
    print(f'End of searching with results: {final_res}.')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
