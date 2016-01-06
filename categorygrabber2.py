#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
A simple Python 3 script to grab all pages of a wikipedia category of the
german Wikipedia.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from copy import deepcopy
import getopt
import sys

def grab(members, category, baseurl, request, recursive):
    print("========================================================")
    print(category)
    print(baseurl)
    print(request)
    print("========================================================")

    if recursive:
        request["cmtype"] = "subcat"
        requestparsed = urllib.parse.urlencode(request)
        url = baseurl+"?"+requestparsed
        xmlstring = urllib.request.urlopen(url).read()
        api = ET.fromstring(xmlstring)
        query = api.find("query")
        categorymembers = query.find("categorymembers")
        cm = list(categorymembers)
        if cm != []:
            for member in cm:
                membertitle = member.attrib["title"]
                category2 = membertitle
                request2 = deepcopy(request)
                request2["cmtitle"] = category2
                grab([], category2, baseurl, request2, recursive)

    #print(request["cmtitle"])
    request["cmtype"] = "page"
    requestparsed = urllib.parse.urlencode(request)
    url = baseurl+"?"+requestparsed
    xmlstring = urllib.request.urlopen(url).read()
    api = ET.fromstring(xmlstring)
    query = api.find("query")
    categorymembers = query.find("categorymembers")
    cm = list(categorymembers)

    for member in cm:
        membertitle = member.attrib["title"]
        membertitle = re.sub(r" \(.+\)$", r"", membertitle)
        members.append(membertitle)
    
    continuecat = api.find("continue")
    if continuecat != None:
        cmcontinue = continuecat.attrib["cmcontinue"]
        request["cmcontinue"] = cmcontinue
        grab(members, category, baseurl, request, recursive)
    
    members = "\n".join(members)
    #print(members)
    filename = re.sub(r"\/", r"_", category)
    with open(filename+".txt", "w") as text_file:
        print(members, file=text_file)

def usage():
    helpstring = """Categorygrabber is a small Python 3 script to grab all pages of a category of a 
mediawiki like Wikipedia. The output will be stored in a file named after the 
category. The pagenames will be beautifyed like trailing braces will be removed. 
Usage:
-h --help               Print this help-string and exit.
-w --wiki=WIKI          Select the wiki wich will be searched. For example:
                        "--wiki https://de.wikipedia.org" The http(s) is 
                        necessary, a trailing slash ("/") is not allowed.
                        Default: "https://de.wikipedia.org"
-c --category=CAT       Select the category which will be searched. For example:
                        "Kategorie:US-amerikanisches_Musiklabel". The leading
                        "Kategorie:" is necessary.
-r --recursive          If the recursuve-flag is given, the search will be
                        recursive through all sub-categorys.
Example:
categorygrabber -w https://en.wikipedia.org -c Category:Offspring_of_Gaia -r
"""
    print(helpstring)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:c:hr", ["wiki=", "help", "category", "recusive"])
    except getopt.GetoptError as err:
        print(err)
        #usage()
        sys.exit(2)
    wiki = "https://de.wikipedia.org"
    category = ""
    recursive = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-w", "--wiki"):
            wiki = a
        elif o in ("-c", "--category"):
            category = a
        elif o in ("-r", "--recursive"):
            recursive = True
        else:
            assert False, "unhandled option"
    baseurl = wiki+"/w/api.php"
    request = {
    "action" : "query",
    "list" : "categorymembers",
    "format" : "xml",
    "cmtitle" : category,
    "cmlimit" : "500"}
    grab([], category, baseurl, request, recursive)

if __name__ == "__main__":
    main()
