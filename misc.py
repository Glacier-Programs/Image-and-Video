'''
miscelaneous functions, classes, constants used throughtout project
'''
from typing import Any

_lists_cycling = [] # to store what lists are being cycled. Allows for multiple lists using cycle()
_indices_cycling = [] # to store the current index of each list being cycled
def cycle(list: list[Any], amnt: int = 1) -> Any:
    '''Function to cycle through the values of a list'''
    global _lists_cycling, _indices_cycling
    if not list in _lists_cycling:
        _lists_cycling.append(list)
        _indices_cycling.append(-1) # start at negative one so that first value return is index 0
    # since each list and it's counter both have the same index, 
    # finding one the list gives the one of its counter
    cur_index = _indices_cycling[ _lists_cycling.index(list) ]
    # modulus here just prevents going over the maximum index
    new_index = (cur_index + amnt) % len(list)
    _indices_cycling[ _lists_cycling.index(list) ] = new_index
    return list[new_index]

def reset_cycle(list: list[Any]) -> None:
    '''Function to reset the cycle value of a list'''
    global _lists_cycling, _indices_cycling
    if not list in _lists_cycling: return
    spot = _lists_cycling.index(list)
    _lists_cycling.pop(spot)
    _indices_cycling.pop(spot)
