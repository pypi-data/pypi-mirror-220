
ORG_MODULUS = 11
CREDITCODE_LENGTH = 18
CREDITCODE_MODULUS = 31

SOCIAL_CREDIT_CHECK_CODE_DICT = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24, 'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30}

CREDIT_WEIGHT_FACTOR = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]


def is_creditcode(code):
    ''' 判断是否是统一社会信用码 '''

    return verify(code, CREDITCODE_MODULUS, SOCIAL_CREDIT_CHECK_CODE_DICT, CREDIT_WEIGHT_FACTOR, CREDITCODE_LENGTH)


def verify(code, modulus, code_dict, weight, length):
    ''' 根据不同编辑映射校验合法性  '''

    #字符长度判断
    if len(code) != length: return False


    #判断字符串是否异常
    for char in code:
        if char not in code_dict: return False

    #比较校验码是否相等
    check_code = code[-1]
    sum_code = sum([code_dict[char] * weight[ind] for ind, char in enumerate(code[:-1])])

    char_val = modulus - (sum_code % modulus)
    char_val = 0 if char_val == modulus else char_val

    if ORG_MODULUS == modulus and char_val == 10: char_val = 33

    return code_dict[check_code] == char_val
     

if __name__ == '__main__':
    print(is_creditcode('91110105MA00BAAY6N'))
    print(is_creditcode('911101050BAAY6N'))
