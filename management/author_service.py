# 1. Defaults
# 2. Docs

def process_age(age=None) -> bool:
    """
    Process author age

    :param int age: Author age
    :return: True - if author is below 30 otherwise False
    :rtype bool
    """

    if age is None and not isinstance(age, int):
        return False

    if int(age) < 30:
        return True

    return False
