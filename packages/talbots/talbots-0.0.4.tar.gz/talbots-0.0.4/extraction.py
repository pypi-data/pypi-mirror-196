import os
import json
import re
from .paths import Paths
from PyPDF2 import *

class Extraction:
    def __init__(self) -> None:
        pass

    def save_into_json(self, fileName, data):
        try:
            if not os.path.exists(fileName):
                raise FileExistsError
            with open(fileName,'r+') as file:
                a = json.load(file)
                for d in data:
                    a.append(d)
                file.seek(0)
                json.dump(a, file, indent = 2)
        except json.decoder.JSONDecodeError:
            with open(fileName,'w') as file:
                json.dump(data, file, indent = 2)
        except FileExistsError:
            print("Cannot find this file!")

    def get_phrases(self, fileName, column = None):
        try:
            if not os.path.exists(fileName):
                raise FileNotFoundError
            availableExtensions = [".txt", ".csv", ".xlsx"]
            flag = False
            e = ""
            for extension in availableExtensions:
                le = -1 * len(extension)
                e = fileName[le:]
                if e == extension:
                    flag = True
                    break
            if not flag:
                raise NameError
            else:
                p = Paths()
                if e == ".txt":
                    return p.data_txt(fileName)
                elif e == ".csv":
                    return p.data_csv(fileName, column)
                elif e == ".xlsx":
                    return p.data_excel(fileName, column)
        except NameError:
            print("Cannot read this type of file!")
        except FileNotFoundError:
            print("Cannot find this file!")

    def extract(self, phrases, pdfFile):
        try:
            if pdfFile[-4:] != ".pdf":
                pdfFile += ".pdf"
            if not os.path.exists:
                raise FileNotFoundError
            result = []
            doc = PdfReader(pdfFile, strict=False)
            pages = len(doc.pages)
            for page in range(pages):
                text = doc.pages[page].extract_text()
                for phrase in phrases:
                    found_phrase_count = len(re.findall(phrase.lower(), text.lower()))
                    if found_phrase_count != 0:
                        if len(result) == 0:
                            result.append({"page":page, "phrases":[{"phrase" : phrase.lower(), "count" : found_phrase_count}]})
                        else:
                            if result[-1]["page"] == page:
                                result[-1]["phrases"].append({"phrase" : phrase.lower(), "count" : found_phrase_count})
                            else:
                                result.append({"page":page, "phrases":[{"phrase" : phrase.lower(), "count" : found_phrase_count}]})

            return result
        except FileNotFoundError:
            print("Cannot find this file!")