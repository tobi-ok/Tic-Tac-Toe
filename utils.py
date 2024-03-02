def recursive_input(m, l):
    new_input = input(m).upper()

    if new_input in l:
        return l[new_input]
    else:
        try:
            new_input = int(new_input)

            for i in l:
                if i == new_input:
                    return i
                
            print('Error - Invalid input')
            return recursive_input(m, l)
        except (ValueError, IndexError):
            print('Error - Invalid input')
            return recursive_input(m, l)