
import csv
import gzip
from os import path
import pickle
import sys
import time
import unicodedata
import click
from click import open_file

# Spanish name particles and prepositions in lower case.
particles = ['de', 'del', 'la', 'el', 'las', 'y', 'i',
             'Mc', 'Van', 'Von', 'Mac', 'Di', 'Della', 'Delle', 'Delli', 'Dello', 'Dell', 'Dels']


def ingest_words(filename, dict, capitation=True, notildado=False, encoding='utf-8', delimiter=';'):
    """
    Load words from csv file and add them to a dictionay with the word in Uppercase as key
    and the word as read from the file as value.
    Args:
        filename (string): File name to load words from.
        dict (dictionay): dictionary to be completed. It will be updated with the words from the file.
        capitation (bool, optional): Controls if the words should be stored with first capital letter. Defaults to True.
        notildado (bool, optional): Controls if words without dyacritics should be stored anyway. Defaults to False.

    Returns:
        dictionary: words added to the dictionary.
    """
    words = {}
    with open_file(filename, 'r', encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if len(row) == 0:
                continue
            word = row[0].strip()
            # change the key to upper case and remove accents.
            keyupper = word.upper()
            # remove diacritics.
            key = unicodedata.normalize('NFKD', keyupper).encode(
                'ASCII', 'ignore').decode('ASCII')

            if notildado == False and key == keyupper:
                continue
            if key in dict or key in words:
                continue
            if capitation:
                words[key] = word.capitalize()
            else:
                words[key] = word
    # Merge the dictionaries.
    dict.update(words)
    print("Added {0} words from {1}. Dictionary size:{2}".format(
        len(words), filename, len(dict)))
    return words

# Change a word to equivalent if it is in the dictionary.


def change_word(word, names_dict):
    if word.strip() == '':
        return word
    # if the word has a hyphen, split it and process recursively.
    if '-' in word:
        words = word.split('-')
        return "-".join([change_word(w, names_dict) for w in words])
    if ',' in word:
        words = word.split(',')
        return ",".join([change_word(w, names_dict) for w in words])
    if '.' in word:
        words = word.split('.')
        return ".".join([change_word(w, names_dict) for w in words])
    # change the key to upper case and remove accents.
    key = word.upper()
    # remove diacritics.
    key = unicodedata.normalize('NFKD', key).encode(
        'ASCII', 'ignore').decode('ASCII')
    # trim the key.
    key = key.strip()
    # if the key is in the dictionary, return the value.
    if key in names_dict:
        return names_dict[key]
    # if not, return the original word capitalized.
    return word.capitalize()

    
# Write dictionary to file.
def write_dict_to_file(filename, names_dict, compress=False, encoding='utf-8', delimiter=';'):
    if compress:
        with open_file(filename, 'wb') as f:
            with gzip.open(f, 'wb') as gf:
                pickle.dump(names_dict, gf)
    else:
        with open_file(filename, 'w', encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator='\n')
            for key in names_dict:
                writer.writerow([key, names_dict[key]])

def build_root_dict(dict):
    # Add prepositions to the dictionary with the key in upper case.
    for prep in particles:
        dict[prep.upper()] = prep
    return dict


def compile_dictionary(dictionaryfile, inputfile, outputfile, compress=True, encoding='utf-8', delimiter=';'):
    if dictionaryfile != None:
        dict = load_dictionary(dictionaryfile)
    else:
        dict = build_root_dict(dict)

    if inputfile != None:
        ingest_words(inputfile, dict=dict, capitation=True, notildado=False, encoding=encoding, delimiter=delimiter)

    write_dict_to_file(outputfile, dict, compress=compress, encoding='utf-8', delimiter=';')

    print("Dictionary size:{0}".format(len(dict)))
    return dict

# Load the dictionary from file.
# If file extension is csv, load the dictionary from csv file.
# Otherwise, load the dictionary from a pickle file.
# If file is 'builtin', load the dictionary from the dictionary.bin file.


def load_dictionary(file):
    if file == 'builtin':
        # If no file is specified, load dictionary.bin file.
        file = path.join(path.dirname(__file__), 'resources/dictionary.bin')
    # Check file extension.
    # Check if file is csv or pickle.
    ext = file.split('.')[-1]
    words_dict = {}
    if ext == 'csv':
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) == 0:
                    continue
                words_dict[row[0]] = row[1]
    else:
        with gzip.open(file, 'rb') as f:
            words_dict = pickle.load(f)
    return words_dict

