import random
from string import digits

VISA_PREFIXES = ('4539', '4556', '4916', '4532', '4929', '40240071', '4486', '4716', '4')
MASTERCARD_PREFIXES = ('51', '52', '53', '54', '55')


def gen_cc_number(prefixes=VISA_PREFIXES + MASTERCARD_PREFIXES, length=16):
    cc_number = random.choice(prefixes)
    cc_number += ''.join(random.choices(digits, k=length - len(cc_number) - 1))

    cc_sum = 0
    for i, digit in enumerate(reversed(cc_number)):
        digit = int(digit)
        if i % 2 == 0:
            digit *= 2
            if digit >= 10:
                digit = sum(divmod(digit, 10))
        cc_sum += digit

    check_digit = (10 - cc_sum % 10) % 10
    cc_number += f"{check_digit}"

    return cc_number


NAMES_DATA = dict(
    first_names='../data/first_names.csv',
    last_names='../data/first_names.csv',
)


def load_names(file_path):
    names, weights = [], [0]
    with open(file_path) as file:
        for line in file.readlines():
            name, weight = line.split(',')
            names.append(name)
            weights.append(weights[-1] + float(weight))

    return dict(population=tuple(names), cum_weights=tuple(weights[1:]))
