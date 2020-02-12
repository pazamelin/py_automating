import requests
import bs4
import time


def requestCD(word):
    result = []
    time_start = time.time()
    frameURL = 'https://dictionary.cambridge.org/dictionary/english/'
    res = requests.get(frameURL + word)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    dictionary_block = (soup.findAll("div", {"class": "pr dictionary"}))[0]
    header = (dictionary_block.findAll("div", {"class": "pos-header dpos-h"}))[0]
    definitions = dictionary_block.findAll("div", {"class": "def-block ddef_block"})
    idiom_blocks = dictionary_block.findAll("div", {"class": "xref idioms hax dxref-w lmt-25 lmb-25"})
    idiom_blocks += dictionary_block.findAll("div", {"class": "xref idiom hax dxref-w lmt-25 lmb-25"})
    verb_blocks = dictionary_block.findAll("div", {"class": "xref phrasal_verbs hax dxref-w lmt-25 lmb-25"})
    verb_blocks += dictionary_block.findAll("div", {"class": "xref phrasal_verb hax dxref-w lmt-25 lmb-25"})
    headword = (header.findAll("span", {"class": "hw dhw"}))[0]
    pronunciation = (header.findAll("span", {"class": "pron dpron"}))[0]
    result.append(headword.getText() + " " + pronunciation.getText())
    forms = (header.findAll("span", {"class": "irreg-infls dinfls"}))
    if len(forms) > 0:
        result.append(headword.getText() + " | " + forms[0].getText())
    for definition in definitions:
        formulation = (definition.findAll("div", {"class": "def ddef_d db"}))[0]
        result.append("- " + formulation.getText())
        examples = (definition.findAll("span", {"class": "eg deg"}))
        for example in examples:
            result.append("    " + example.getText())
    if len(idiom_blocks) > 0:
        result.append("idioms:")
        for block in idiom_blocks:
            block = (block.findAll("a"))
            for idiom in block:
                result.append(" " + idiom.getText())
    if len(verb_blocks) > 0:
        result.append("phrasal verbs:")
        for block in verb_blocks:
            block = (block.findAll("a"))
            for verb in block:
                result.append(" " + verb.getText())
    print(time.time() - time_start)
    return result


def requestUD(word):
    result = []
    time_start = time.time()
    frameURL = 'https://www.urbandictionary.com/'
    res = requests.get(frameURL + word)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    def_panel = (soup.findAll("div", {"class": "def-panel"}))[0]
    header = (def_panel.findAll("div", {"class": "def-header"}))[0]
    header = header.findAll("a")[0]
    meaning = def_panel.findAll("div", {"class": "meaning"})[0]
    example = def_panel.findAll("div", {"class": "example"})[0]
    result.append(header.getText())
    result.append("- " + meaning.getText())
    result.append("    " + example.getText())
    print(time.time() - time_start)
    return result


def inputList(fileName):
    result = []
    file = open(fileName, 'r')
    for line in file:
        result.append(line)
    file.close()
    return result


time_start = time.time()
wordlist = inputList("wordlist.txt")
file_out = open('out.txt', 'w')
for word in wordlist:
    word = word[:-1]
    print(word)
    file_out.write('\n'.join(requestCD(word)))
    file_out.write('\n')
    file_out.write('\n')

print(time.time() - time_start)
