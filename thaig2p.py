import html, re, tltk, csv
from pythainlp import word_tokenize

##################################################
### CONSTANTS
##################################################

SHORT_VOWELS = "aiɯueɛoɔə"
LONG_VOWELS =  "AIWUEYOXZ"
DIPHTHONGS = "JRV"
VOWELS = SHORT_VOWELS + LONG_VOWELS + DIPHTHONGS
CLUSTERS = ["br","bl","pr","pl","Pr","Pl","fr","fl","dr","tr","Tr","kr","kl","kw","Kr","Kl","Kw"]
ONSETS = ["b","p","P","m","f","d","t","T","n","s","r","l","c","C","k","K","ŋ","w","j","h","ʔ"]
CODAS = ["p","m","f","t","d","n","s","l","k","ŋ","w","j","ʔ","-"]

# read dictionary
with open('thai2phone.csv') as f:
    THAI2PHONE_DICT = dict(csv.reader(f))
    THAI2PHONE_DICT = {k:v for k,v in THAI2PHONE_DICT.items() if v != ''}
with open('number2phone.csv') as f:
    NUMBER2PHONE_DICT = dict(csv.reader(f))

##################################################
### UTILS FUNCTIONS FOR HANDLING PHONES (invisible)
##################################################

# convert short vowel <> long vowel
def __short2long(vowel_phone):
    """convert short vowel into long vowel
    >>> short2long('a') -> A
    """
    try:
        return LONG_VOWELS[SHORT_VOWELS.index(vowel_phone)]
    except:
        return None

def __long2short(vowel_phone):
    """convert long vowel into short vowel
    >>> short2long('A') -> a
    """
    try:
        return SHORT_VOWELS[LONG_VOWELS.index(vowel_phone)]
    except:
        return None

def __validate(phone):
    """validate encoded phone
    >>> validate('paj1 dAj3') -> True
    >>> validate('aaa aaa') -> False
    """
    syls = phone.split()
    for syl in syls:
        try:
            tone = syl[-1] # prA-1 -> 1
            coda = syl[-2] # prA-1 -> -
            vowel = syl[-3] # prA-1 -> A
            onset = syl[:-3] # # prA-1 -> pr
        except:
            return False 
        # check all 4 parts are valid
        if tone.isdigit() and coda in CODAS and vowel in VOWELS and onset in CLUSTERS+ONSETS:
            continue
        else:
            return False
    return True

def __get_tones(phone):
    """get all tones of one word
    >>> get_tones('paj1 dAj3') -> (1, 3)
    """
    return tuple(syl[-1] for syl in phone.split())

def __get_onsets(phone, ipa=False):
    """get all onsets of one word
    >>> get_onsets('paj1 dAj3') -> (p, d)
    """
    return tuple(syl[:-3] for syl in phone.split())

def __get_vowels(phone):
    """get all vowels of one word
    >>> get_tones('paj1 dAj3') -> (a, A)
    """
    return tuple(syl[-3] for syl in phone.split())

def __get_codas(phone):
    """get all codas of one word
    >>> get_codas('paj1 dAj3') -> (j, j)
    """
    return tuple(syl[-2] for syl in phone.split())

def __get_vowels_tone(phone):
    """get all vowels & tones of one word
    >>> get_vowels_tone('paj1 dAj3') -> (a1, A3)
    """
    return tuple(syl[-3]+syl[-1] for syl in phone.split())

def __decode(phone, transcription='haas'):
    """decode phone into Haas or IPA
    :phone: encoded phone
    :transcription: - 'haas' or 'ipa'
    >>> decode('" kot2 mAj5 ʔA-1 jA-1 "', 'ipa') ->  " kòt mǎːj ʔaː jaː "
    """
    decoded_syls = []
    syls = phone.split() # ['kot2','mAj5']
    for i, syl in enumerate(syls):
        if not __validate(syl): # e.g. English, punctuation
            decoded_syls.append(syl)
            continue
        tone = syl[-1]
        coda = syl[-2]
        if i != len(syls) - 1: # if not the final syllable, delete ʔ
            coda = coda.replace('ʔ','-') # "-" = no coda
        vowel = syl[-3]
        onset = syl[:-3] # one or two characters
        if transcription == 'ipa':
            decoded_syls.append(''.join([PHONE2IPA[c] for c in onset]) + PHONE2IPA[vowel+tone] + PHONE2IPA[coda])
        elif transcription == 'haas':
            decoded_syls.append(''.join([PHONE2HAAS[c] for c in onset]) + PHONE2HAAS[vowel+tone] + PHONE2HAAS[coda])
    return ' '.join(decoded_syls)

