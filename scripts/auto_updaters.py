import sys
from datetime import datetime
from apps.dictionary.models import (
    EnglishWord,
    WordPair
)
from . autodict import (
    # test_a,
    a_words,
    b_words,
    c_words,
    d_words,
    e_words,
    f_words,
    g_words,
    h_words,
    i_words,
    j_words,
    k_words,
    l_words,
    m_words,
    n_words,
    o_words,
    p_words,
    q_words,
    r_words,
    s_words,
    t_words,
    u_words,
    v_words,
    w_z_words
)
from . new_words_one import (
    new_words,
    d_k_words
)


def add_english_words(filename: str) -> None:
    """Adds new English words to the dictionary from a text file"""
    print("STARTED:", datetime.now())
    with open(filename, "r") as f:
        english_words: list = f.readlines()
    count = 0
    for word in english_words:
        if word.isupper():
            try:
                new_word = EnglishWord(word=word, word_case="Proper Noun")
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
        else:
            try:
                new_word = EnglishWord(word=word)
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
    print(count, "English words were added)")
    print("ENDED:", datetime.now())
    return


def add_eng_words(words_dict: dict[str, list[str]]) -> None:
    """Adds new English words to the dictionary from a python list"""
    print("STARTED:", datetime.now())
    words_list: list[str] = [word for word in words_dict]
    count = 0
    for word in words_list:
        if word[0].isupper():
            try:
                new_word = EnglishWord(word=word, word_case="Proper Noun")
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
        else:
            try:
                new_word = EnglishWord(word=word)
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
    print(count, "English words were added)")
    print("ENDED:", datetime.now())
    return


def add_osh_words(words_dict: dict) -> None:
    """Adds new Oshindonga words to the dictionary from a python dictionary"""
    print("STARTED:", datetime.now())
    words_list = [word for word in words_dict]
    count = 0
    for word in words_list:
        for osh_word in words_dict[word]:
            try:
                new_word = WordPair(
                    english_word=EnglishWord.objects.get(word=word), oshindonga_word=osh_word
                )
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
    print(count, "Oshindonga words were added)")
    print("ENDED:", datetime.now())
    return


update = [
    a_words,
    b_words,
    c_words,
    d_words,
    e_words,
    f_words,
    g_words,
    h_words,
    i_words,
    j_words,
    k_words,
    l_words,
    m_words,
    n_words,
    o_words,
    p_words,
    q_words,
    r_words,
    s_words,
    t_words,
    u_words,
    v_words,
    w_z_words,
    new_words,
    d_k_words
]
for obj in update:
    add_eng_words(obj)
    add_osh_words(obj)

# add_eng_words(test_a)
# add_osh_words(test_a)