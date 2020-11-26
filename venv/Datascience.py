# Exercise 1 WQU DATASCIENCE
# Visit world quanta university site on google to ascertain the question asked
import math


def mersenne_number(p):
    """(2^P - 1) IS A MERSENNE NUMBER, WHERE 'p', IS AN EXPONENT"""
    val_to_raise_exponent = 2
    mer_num = ((val_to_raise_exponent ** p) - 1)
    return mer_num


def is_prime(number):
    """THIS FUNCTION CHECKS THE PRIME NUMBERS AND SORT THEM OUT"""
    if number == 1:
        return False
    for factor in range(2, number):
        if (number % factor) == 0:
            if (number / factor) > 1.0:
                return False
    return number


def get_primes(n_start, n_end):
    """THIS FUNCTION SHOULD TAKE THE OUTPUT OF is_prime AND MAKE OUT A LIST"""
    holder = []  # An empty to hold the values
    for number in range(n_start, n_end):
        if is_prime(number):
            holder.append(number)
    return holder


# EXERCISE 2:
def lucas_lehmer(p):
    count = 3
    initial = 4
    final2 = [initial]
    while count <= p:
        final = (initial ** 2 - 2) % mersenne_number(p)
        final2.append(final)
        initial = final
        count += 1
    return final2


# Exercise 3: mersenne_primes
def ll_prime(p):
    get_prime_holder = get_primes(3, p)
    lucas_lehmer_holder = []
    v = []
    # This get_prime will return for me a list of prime numbers
    for val in get_prime_holder:
        lucas_lehmer_holder.append(lucas_lehmer(val))
    for val_x in lucas_lehmer_holder:
        i = lucas_lehmer_holder.index(val_x)
        # These i holds the index position for the list(val_x) inside the list(lucas_lehmer_holder)
        if val_x[-1] == 0:
            v += [(get_prime_holder[i], 1)]
        elif val_x[-1] != 0:

            v += [(get_prime_holder[i], 0)]
    return v


# Exercise 4: Optimize is_prime
def is_prime_fast(number):
    is_prime_fast_holder = []
    if number == 1:
        return False
        # Here i am trying to catch all other even numbers
    if number % 2 == 0:
        is_prime_fast_holder = check_first_optimize(number)
    elif number % 2 != 0:
        is_prime_fast_holder = check_2_optimize(number)
    return is_prime_fast_holder


def check_first_optimize(number):
    """THIS FUNCTION TAKES CARE OF EVEN NUMBERS"""
    if number % 2 == 0 and number != 2:
        return False
    elif number % 2 == 0 and number == 2:
        return number


def check_2_optimize(number):
    """THIS FUNCTION TAKES CARE OF ODD NUMBERS AND THEIR FACTORS"""
    holder = []
    for num in range(3, number, 2):  # Checking for the first condition when n is prime
        if num <= math.sqrt(number):
            holder.append(num)
    for val in holder:
        if number % val == 0:
            if number / val > 1.0: return False

    return number


# Exercise 5: sieve
def list_true(n):
    boolean_list_holder = []
    for boo in range(n + 1):
        if boo <= 1:
            boolean_list_holder.append(False)
        else:
            boolean_list_holder.append(True)
    return boolean_list_holder


def mark_false(bool_list, p):
    i = 2
    while i * p < len(bool_list):
        bool_list[i * p] = False
        i += 1
    return bool_list


def find_next(bool_list, p):
    my_list = enumerate(bool_list[p + 1:], start=p + 1)
    for i, y in my_list:
        if y:
            return i
    return None


def prime_from_list(bool_list):
    states = bool_list
    holder = []
    h = enumerate(states)
    for y, z in h:
        if z:
            holder.append(y)
    return holder


def sieve(n):
    bool_list = list_true(n)
    p = 2
    while p is not None:
        bool_list = mark_false(bool_list, p)
        p = find_next(bool_list, p)
    return prime_from_list(bool_list)


print(get_primes(1, 2000))