"""
def tokenize(text, delete_newline=True, twitter=False):
    text = html.unescape(text)
    if twitter:
        text = re.sub(r'@.+?(?:\s|$)', '', text) # for twitter
        text = re.sub(r'pic\.twitter\.com.+?(?:\s|$)', '', text) # for twitter
    text = re.sub(r'http.+?\b', '', text)
    text = re.sub(r'[“”„]', '"', text) # convert double quotations into "
    text = re.sub(r'[‘’`]', "'", text) # convert single quotations into '
    text = re.sub(r'[ \u00a0\xa0\u3000\u2002-\u200a\t]+', ' ', text) # e.g. good  boy -> good boy
    text = re.sub(r'[\r\u200b\ufeff]+', '', text) # remove non-breaking space
    text = text.strip()
    if delete_newline:
        text = re.sub(r'\n+', ' ', text)
    tokens = word_tokenize(text, keep_whitespace=False)
    return [token.strip('"').strip("'").strip("(").strip(")") for token in tokens]
"""

def __get_phone_word(thaiword:str):
    # if the word in the dict, return the phone
    # ไป -> paj1
    return THAI2PHONE_DICT.get(thaiword, None)

def __is_time(text:str):
    return bool(re.match(r'\d{1,2}[:\.]\d{1,2}', text))

def __get_phone_time(time:str):
    # 20.31 -> jI-3 sip2 nA-1 liʔ4 kA-1 sAm5 sip2 ʔet2 nA-1 TI-1
    hour, minute = re.split(r'[:\.]', time)
    if minute == '00':
        return __get_phone_number(hour) + ' nA-1 li-4 kA-1'
    else:
        return __get_phone_number(hour) + ' nA-1 li-4 kA-1 ' + __get_phone_number(minute) + ' nA-1 TI-1'

def __is_number(text:str):
    return bool(re.match(r'\-?\d[\d\,]*(?:\.\d+)?$', text))

def __get_phone_number(number:str):
    # 3,120 -> sAm5 Pan1 rXj4 jI-3 sip2
    # 123.123 -> nɯŋ2 rXj4 jI-3 sip2 sAm5 cut2 nɯŋ2 sXŋ5 sAm5
    number = str(number) # float 123.5 -> str "123.5"
    if re.match(r'0[0-9]*[1-9]+', number): # e.g. 0012 (exclude 0, 00)
        number = number.lstrip('0') # 0012 -> 12
    number = number.replace(',', '') # 1,000 -> 1000
    minus = number[0] == '-' # bool to check negative
    number = number.strip('-') # delete initial -
    if '.' not in number: # if integer
        length = len(number)
        if length <= 2:
            if number in NUMBER2PHONE_DICT:
                phone = NUMBER2PHONE_DICT[number]
            else:
                phone = NUMBER2PHONE_DICT[number[0]+'0'] + ' ' + NUMBER2PHONE_DICT[number[1]] # 34 -> 30 + 4
        elif length <= 7: # 7 = million = ล้าน
            if number in NUMBER2PHONE_DICT:
                phone = NUMBER2PHONE_DICT[number]
            else:
                phone = NUMBER2PHONE_DICT[number[0]+'0'*(length-1)] + ' ' + __get_phone_number(number[1:]) # 345 -> 300 + 45 (recursive)
        elif length <= 12: # 12 = trillion = ล้านล้าน
            # 123456000 -> 123 + ล้าน + 456000
            upper = number[:-6]
            lower = number[-6:] # xxx ล้าน
            if lower == '000000':
                phone = __get_phone_number(upper) + ' lAn4'
            else:
                phone = __get_phone_number(upper) + ' lAn4 ' + __get_phone_number(lower)
        else:
            return number # longer than 12, return original
    else: # if decimal
        integer, decimal = number.split('.')
        decimal = ' '.join([__get_phone_number(x) for x in decimal]) # get one by one
        phone = __get_phone_number(integer) + ' cut2 ' + decimal
    if minus:
        return 'lop4 ' + phone
    else:
        return phone

##################################################
### G2P FUNCTIONS
##################################################