# Process input file csv and write the output to the output csv file.


def process_file(inputfile, outputfile, columns_to_process, dictionaryfile, encoding = 'utf-8-sig', delimiter = ';'):
    fields_to_process = '*' if columns_to_process=='*' else columns_to_process.split(',')
    # load the dictionary from file.
    words_dict = load_dictionary(dictionaryfile)
    # open the input file.
    with open(inputfile, 'r', encoding=encoding) as f:
        # open the output file.
        with open(outputfile, 'w', encoding=encoding) as f2:
            rows = 0
            # read the input csv.
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            reader = csv.reader(f, dialect=dialect)
            writer = csv.writer(f2, delimiter=delimiter, lineterminator='\n')
            fields = reader.__next__()
            # write headers from input file to the output file.
            writer.writerow(fields)
            for row in reader:
                # process columns in columns_to_process.
                # iterate over the fields in the row.
                for col in range(len(fields)):
                    # get the column value.
                    text = row[col]
                    if fields_to_process != '*' and fields[col] not in fields_to_process:
                        continue
                    # split the string into words.
                    words = text.split()
                    # create a new string with the words processed by change_word function.
                    newstr = " ".join([change_word(word, words_dict)
                                      for word in words])
                    # write the new string to the output file.
                    row[col] = newstr
                rows += 1
                writer.writerow(row)
    print("Processed {0} rows.".format(rows))


def process_words(teststr, dictionaryfile):
    # load the dictionary from file.
    words_dict = load_dictionary(dictionaryfile)
    # split the string into words.
    words = teststr.split()
    # create a new string with the words processed by change_word function.
    newstr = " ".join([change_word(word, words_dict) for word in words])
    print(newstr)

# Procesador de nombres y apellidos. Pasa de todo mayúsculas a capitalizado con tildes y minúsculas.
# arguments: input file, output file, dictionary file, action, compress, words.
# action: compile, process, test.
# compile: compile the dictionary from the csv files.
# process: process the input file and write the output to the output file.
# columns: column names separated by commas to process in the input file.
# test: process the input file and print the output to the console.
# if no arguments are given, the default values are used.
# input file: input.csv
# output file: output.csv
# dictionary file: dictionary.csv|builtin
# action: process
# if the action is compile, the dictionary file is read (opyional), expanded with input (optional) and written to output.
# if the action is test, the output file is not used.
# if the action is process, the input file and the output file are used.
# if the action is test, the words argument is used.
# if the action is process, the columns are used
profiling = False
start_time = time.time()

from . import __version__
@click.group()
@click.option('--profile', is_flag=True, help='Profile the execution time.')
@click.version_option(version=__version__)
def cli(profile):
    global profiling
    profiling = profile
    if profiling:
        click.echo('Profiling on')

def print_profiling():
    global profiling
    if profiling == True:
        click.echo("Elapsed time: {0} seconds.".format(time.time() - start_time))

