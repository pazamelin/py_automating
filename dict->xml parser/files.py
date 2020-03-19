from lxml import etree
from scrape import requestCD, requestUD


def dumpWord(filename, word):
    file_properties = open("properties.txt", 'r')
    properties = []
    for line in file_properties:
        properties.append(line)
    file_properties.close()
    out = open(filename, 'w')

    for element in properties:
        out.write(element)
    out.write('\n')
    out.write("<DICTIONARY>\n")
    out.write(str(word))
    out.write('\n')
    out.write("</DICTIONARY>\n")

    out.close()


def appendWord(xmlFile, word):
    out = open(xmlFile, 'a')
    out.write(str(word))
    out.write('\n')
    out.close()


def inputList(fileName):
    result = []
    file = open(fileName, 'r')
    for line in file:
        result.append(line)
    file.close()
    return result


def handleList(inputFile, out_xmlFile):
    wordlist = inputList(inputFile)
    if len(out_xmlFile) == 0:
        file_properties = open("properties.txt", 'r')
        properties = []
        for line in file_properties:
            properties.append(line)
        file_properties.close()

        out = open(inputFile[:-4] + "_out.xml", 'w')

        for element in properties:
            out.write(element)
        out.write('\n')
        out.write("<DICTIONARY>\n")
    else:
        out = open(out_xmlFile, 'a')

    for word in wordlist:
        print(word)
        res = requestCD(word[:-1])
        out.write(str(res))
        out.write('\n')

    if len(out_xmlFile) == 0:
        out.write("</DICTIONARY>\n")

    out.close()


def sortAlphabet(inputFile):
    wordlist = inputList(inputFile)
    wordlist.sort()
    rewrite = open(inputFile, 'w')
    for word in wordlist:
        rewrite.write(word)
    rewrite.close()



