import sys
import nltk
import re
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download('averaged_perceptron_tagger')

TAGS = {
    'PREPOSITION': 'IN',
    'CONJUNCTION': 'CC',
    'ARTICLE': 'RP'
}

def get_base_file():
    argument = sys.argv[1]
    return open(argument, 'r')

def get_text_in_files(base_file):
    files = base_file.read()
    return [open(file, 'r').read() for file in files.split('\n')]

def get_stopwords():
    return nltk.corpus.stopwords.words('portuguese')

def transform_list_to_text(list):
    return ' '.join(list)

def is_preposition_conjuntion_article(word):
    return word[1] == TAGS['PREPOSITION'] and word[1] == TAGS['CONJUNCTION'] and TAGS['ARTICLE']

def filter_preposition_conjunction_article(list):
    words_tags = nltk.pos_tag(list)
    return [word[0] for word in words_tags if not is_preposition_conjuntion_article(word)]

def filter_list(text):
    stemmer = nltk.stem.RSLPStemmer()
    list = re.sub(r' |\.|,|!|\?|\...|\n', ' ', text).split()
    list_filtered = filter_preposition_conjunction_article(list)
    return [stemmer.stem(word.lower()) for word in list_filtered if word not in get_stopwords()]

def create_dictionary(list):
    return { word: {} for word in list }

def indexing(list, dictionary, text_files):
    for word in list:
        for i in range(len(text_files)):
            filtered_text_file = filter_list(text_files[i])
            if word in filtered_text_file:
                dictionary[word][i + 1] = filtered_text_file.count(word)

def transform_index_to_write(index):
    remove_brackets = re.sub(r'{|}', '', index);
    remove_two_points = re.sub(r': ', ',', remove_brackets)
    return remove_two_points


def write_dictionary_in_file(dictionary):
    index_file = open('./indice.txt', 'w+')
    for word, index in dictionary.items():
        index_file.write(word + ': ' + transform_index_to_write(str(index)) + '\n')
    index_file.close()

def main():
    text_files = get_text_in_files(get_base_file())
    filtered_list = filter_list(transform_list_to_text(text_files))
    dictionary = create_dictionary(filtered_list)
    indexing(filtered_list, dictionary, text_files)
    write_dictionary_in_file(dictionary)
    print(dictionary)

main()


