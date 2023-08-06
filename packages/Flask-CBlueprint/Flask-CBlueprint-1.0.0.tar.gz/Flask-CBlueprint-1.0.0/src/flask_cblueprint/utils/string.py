import re

def camel_to_snake(x):
    """
    It replaces all instances of a capital letter followed by a lowercase letter with an underscore
    followed by the lowercase letter
    
    :param x: The string to be converted
    :return: A list of the keys of the dictionary.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', x)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(word):
    """
    It takes a string, splits it on the underscore, capitalizes the first letter of each word, and joins
    them back together
    
    :param word: The word to convert
    :return: a string that is the result of joining the capitalized version of each word in the list.
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))