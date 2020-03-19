import bs4
import time
import requests
import structure


def requestTranslation(word):
    frameURL = 'https://www.babla.ru/английский-русский/'
    res = requests.get(frameURL + word)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    container = soup.findAll("div", {"class": "quick-results container"})[0]
    translations = container.findAll("ul", {"class": "sense-group-results"})

    if len(translations) > 0:
        res = []
        for block in translations:
            items = block.findAll("li")
            for item in items:
                res.append(item.getText())
        return res
    else:
        res = []
        return res


def request_initialForm(item):
    frameURL = 'https://www.dictionary.com/browse/'
    res = requests.get(frameURL + item)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    initialForm = (soup.findAll("h1", {"class": "css-1jzk4d9 e1rg2mtf8"}))[0].getText()
    return initialForm


def requestCD_subItem(item):
    time_start = time.time()
    frameURL = 'https://dictionary.cambridge.org/dictionary/english/'

    item = item.replace(' ', '-')
    item = item.replace('/', '-')
    res = requests.get(frameURL + item)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    dictionary_blocks = (soup.findAll("div", {"class": "pr dictionary"}))
    if len(dictionary_blocks) == 0:
        return 1
    dictionary_block = dictionary_blocks[0]

    title = (dictionary_block.findAll("div", {"class": "di-title"}))[0]
    newSubItem = structure.SubItem(title.getText())

    definitions = dictionary_block.findAll("div", {"class": "def-block ddef_block"})
    if len(definitions) == 0:
        return 3

    for definition in definitions:
        formulation = (definition.findAll("div", {"class": "def ddef_d db"}))[0].getText()
        newDefinition = structure.Definition(formulation)
        examples = (definition.findAll("span", {"class": "eg deg"}))
        for example in examples:
            newDefinition += example.getText()
        newSubItem += newDefinition
    return newSubItem


def requestCD(word):
    time_start = time.time()
    frameURL = 'https://dictionary.cambridge.org/dictionary/english/'
    res = requests.get(frameURL + word)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    dictionary_blocks = (soup.findAll("div", {"class": "pr dictionary"}))
    if len(dictionary_blocks) == 0:
        try_initial = request_initialForm(word)
        res = requests.get(frameURL + try_initial)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        dictionary_blocks = (soup.findAll("div", {"class": "pr dictionary"}))
        if len(dictionary_blocks) == 0:
            return 1
    dictionary_block = dictionary_blocks[0]

    headers = (dictionary_block.findAll("div", {"class": "pos-header dpos-h"}))
    header = None
    wtype = None
    flag = False
    for temp_header in headers:
        temp_wtype = temp_header.findAll("span", {"class": "pos dpos"})
        if len(temp_wtype) > 0:
            header = temp_header
            wtype = temp_wtype[0]
            flag = True
            break
    if not flag:
        return 2
    definitions = dictionary_block.findAll("div", {"class": "def-block ddef_block"})
    if len(definitions) == 0:
        definitions = dictionary_block.findAll("div", {"class": "def ddef_d db"})
        if len(definitions) == 0:
            return 3
    idiom_blocks = dictionary_block.findAll("div", {"class": "xref idioms hax dxref-w lmt-25 lmb-25"})
    idiom_blocks += dictionary_block.findAll("div", {"class": "xref idiom hax dxref-w lmt-25 lmb-25"})
    verb_blocks = dictionary_block.findAll("div", {"class": "xref phrasal_verbs hax dxref-w lmt-25 lmb-25"})
    verb_blocks += dictionary_block.findAll("div", {"class": "xref phrasal_verb hax dxref-w lmt-25 lmb-25"})

    headword = (header.findAll("span", {"class": "hw dhw"}))[0]
    pronunciations = (header.findAll("span", {"class": "pron dpron"}))
    pronunciation = ""
    if len(pronunciations) > 0:
        pronunciation = pronunciations[0].getText()
    newWord = structure.Word(headword.getText(), pronunciation, wtype.getText())

    forms = (header.findAll("span", {"class": "irreg-infls dinfls"}))
    if len(forms) > 0:
        for form in forms:
            newWord.irreg_forms.append(form.getText())

    usage_type = (header.findAll("span", {"class": "lab dlab"}))
    if len(usage_type) > 0:
        usage_type = usage_type[0].getText()
    else:
        usage_type = ""
    newWord.usage_type = usage_type

    newWord.translations = requestTranslation(word)
    for definition in definitions:
        formulations = (definition.findAll("div", {"class": "def ddef_d db"}))
        formulation = None
        if len(formulations) > 0:
            formulation = formulations[0].getText()
        else:
            formulation = definition.getText()
        newDefinition = structure.Definition(formulation)
        examples = (definition.findAll("span", {"class": "eg deg"}))
        for example in examples:
            newDefinition += example.getText()
        newWord += newDefinition

    if len(idiom_blocks) > 0:
        for block in idiom_blocks:
            block = (block.findAll("a"))
            for idiom in block:
                newWord.idioms.append(requestCD_subItem(idiom.getText()))

    if len(verb_blocks) > 0:
        for block in verb_blocks:
            block = (block.findAll("a"))
            for verb in block:
                newWord.ph_verbs.append(requestCD_subItem(verb.getText()))

    runtime = time.time() - time_start
    return newWord


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
