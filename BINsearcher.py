from os import listdir, makedirs
from os.path import exists, isfile
from re import findall
from sys import exit, argv

from natsort import natsorted, ns


def find_bin_files(keywords, files, folder=""):
    try:
        data, i, response = {}, 1, True

        for file in files:
            print(f"[{i} из {len(files)}] Ищем данные в: {folder}{file}")

            try:
                with open(file=f"{folder}{file}",
                          mode="rb") as input_bin_file:
                    for line in input_bin_file.readlines():
                        for keyword in keywords:
                            if keyword not in data:
                                data.update({keyword: []})
                            for word in findall(pattern=rb"(%s_\w+)" % keyword.encode(encoding="UTF-8",
                                                                                      errors="ignore"),
                                                string=line):
                                if (word.decode(encoding="UTF-8",
                                                errors="ignore") not in data[keyword]):
                                    data[keyword].append(word.decode(encoding="UTF-8",
                                                                     errors="ignore"))
            except Exception:
                print(f"[WARNING] При обработке файла {folder}{file} возникла ошибка. "
                      f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                      f"Файл пропущен.\n")

                response = (False if response else False)

            i += 1

        if not exists(path="BINsearcher"):
            print(f"2: Создание папки BINsearcher.\n")

            try:
                makedirs(name="BINsearcher")
            except Exception:
                print(f"[ERROR] Во время создания папки BINsearcher возникла ошибка. "
                      f"Возможно нет прав на создания папок.\n")

                response = False

        for key in data:
            words = natsorted(seq=data[key],
                              alg=ns.IGNORECASE)

            print(f"3: Создание файла BINsearcher/{key}.txt.\n")

            try:
                with open(file=f"BINsearcher/{key}.txt",
                          mode="w",
                          encoding="UTF-8") as output_txt_file:
                    for item in words:
                        output_txt_file.write(f"{item}\n")
            except Exception:
                print(f"[WARNING] Во время создания файла BINsearcher/{key}.txt возникла ошибка. "
                      f"Возможно нет прав на создания файлов."
                      f"Файл пропущен.\n")

                response = False

        return response
    except Exception:
        print("[ERROR] Во время обработки файлов возникла ошибка. "
              "Возможно файлы повреждены или нет прав на чтение файлов.\n")

        return False


def load_file_settings():
    try:
        if exists(path="BINsearcher.txt"):
            print("1: Обработка файла BINsearcher.txt.\n")

            with open(file="BINsearcher.txt",
                      mode="r",
                      encoding="UTF-8") as input_file_txt:
                keywords = [x.strip() for x in input_file_txt.readlines() if x.strip()]

                if len(keywords) > 0:
                    files = [x for x in argv[1:] if (isfile(path=x) and x.endswith(".bin"))]

                    if len(files) > 0:
                        return find_bin_files(keywords=keywords,
                                              files=files,
                                              folder="")
                    else:
                        if exists(path="bin"):
                            files = [x for x in listdir(path="bin") if
                                     (isfile(path=f"bin/{x}") and f"bin/{x}".endswith(".bin"))]

                            if len(files) > 0:
                                return find_bin_files(keywords=keywords,
                                                      files=files,
                                                      folder="bin/")
                            else:
                                print("[ERROR] В папке bin нет файлов. "
                                      "Загрузите в нее бинарные файлы в которых нужно найти данные.\n")

                                return False
                        else:
                            print(f"[ERROR] Папки bin не существует. "
                                  f"Будет создана пустая папка. "
                                  f"Загрузите в нее бинарные файлы в которых нужно найти данные.\n")

                            try:
                                makedirs(name="bin")
                            except Exception:
                                print(f"[ERROR] Во время создания папки bin возникла ошибка. "
                                      f"Возможно нет прав на создания папок.\n")

                            return False
                else:
                    print("[ERROR] В файле BINsearcher.txt нет ключевых слов. "
                          "Добавьте ключевые слова в этот файл. "
                          "На одной строке одно слово. "
                          "Для работы программы нужно добавить хотя бы один.\n")

                    return False
        else:
            print("[INFO] Файл настроек BINsearcher.txt не обнаружен. "
                  "Будет создан новый пустой файл. "
                  "Добавьте в него ключевые слова. "
                  "На одной строке одно слово. "
                  "Для работы программы нужно добавить хотя бы один.\n")

            try:
                with open(file="BINsearcher.txt",
                          mode="w",
                          encoding="UTF-8") as input_file_txt:
                    input_file_txt.close()
            except Exception:
                print("[ERROR] Во время создания файла BINsearcher.txt возникла ошибка. "
                      "Возможно нет прав на создания файлов.\n")

            return False
    except Exception:
        print("[ERROR] Во время обработки файла настроек BINsearcher.txt возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")

        return False


if __name__ == "__main__":
    try:
        if load_file_settings():
            exit()
        else:
            raise Exception
    except Exception:
        print("[INFO] Работа программы завершена, но во время работы возникли ошибки!\n")

        input()
        exit()
