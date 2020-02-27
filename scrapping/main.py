import files
from scrape import requestCD, requestUD, requestCD_subItem

res = requestCD("burst")
files.dumpWord("test.xml", res)
