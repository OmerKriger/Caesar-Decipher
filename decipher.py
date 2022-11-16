import json


def decipher_word(word, key, lst_abc):
    res = ""
    for i in range(len(word)):
        char = word[i]
        index_abc = lst_abc.index(char)
        index_abc = (index_abc + key) % 26
        new_char = lst_abc[index_abc]
        res = res + new_char
    return res


def decipher_phrase(phrase, lexicon_filename, abc_filename):
    print(f'starting deciphering using {lexicon_filename} and {abc_filename}')
    lex_file = open(lexicon_filename, 'r', encoding='utf8')
    abc_file = open(abc_filename, 'r', encoding='utf8')
    lst_abc = list(abc_file.read().split())  # Creating list and put the chars in abc_file
    lst_lex = list(lex_file.read().split())  # Creating list, put inside top 10K most freq words in the English lex
    lex_file.close()
    abc_file.close()
    if phrase == '':  # check if the phrase is empty string and finish the search
        print('Empty phrase!')
        return None  # return None for print that string can't be decipher
    res = {"orig_phrase": '', "K": -1}
    for k in range(len(lst_abc)):  # run about all of the possibilities for K and search the right one
        new_sentence = ''  # the new possible right sentence will add to this string
        for word in phrase.split():  # trying to decipher word by word from the phrase
            new_word = decipher_word(word, k, lst_abc)  # decipher the cipher word by the key and list of abc
            if new_word in lst_lex:
                if new_sentence == '':  # check if this is the first word in sentence
                    new_sentence += new_word
                else:  # if is not the first add space before the next word
                    new_sentence += " " + new_word
            else:  # if the new work is not in lst_lex
                break  # skip to the next k to check
        else:  # if we didn't break the for loop (we found the right k)
            res["K"] = k
            res["orig_phrase"] += new_sentence
            return res  # return the res we found
    else:  # we didn't find the right K
        return None  # return None for unable to decipher this word


if __name__ == '__main__':
    with open('config-decipher.json', 'r') as json_file:
        config = json.load(json_file)

    result = decipher_phrase(config['secret_phrase'], config['lexicon_filename'], config['abc_filename'])

    if result:
        print(f'deciphered phrase: {result["orig_phrase"]}, K: {result["K"]}')
    else:
        print("Cannot decipher the phrase!")