# try tokenization by pythainlp -> look up dictionary
# if there is None, try use tltk instead
def g2p(sentence:str, transcription='haas', return_tokens=False):
    """G2P function for Thai sentence

    Parameters
    ----------
    sentence : str
        Thai sentences
    transcription : str
        'haas'(default) or 'ipa'
    return_token : bool
        whether return also tokenized sentence

    Returns
    -------
    str
        syllables delimited by whitespaces 
        or list of [token, phone]

    >>> g2p('ไปโรงเรียน') -> 'paj rooŋ rian'
    >>> g2p('ไปโรงเรียน', transcription='ipa') -> 'paj roːŋ rian'
    >>> g2p('ไปโรงเรียน', return_tokens=True) -> [['ไป', 'pay'], ['โรงเรียน', 'rooŋ rian']]
    """

    ### preprocessing ###
    sentence = re.sub(r'[\n\s]+', ' ', sentence) # shrink whitespaces
    sentence = re.sub(r'http[^\s]+((?=\s)|(?=$))', '', sentence) # remove URL

    ### tokenize ###
    tokens = word_tokenize(sentence, keep_whitespace=False)
    token_phone_list = []

    ### check each token ###
    for i, token in enumerate(tokens):
        if token == 'น.' and i > 0 and (token_phone_list[i-1][1] == 'nA-1 li-4 kA-1' or token_phone_list[i-1][1] == 'nA-1 TI-1'): # avoid duplicate
            continue
        elif token == 'ๆ' and i > 0: # if single ๆ, repeat final one
            token_phone_list[-1][0] += ' ๆ'
            token_phone_list[-1][1] += ' ' + token_phone_list[-1][1]
        elif token in THAI2PHONE_DICT:
            phone = __decode(__get_phone_word(token), transcription=transcription)
        elif re.match(r'[ก-๙][ก-๙\-\.]*$', token): # thaiword, but not in dictionary
            phone = None
        elif __is_time(token):
            phone = __decode(__get_phone_time(token), transcription=transcription)
        elif __is_number(token):
            phone = __decode(__get_phone_number(token), transcription=transcription)
        else: # do nothing for the others, e.g. english, punctuation...
            phone = token
        token_phone_list.append([token, phone])
    if return_tokens:
        return token_phone_list
    else:
        return ' '.join([phone for _, phone in token_phone_list])


PHONE2IPA = {
    'a1':'a', 'a2':'à', 'a3':'â', 'a4':'á', 'a5':'ǎ',
    'A1':'aː','A2':'àː','A3':'âː','A4':'áː','A5':'ǎː',
    'i1':'i', 'i2':'ì', 'i3':'î', 'i4':'í', 'i5':'ǐ',
    'I1':'iː','I2':'ìː','I3':'îː','I4':'íː','I5':'ǐː',
    'u1':'u', 'u2':'ù', 'u3':'û', 'u4':'ú', 'u5':'ǔ',
    'U1':'uː','U2':'ùː','U3':'ûː','U4':'úː','U5':'ǔː',
    'ɯ1':'ɯ', 'ɯ2':'ɯ̀', 'ɯ3':'ɯ̂', 'ɯ4':'ɯ́', 'ɯ5':'ɯ̌',
    'W1':'ɯː','W2':'ɯ̀ː','W3':'ɯ̂ː','W4':'ɯ́ː','W5':'ɯ̌ː',
    'e1':'e', 'e2':'è', 'e3':'ê', 'e4':'é', 'e5':'ě',
    'E1':'eː','E2':'èː','E3':'êː','E4':'éː','E5':'ěː',
    'ɛ1':'ɛ', 'ɛ2':'ɛ̀', 'ɛ3':'ɛ̂', 'ɛ4':'ɛ́', 'ɛ5':'ɛ̌',
    'Y1':'ɛː','Y2':'ɛ̀ː','Y3':'ɛ̂ː','Y4':'ɛ́ː','Y5':'ɛ̌ː',
    'o1':'o', 'o2':'ò', 'o3':'ô', 'o4':'ó', 'o5':'ǒ',
    'O1':'oː','O2':'òː','O3':'ôː','O4':'óː','O5':'ǒː',
    'ɔ1':'ɔ', 'ɔ2':'ɔ̀', 'ɔ3':'ɔ̂', 'ɔ4':'ɔ́', 'ɔ5':'ɔ̌',
    'X1':'ɔː','X2':'ɔ̀ː','X3':'ɔ̂ː','X4':'ɔ́ː','X5':'ɔ̌ː',
    'ə1':'ə', 'ə2':'ə̀', 'ə3':'ə̂', 'ə4':'ə́', 'ə5':'ə̌',
    'Z1':'əː','Z2':'ə̀ː','Z3':'ə̂ː','Z4':'ə́ː','Z5':'ə̌ː',
    'J1':'ia','J2':'ìa','J3':'îa','J4':'ía','J5':'ǐa',
    'R1':'ɯa','R2':'ɯ̀a','R3':'ɯ̂a','R4':'ɯ́a','R5':'ɯ̌a',
    'V1':'ua','V2':'ùa','V3':'ûa','V4':'úa','V5':'ǔa',
    'b':'b',  'p':'p',   'P':'pʰ', 'm':'m',  'f':'f',
    'd':'d',  't':'t',   'T':'tʰ', 'n':'n',  's':'s',
    'r':'r',  'l':'l',   'c':'tɕ', 'C':'tɕʰ',
    'k':'k',  'K':'kʰ',  'ŋ':'ŋ',
    'w':'w',  'j':'j',   'h':'h',  'ʔ':'ʔ',
    '.':'.',   '-':''
}

