import re

# This file contains the actual functionality of the processor
def processor(input, lang, a, e, o, s, sri, n, jn, m):
    if lang == 'kn':
        output = input
        if a:
            output = re.sub('[âàá]', 'ā', output)
        if e:
            output = re.sub('é', 'ē', output)
        if o:
            output = re.sub('[ôó]', 'ō', output)
        if s:
            output = re.sub('$', 'ś', output)
            output = re.sub('S\'', 'Ś', output)
        if sri:
            output = re.sub('[sS$géē]ri', 'śrī', output)
        if n:
            output = re.sub('n([kg])', r'ṅ\1', output)

            output = re.sub('n([cj])', r'ñ\1', output)

            output = re.sub('n([ṭḍ])', r'ṇ\1', output)
        if jn:
            output = re.sub('fi([cj])', r'ñ\1', output)
        if m:
            output = re.sub('m([-\s+])([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ])', r'ṁ\1\2', output)
        return output
    else:
        return None
