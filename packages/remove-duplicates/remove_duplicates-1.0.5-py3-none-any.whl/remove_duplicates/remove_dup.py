#!/usr/bin/env python3
"""utility to move/delete duplicate files of the same size and context in specified folder.

command string parameters:
first parameter:    full_path_to_folder - folder where duplicates are searched.
second parameter:   optional - folder for storage duplicate files """

import sys
import logging
import pathlib
import argparse
import remove_duplicates.my_utils as my_utils
import remove_duplicates.str_with_trans as str_with_trans


def _win32_behavior(pth: str) -> str:
    """Костыль для платформы win32. Если в функцию передан путь который не является ни файлом и не папкой,
    то возвращается путь к родительскому каталогу"""
    path = pathlib.Path(pth)
    if not path.is_file() and not path.is_dir():
        return str(path.parent.resolve())
    return str(path.resolve())


def recursive_process_folder(start_folder: str, trash_folder: str,
                             file_name_pattern: list, not_recursively: bool = False):
    """
    :param start_folder: Search for duplicate files starts from this folder.
    :param trash_folder: found copies of files are transferred to this folder.
    :param file_name_pattern: Only files matching the pattern are processed.
    :param not_recursively: If this parameter is set, then recursive search is disabled!
    :return: count file copies deleted/moved."""
    ret_val = 0
    try:
        ret_val = my_utils.delete_duplicate_file(start_folder, file_name_pattern, trash_folder, logging)
    except PermissionError as ex:
        #  logging.warning(f"Folder {start_folder}. OS Error code: {ex.errno}. Error message: {ex.strerror}!")
        logging.warning(str_with_trans.strAccessError + str(ex))
    else:
        logging.info(str_with_trans.strProcessInfo.format(start=start_folder, retval=ret_val))

    if not_recursively:
        return ret_val

    # enumerating
    pth = pathlib.Path(start_folder)
    for child in pth.iterdir():
        try:
            if child.is_dir():
                ret_val += recursive_process_folder(str(child.resolve()), trash_folder, file_name_pattern)
        except PermissionError:
            folder_name = str(child.resolve())
            logging.warning(str_with_trans.strAccessError + folder_name)
    # return value
    return ret_val


def main() -> int:
    """return: count file copies deleted/moved!
    If error return my_utils.INVALID_VALUE."""
    # изменяю кодировку stdout
    sys.stdout.reconfigure(encoding=str_with_trans.default_encoding)
    str_storage_folder, str_search_folder, log_file_name = None, None, None     # default values

    if "win32" == sys.platform:
        # На платформе win32 аргумент sys.argv[0] содержит не имя выполняемого файла,
        # а имя несуществующего файла python скрипта!
        # Проверял под python 3.10 в Win10. В Debian 11 все в порядке.
        str_search_folder = _win32_behavior(sys.argv[0])
    else:  # other platform
        str_search_folder = my_utils.get_folder_name_from_path(sys.argv[0])

    parser = argparse.ArgumentParser(description=str_with_trans.strDescription, epilog=str_with_trans.strEpilog)

    parser.add_argument("-st", "--start_folder", type=str, help=str_with_trans.strRecursiveSearchBegin)
    parser.add_argument("-rb", "--recycle_bin", type=str, help=str_with_trans.strFolderForStor)
    parser.add_argument("-log", "--log_file", type=str, help=str_with_trans.strLogFileName)
    parser.add_argument("-fnp", "--fn_pattern", type=str, help=str_with_trans.strFileNamePattern, default="*.*")
    parser.add_argument("-nr", "--not_recursively", action="store_true", help=str_with_trans.strNotRecursively)

    args = parser.parse_args()

    fn_pattern = ""
    if args.fn_pattern:
        fn_pattern = args.fn_pattern.replace(" ", "")  # удаляю все пробелы из строки
        fn_pattern = fn_pattern.split(",")  # создаю список

    if args.log_file:
        log_file_name = args.log_file
    # setup logger start
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Если пользователь не задал имя файла-журнала, поэтому журналом становится sys.stdout
    handler = logging.StreamHandler(sys.stdout)
    if log_file_name:
        handler = logging.FileHandler(log_file_name, "w", "utf-8")

    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
    root_logger.addHandler(handler)
    # setup logger end

    if args.start_folder:
        str_search_folder = args.start_folder
        if not my_utils.is_folder_exist(str_search_folder):
            logging.critical(str_with_trans.strInvalidSearchFolder.format(search_folder=str_search_folder))
            return my_utils.INVALID_VALUE

    if args.recycle_bin:
        str_storage_folder = args.recycle_bin
        if not my_utils.is_folder_exist(args.recycle_bin):
            logging.critical(str_with_trans.strInvalidStorageFolder.format(stor_folder = args.recycle_bin))
            return my_utils.INVALID_VALUE

    # START
    logging.info(str_with_trans.strSearchForDupFilesInFolder.format(folder_name=str_search_folder))
    logging.info(str_with_trans.strPatternFileName.format(pattern=fn_pattern))
    if log_file_name:
        logging.info(str_with_trans.strLogFileName_1.format(log=log_file_name))
    if str_storage_folder:
        logging.info(str_with_trans.strStorFolder.format(storage=str_storage_folder))
    if args.not_recursively:
        logging.info(str_with_trans.strRecursiveSearchDisabled)

    ret_val = recursive_process_folder(str_search_folder, str_storage_folder, fn_pattern, args.not_recursively)

    action = str_with_trans.strActionDel
    if args.recycle_bin:
        action = str_with_trans.strActionMov

    logging.info(str_with_trans.strTotalFound.format(total=ret_val))

    if ret_val:
        logging.info(str_with_trans.strLastInfo.format(cnt=ret_val, action=action))

    return ret_val


if __name__ == "__main__":
    sys.exit(main())
