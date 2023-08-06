"""строки, c переводом"""
import os
import locale
import pathlib
import remove_duplicates.internationalization as my_int

default_encoding = "utf-8"
# чтобы активировать пользовательскую locale! Для форматирования даты и времени!
# locale.setlocale(locale.LC_ALL, '')
# текущий язык локали
curr_lang = locale.getdefaultlocale()[0][:2].upper()
# полный путь к файлу
src_folder = pathlib.Path(__file__).parent
# чтение интернационализированных строк
_I = my_int.CSVProvider(f"{src_folder}{os.path.sep}translated.csv", "strID", curr_lang)

# переводимые на другие языки строки

strAccessError = _I("strAccessError")
strProcessInfo = _I("strProcessInfo")

strDescription = _I("strDescription")
strEpilog = _I("strEpilog")

strRecursiveSearchBegin = _I("strRecursiveSearchBegin")
strFolderForStor = _I("strFolderForStor")
strLogFileName = _I("strLogFileName")
strFileNamePattern = _I("strFileNamePattern")
strNotRecursively = _I("strNotRecursively")
strInvalidSearchFolder = _I("strInvalidSearchFolder")
strInvalidStorageFolder = _I("strInvalidStorageFolder")

strSearchForDupFilesInFolder = _I("strSearchForDupFilesInFolder")
strPatternFileName = _I("strPatternFileName")
strLogFileName_1 = _I("strLogFileName_1")
strStorFolder = _I("strStorFolder")
strRecursiveSearchDisabled = _I("strRecursiveSearchDisabled")
strActionDel = _I("strActionDel")    # файл удален!
strActionMov = _I("strActionMov")      # файл перемещен!
strTotalFound = _I("strTotalFound")
strLastInfo = _I("strLastInfo")

strInvalidValue = _I("strInvalidValue")
strFileDeleted = _I("strFileDeleted")
strFileMoved = _I("strFileMoved")
