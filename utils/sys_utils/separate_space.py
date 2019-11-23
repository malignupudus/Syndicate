def separate(string, index=4):

    index_ = 0
    new_string = ''

    for _ in string:

        if (index_ == index):

            index_ = 0
            new_string += ' {}'.format(_)

        else:

            new_string += _

        index_ += 1

    return(new_string)
