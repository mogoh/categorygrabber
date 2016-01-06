Categorygrabber is a small Python 3 script to grab all pages of a category of a 
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