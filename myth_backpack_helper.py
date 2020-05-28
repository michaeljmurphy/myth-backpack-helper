import os
import argparse
import shutil

SUPPORTED_LANGUAGES = {
    "en" : "en-EN"
    , "de" : "de-DE"
    , "fr" : "fr-FR"
    , "es" : "es-MX"
    , "pt" : "pt-BR"
    , "jp" : "ja-JP"
}

def parse_args():
    """parse all args"""

    parser = argparse.ArgumentParser(description="Add localisation directories to a myTrailhead backpack")
    parser.add_argument("-v"
                        , "--verbose"
                        , help="verbose mode"
                        , default=False)
    parser.add_argument("-p"
                        , "--path"
                        , type=dir_path
                        , help="path to module backpack")
    parser.add_argument("-l", "--languages"
                        , nargs="+"
                        , type=supported_language
                        , help="language folders to add, supported languages are: en, de, jp, es, fr, pt")
    args = parser.parse_args()
    return args

def dir_path(string):
    """check the path is actually a directory"""

    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError(f"The path: {string} is not a valid directory")
    return string

def supported_language(string):
    """check we are actually using a supported language"""

    if string not in SUPPORTED_LANGUAGES.keys():
        raise argparse.ArgumentTypeError(f"The language: {string} is not supported")
    return string


def copy_unit_images(path, directory, lang):
    """copy the images for a unit"""

    # do nothing for the labels folder
    if directory == "labels":
        return
    
    # if not in labels folder we are in a unit
    for root, dirs, files in os.walk(path):
        # walk through the directories
        for sub_directory in dirs:
            # if image directory
            if sub_directory != "images":
                continue
            os.mkdir(os.path.join(path, sub_directory, SUPPORTED_LANGUAGES[lang]))
            for image in files:
                shutil.copyfile(os.path.join(path, sub_directory, image)
                                , os.path.join(path, sub_directory, SUPPORTED_LANGUAGES[lang]))

def copy_labels(path, directory, lang):
    """copy the labels from the root dir"""

    # sort out the labels file
    if directory == "labels":
        os.mkdir(os.path.join(path, directory, SUPPORTED_LANGUAGES[lang]))
        shutil.copyfile(os.path.join(path, directory, "labels.yml")
                        , os.path.join(path, directory, SUPPORTED_LANGUAGES[lang]))

def copy_unit_files(path, directory, lang):
    """copy the unit files"""

    # create the language dir within the unit
    os.mkdir(os.path.join(path, directory, SUPPORTED_LANGUAGES[lang]))
    
    # copy the files... hard coded for now
    shutil.copyfile(os.path.join(path, directory, "evaluation.json")
                    , os.path.join(path, directory, SUPPORTED_LANGUAGES[lang]))
    shutil.copyfile(os.path.join(path, directory, "content.html")
                    , os.path.join(path, directory, SUPPORTED_LANGUAGES[lang]))
    shutil.copyfile(os.path.join(path, directory, "toc.html")
                    , os.path.join(path, directory, SUPPORTED_LANGUAGES[lang]))

def create_dirs(path, languages):
    """create all the directories"""

    # get the structure
    for root, dirs, files in os.walk(path):
        # walk through the directories
        for directory in dirs:
            # for each supported lanaguage
            for lang in languages:
                copy_labels(path, directory, lang)
                copy_unit_files(path, directory, lang)
                copy_unit_images(path, directory, lang)

if __name__ == "__main__":
    args = parse_args()
    create_dirs(args.path, args.languages)
