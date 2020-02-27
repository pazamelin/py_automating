from lxml import etree


class Dictionary:
    def __init__(self):
        self.words = {}


class Word:
    def __init__(self, word, pronun, wtype):
        self.word = word
        self.pronun = pronun
        self.wtype = wtype
        self.irreg_forms = []
        self.definitions = []
        self.idioms = []
        self.ph_verbs = []

    def __eq__(self, other):
        return self.word == other.word

    def __iadd__(self, definition):
        self.definitions.append(definition)
        return self

    def print(self):
        print(self.word + "  " + self.pronun)
        print(self.wtype)
        if len(self.irreg_forms) > 0:
            print(self.word + " | " + self.irreg_forms[0] + " | " + self.irreg_forms[1])
        for definition in self.definitions:
            definition.print()
        if len(self.idioms) > 0:
            print("idioms:")
            for idiom in self.idioms:
                print("  " + idiom)
        if len(self.ph_verbs) > 0:
            print("phrasal verbs:")
            for verb in self.ph_verbs:
                print("  " + verb)

    def xml(self):
        root = etree.Element('WORD_BLOCK')

        e_word = etree.Element('WORD')
        e_word.text = self.word
        root.append(e_word)

        pronunciation = etree.Element('PRONUN')
        pronunciation.text = self.pronun
        root.append(pronunciation)

        wtype = etree.Element('TYPE')
        wtype.text = self.wtype
        root.append(wtype)

        if len(self.irreg_forms) > 0:
            irreg_forms = etree.Element('FORMS')
            irreg_forms.text = self.word + " | " + self.irreg_forms[0]
            root.append(irreg_forms)

        for definition in self.definitions:
            def_block = etree.Element('DEF_BLOCK')

            formulation = etree.Element('FRML')
            formulation.text = definition.formulation
            def_block.append(formulation)

            for example in definition.examples:
                exm = etree.Element('EXM')
                exm.text = example
                def_block.append(exm)
            root.append(def_block)

        if len(self.idioms) > 0:
            idioms = etree.Element('IDIOMS_BLOCK')
            idioms.text = "IDIOMS:"
            for idiom in self.idioms:
                e_idiom = idiom.xml()
                idioms.append(e_idiom)
            root.append(idioms)

        if len(self.ph_verbs) > 0:
            phvb = etree.Element('PHVB')
            phvb.text = "PHRASAL VERBS:"
            for verb in self.ph_verbs:
                e_verb = verb.xml()
                phvb.append(e_verb)
            root.append(phvb)

        return root

    def __str__(self):
        xml_form = self.xml()
        str_res = etree.tostring(xml_form, pretty_print=True, encoding="unicode")
        return str_res


class SubItem:
    def __init__(self, title):
        self.title = title
        self.definitions = []

    def __eq__(self, other):
        return self.title == other.title

    def __iadd__(self, definition):
        self.definitions.append(definition)
        return self

    def print(self):
        print(self.title)
        for definition in self.definitions:
            definition.print()

    def xml(self):
        root = etree.Element('SUB_ITEM')

        title = etree.Element('TITLE')
        title.text = self.title
        root.append(title)

        for definition in self.definitions:
            def_block = etree.Element('DEF_BLOCK')

            formulation = etree.Element('FRML')
            formulation.text = definition.formulation
            def_block.append(formulation)

            for example in definition.examples:
                exm = etree.Element('EXM')
                exm.text = example
                def_block.append(exm)
            root.append(def_block)
        return root

    def __str__(self):
        xml_form = self.xml()
        str_res = etree.tostring(xml_form, pretty_print=True, encoding="unicode")
        return str_res


class Definition:
    def __init__(self, formulation):
        self.formulation = formulation
        self.examples = []

    def __iadd__(self, example):
        self.examples.append(example)
        return self

    def print(self):
        if len(self.formulation) == 0:
            return
        else:
            print(self.formulation)
            for example in self.examples:
                print("  " + example)
