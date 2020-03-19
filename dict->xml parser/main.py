import files
import time
import scrape

time_start = time.time()
files.sortAlphabet("19mar.txt")
files.handleList("19mar.txt", "")
print(time.time() - time_start)
"""
res = scrape.requestTranslation("profound")
if res is not None:
    print(res)
"""