PHONE2HAAS = {
    'a1':'a', 'a2':'à', 'a3':'â', 'a4':'á', 'a5':'ǎ',
    'A1':'aa','A2':'àa','A3':'âa','A4':'áa','A5':'ǎa',
    'i1':'i', 'i2':'ì', 'i3':'î', 'i4':'í', 'i5':'ǐ',
    'I1':'ii','I2':'ìi','I3':'îi','I4':'íi','I5':'ǐi',
    'u1':'u', 'u2':'ù', 'u3':'û', 'u4':'ú', 'u5':'ǔ',
    'U1':'uu','U2':'ùu','U3':'ûu','U4':'úu','U5':'ǔu',
    'ɯ1':'ɯ', 'ɯ2':'ɯ̀', 'ɯ3':'ɯ̂', 'ɯ4':'ɯ́', 'ɯ5':'ɯ̌',
    'W1':'ɯɯ','W2':'ɯ̀ɯ','W3':'ɯ̂ɯ','W4':'ɯ́ɯ','W5':'ɯ̌ɯ',
    'e1':'e', 'e2':'è', 'e3':'ê', 'e4':'é', 'e5':'ě',
    'E1':'ee','E2':'èe','E3':'êe','E4':'ée','E5':'ěe',
    'ɛ1':'ɛ', 'ɛ2':'ɛ̀', 'ɛ3':'ɛ̂', 'ɛ4':'ɛ́', 'ɛ5':'ɛ̌',
    'Y1':'ɛɛ','Y2':'ɛ̀ɛ','Y3':'ɛ̂ɛ','Y4':'ɛ́ɛ','Y5':'ɛ̌ɛ',
    'o1':'o', 'o2':'ò', 'o3':'ô', 'o4':'ó', 'o5':'ǒ',
    'O1':'oo','O2':'òo','O3':'ôo','O4':'óo','O5':'ǒo',
    'ɔ1':'ɔ', 'ɔ2':'ɔ̀', 'ɔ3':'ɔ̂', 'ɔ4':'ɔ́', 'ɔ5':'ɔ̌',
    'X1':'ɔɔ','X2':'ɔ̀ɔ','X3':'ɔ̂ɔ','X4':'ɔ́ɔ','X5':'ɔ̌ɔ',
    'ə1':'ə', 'ə2':'ə̀', 'ə3':'ə̂', 'ə4':'ə́', 'ə5':'ə̌',
    'Z1':'əə','Z2':'ə̀ə','Z3':'ə̂ə','Z4':'ə́ə','Z5':'ə̌ə',
    'J1':'ia','J2':'ìa','J3':'îa','J4':'ía','J5':'ǐa',
    'R1':'ɯa','R2':'ɯ̀a','R3':'ɯ̂a','R4':'ɯ́a','R5':'ɯ̌a',
    'V1':'ua','V2':'ùa','V3':'ûa','V4':'úa','V5':'ǔa',
    'b':'b',  'p':'p',   'P':'pʰ', 'm':'m',  'f':'f',
    'd':'d',  't':'t',   'T':'tʰ', 'n':'n',  's':'s',
    'r':'r',  'l':'l',   'c':'c', 'C':'cʰ',
    'k':'k',  'K':'kʰ',  'ŋ':'ŋ',
    'w':'w',  'j':'y',   'h':'h',  'ʔ':'ʔ',
    '.':'.',   '-':''
}