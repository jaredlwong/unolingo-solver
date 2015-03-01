from itertools import groupby
import re
import copy
#http://web.stanford.edu/class/cs106l/assignments/dictionary.txt


#word = [symbols]
#symbol = locked or unlocked, value
p = '''
wi ar --b-
a -d-a a -
 t- -ta i-
 ourn  ent
r--a---- o
 na le-c-r
s--l-l ri 
s  ea -a  
--s- -o l-
- e er- eg
'''

class V(object):
    def __init__(self, locked=True, value=None, black=False):
        self.locked = locked
        self.value = value
        self.black = black

    def __repr__(self):
        if self.black:
            return "#"
        if self.value:
            return self.value
        return "_"

    def copy(self):
        return copy.copy(self)
#        return V(self.locked, self.value, self.black)


def to_rows(p):
    return [r for r in p.split("\n") if r != '']

def strs_to_char_lsts(strs):
    return map(list, strs)

def transpose(matrix):
    return map(list, zip(*matrix))

def char_to_var(c):
    if c == ' ':
        return V(locked=False, value=None, black=False)
    if c == '-':
        return V(locked=True, value=None, black=True)
    return V(locked=True, value=c, black=False)

def puzzle_to_rows_cols_vars(p):
    """return list of rows and cols with Vs for chars"""
    rows = strs_to_char_lsts(to_rows(p))
    rows = [[char_to_var(c) for c in r] for r in rows]
    cols = transpose(rows)
    rows.extend(cols)
    return rows

def row_col_to_words(rc):
    groupbyiter = groupby(rc, lambda v: v.black)
    ws = [list(w) for k, w in groupbyiter if not k]
    return filter(lambda w: len(w) > 1, ws)

def puzzle_to_word_vars(p):
    return [w for rc in puzzle_to_rows_cols_vars(p)
              for w in row_col_to_words(rc)]

def dictionary():
    with open('dictionary.txt') as f:
        return [w.rstrip('\n') for w in f.readlines()]

def var_to_regex(v):
    if v.value:
        return v.value
    return "."

def var_word_to_regex(w):
    return re.compile("^" + ''.join(map(var_to_regex, w)) + "$")

def potential_words(vw, d):
    revw = var_word_to_regex(vw)
    #return revw.match("wizard")
    return [w for w in d if revw.match(w)]

def at_least_one_potential_word(vw, d):
    revw = var_word_to_regex(vw)
    for w in d:
        if revw.match(w):
            return True
    return False


def unlocked_variables(wvl):
    return set(c for w in wvl for c in w if not c.locked)

def variable_copy_map(var_set):
    return {v: v.copy() for v in var_set}

def replace_vars(word_var_list, var_map):
    return [[var_map[c] if c in var_map else c for c in w]
            for w in word_var_list]

def copy_word_var_list(wvl):
    var_set = unlocked_variables(wvl)
    var_map = variable_copy_map(var_set)
    return replace_vars(wvl, var_map)

#print row_col_to_words(puzzle_to_rows_cols(p)[0])
#print [c for r in p.split("\n") if r != '' for c in r ]

def word_complete(word):
    return all(c.value for c in word)

def words_unilingo(words):
    values = [v.value for v in unlocked_variables(words)
                      if v.value is not None]
    return len(values) == len(set(values))

def puzzle_possible_solved(words, d):
    words_alpha = words_unilingo(words)
    if not words_alpha:
        return (False, False)
    words_possible = all(at_least_one_potential_word(w, d) for w in words)
    if not words_possible:
        return (False, False)
    words_complete = all(map(word_complete, words))
    return (True, words_complete)

def fill_in_word(word_vars, word_string):
    for i, c in enumerate(word_vars):
        if not c.locked:
            c.value = word_string[i]

def gen_potential_words(words, d):
    def xxx(w):
        if word_complete(w):
            return None
        return potential_words(w, d)
    all_potential_words = [(i, w) for i, w in [(i, xxx(w)) for i, w in enumerate(words)] if w is not None]
    next_words = list()
    index, min_words = min(all_potential_words, key=len)
    for pw in min_words:
        new_words = copy_word_var_list(words)
        fill_in_word(new_words[index], pw)
        next_words.append(new_words)
    return next_words

def solve_puzzle(p, d):
    queue = [puzzle_to_word_vars(p)]
    while len(queue) > 0:
        words = queue.pop()
        print words
        print '-' * 80
        possible, solved = puzzle_possible_solved(words, d)
        if solved:
            return words
        if not possible:
            continue
        queue.extend(gen_potential_words(words, d))
    return None


if __name__ == '__main__':
    d = frozenset(dictionary())
#    print puzzle_to_rows_cols_vars(p)
    #words = puzzle_to_word_vars(p)
    #print unlocked_variables(words)
    #print words
    #print copy_word_var_list(words)
    #w2 = copy_word_var_list(words)
    #print words
#    for w in words:
#        print potential_words(w)
    #words = puzzle_to_word_vars(p)
    #print words
    #print gen_potential_words(words, d)
    #print words
    print solve_puzzle(p, d)