@cli.command()
@click.argument('action', required=True, type=click.Choice(['process', 'compile', 'filter'], case_sensitive=False))
@click.option('-i', '--input', default=None, type=click.Path(allow_dash=True), help='Input CSV file. For compile action, this is the input file to expand the dictionary. For process action, this is the input CSV to process.')
@click.option('-o', '--output', default=None, type=click.Path(allow_dash=True, writable=True), help='Output file. For compile action, this is the output file to write the dictionary. For process action, this is the output file to write the processed input file.')
@click.option('-d', '--dictionary', required=False, type=click.Path(allow_dash=True), default="builtin", help='Dictionary file. For "compile" action, this is the dictionary file to read and expand. For "process" and "filter" action, this is the dictionary file to use. If not specified, a built-in dictionary is used.')
@click.option('-w', '--words', default='', help='String to filter.')
@click.option('-c', '--columns', default='*', help='Columns to process in the input CSV. Separated by commas. Only for process action, this is the columns to process.')
@click.option('--csv', is_flag=True, help='Don\'t compress the dictionary file.')
@click.option('--encoding', default='utf-8', help='Encoding of the csv.')
@click.option('--delimiter', default=';', help='Delimiter for the csv.')
@click.option('--profile', is_flag=True, help='Profile the execution time.')
def all(action, input, output, columns, words, dictionary, csv, encoding, delimiter, profile):
    """Procesador de nombres y apellidos. Pasa de todo mayúsculas a capitalizado con tildes y minúsculas.\n
    Esta herramienta se ha desarrollado como herramienta de apoyo en la gestión de datos de personas en el directorio de la Universidad de Valladolid.\n
    Name and surname processor. It goes from all uppercase to capitalized with accents and lowercase.\n
    This tool has been developed as a support tool in the management of people data in the directory of the University of Valladolid.\n
    (C) 2023 Juan Pablo de Castro (Universidad de Valladolid)"""
    start_time = time.time()
    if action == 'compile':
        compress = not csv
        compile_dictionary(dictionaryfile=dictionary,
                           inputfile=input, outputfile=output, encoding=encoding, compress=compress)
    elif action == 'process':
        process_file(input, output, columns, dictionary, encoding=encoding, delimiter=delimiter)
    elif action == 'filter':
        process_words(words, dictionary)
    else:
        print("Invalid action: " + action)
    if profile:
        print("Elapsed time: {0} seconds.".format(time.time() - start_time))

@cli.command()
@click.option('-d', '--dictionary', required=False, type=click.Path(allow_dash=True), default="builtin", help='Dictionary file. For "compile" action, this is the dictionary file to read and expand. For "process" and "filter" action, this is the dictionary file to use. If not specified, a built-in dictionary is used.')
@click.option('-w', '--words', default='', help='String to filter.')
def filter(words, dictionary):
    """ Decapitaliza the text passed in --words|-w """
    process_words(words, dictionary)
    print_profiling()

@cli.command()
@click.option('-i', '--input', default=None, type=click.Path(allow_dash=True), help='Input CSV file to process.')
@click.option('-o', '--output', default=None, type=click.Path(allow_dash=True, writable=True), help='Output file to write the processed input file to.')
@click.option('-d', '--dictionary', required=False, type=click.Path(allow_dash=True), default="builtin", help='Dictionary file to use. If not specified, a built-in dictionary is used.')
@click.option('-c', '--columns', default='*', help='Columns to process in the input CSV. Separated by commas.')
@click.option('--encoding', default='utf-8', help='Encoding of the csv.')
@click.option('--delimiter', default=';', help='Delimiter for the csv.')
def process(input, output, columns, dictionary, encoding, delimiter):
    """ Read a csv and decapitaliza a set of columns """
    process_file(input, output, columns, dictionary, encoding=encoding, delimiter=delimiter)
    print_profiling()

@cli.command()
@click.option('-i', '--input', default=None, type=click.Path(allow_dash=True), help='Input CSV file to expand the dictionary with.')
@click.option('-o', '--output', default=None, type=click.Path(allow_dash=True, writable=True), help='Output file. This is the output file to write the dictionary to.')
@click.option('-d', '--dictionary', required=False, type=click.Path(allow_dash=True), default="builtin", help='Dictionary file to read and expand. If not specified, a built-in dictionary is used.')
@click.option('--csv', is_flag=True, help='Don\'t compress the dictionary file.')
@click.option('--encoding', default='utf-8', help='Encoding of the csv.')
def compile(dictionary, input, output, encoding, csv):
    """Generate a new dictionary adding words to a dictionary"""
    compress = not csv
    compile_dictionary(dictionaryfile=dictionary, inputfile=input, outputfile=output, encoding=encoding, compress=compress)
    print_profiling()

# run the command line interface.
if __name__ == '__main__':
    cli()
