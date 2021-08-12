import random


def sample_without_replacement(mylist: list):
    """
    Pick a random name from a list
    return the name and the list without that name

    Args:
        mylist (list): list of items to pick from

    Returns:
        name (str): random item from the list
        mylist_copy(list): mylist with name removed
    """

    mylist_copy = mylist.copy()

    if len(mylist_copy) == 0:
        return None

    name = random.choice(mylist_copy)

    mylist_copy.remove(name)

    return name, mylist_copy
