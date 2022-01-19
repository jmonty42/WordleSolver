import pickle

DICTIONARY_SOURCE_FILE = 'dictionary.pickle'


def main():
    with open(DICTIONARY_SOURCE_FILE, 'rb') as dictionary_source:
        dictionary = pickle.load(dictionary_source)
    first_word = dictionary["FIRST_WORD"]
    del dictionary["FIRST_WORD"]
    print("There are {0} possible words".format(len(dictionary)))
    print("Here are the 20 most common words with 5 unique letters and at least 3 vowels:")
    word = first_word
    top_n = 0
    while word != '' and top_n < 20:
        if len(dictionary[word]) == 7:  # 5 unique letters plus "prev" and "next"
            vowels = 0
            for letter in word:
                if letter in {'a', 'e', 'i', 'o', 'u'}:
                    vowels += 1
            if vowels >= 3:
                print(word)
                top_n += 1
        word = dictionary[word]["next"]
    known_positions = {}  # green clues
    known_non_positions = {}  # yellow clues
    absent_letters = set()  # grey clues (where the character isn't already in the green or yellow clues)
    absolute_counts = {}  # rare: when multiple of a character was guessed
    guess = 1
    while True:
        # collect the green clues
        try_again = True
        greens = 0
        while try_again:
            print("{0} guess:".format(ordinal(guess)))
            greens = int(input("How many letters were green? ").strip())
            if greens < 0 or greens > 5:
                print("Invalid input, try again.")
            elif greens == 5:
                print("Good job, you solved it!")
                exit()
            else:
                try_again = False
        for nth_green in range(greens):
            try_again = True
            green_letter = ''
            while try_again:
                green_letter = input("What was the {0} green letter? ".format(ordinal(nth_green+1))).strip().lower()
                if len(green_letter) != 1 or green_letter < 'a' or green_letter > 'z':
                    print("Invalid input, try again.")
                else:
                    try_again = False
            try_again = True
            position = 0
            while try_again:
                position = int(input("What 0-based position was {0} at? ".format(green_letter)).strip())
                if position < 0 or position >= 5:
                    print("Invalid input, try again.")
                else:
                    try_again = False
            if green_letter not in known_positions:
                known_positions[green_letter] = {position}
            else:
                known_positions[green_letter].add(position)
        print("green clues: " + str(known_positions))
        # collect the yellow clues
        try_again = True
        yellows = 0
        yellow_letters_this_turn = {}  # frequency of each yellow letter
        while try_again:
            yellows = int(input("How many letters were yellow? ").strip())
            if yellows < 0 or yellows >= 5:
                print("Invalid input, try again.")
            else:
                try_again = False
        for nth_yellow in range(yellows):
            try_again = True
            yellow_letter = ''
            while try_again:
                yellow_letter = input("What was the {0} yellow letter? ".format(ordinal(nth_yellow+1))).strip().lower()
                if len(yellow_letter) != 1 or yellow_letter < 'a' or yellow_letter > 'z':
                    print("Invalid input, try again.")
                else:
                    try_again = False
            if yellow_letter not in yellow_letters_this_turn:
                yellow_letters_this_turn[yellow_letter] = 0
            yellow_letters_this_turn[yellow_letter] = yellow_letters_this_turn[yellow_letter] + 1
            try_again = True
            position = 0
            while try_again:
                position = int(input("What 0-based position was {0} at? ".format(yellow_letter)).strip())
                if position < 0 or position >= 5:
                    print("Invalid input, try again.")
                else:
                    try_again = False
            if yellow_letter not in known_non_positions:
                known_non_positions[yellow_letter] = {position}
            else:
                known_non_positions[yellow_letter].add(position)
        print("yellow clues: " + str(known_non_positions))
        # collect the grey clues
        try_again = True
        greys = 0
        while try_again:
            greys = int(input("How many letters were grey? "))
            if greys < 0 or greys > 5:
                print("Invalid input, try again.")
            else:
                try_again = False
        for nth_grey in range(greys):
            try_again = True
            grey_letter = ''
            while try_again:
                grey_letter = input("What was the {0} grey letter? ".format(ordinal(nth_grey+1))).strip().lower()
                if len(grey_letter) != 1 or grey_letter < 'a' or grey_letter > 'z':
                    print("Invalid input, try again.")
                else:
                    try_again = False
            if grey_letter not in known_positions and grey_letter not in known_non_positions:
                absent_letters.add(grey_letter)
            else:
                # getting a grey letter when that same letter has already been green or yellow means that we now know
                # exactly how many times that particular letter appears in the answer
                count = 0
                if grey_letter in known_positions:
                    count += len(known_positions[grey_letter])
                if grey_letter in yellow_letters_this_turn:
                    count += yellow_letters_this_turn[grey_letter]
                absolute_counts[grey_letter] = count
        print("grey clues: " + str(absent_letters))
        print("known counts of letters: " + str(absolute_counts))
        # filter dictionary based on constraints
        word = first_word
        while word != '':
            eligible = True
            # filter known positions first
            for letter in known_positions:
                if letter not in dictionary[word]:
                    eligible = False
                    break
                if eligible:
                    for position in known_positions[letter]:
                        if position not in dictionary[word][letter]:
                            eligible = False
                            break
            # filter absent letters
            if eligible:
                for letter in absent_letters:
                    if letter in dictionary[word]:
                        eligible = False
                        break
            # filter counts
            if eligible:
                for letter in absolute_counts:
                    if letter not in dictionary[word]:
                        eligible = False
                        break
                    elif absolute_counts[letter] != len(dictionary[word][letter]):
                        eligible = False
                        break
            # filter known non positions
            if eligible:
                for letter in known_non_positions:
                    if letter not in dictionary[word]:
                        eligible = False
                        break
                    else:
                        for non_position in known_non_positions[letter]:
                            if non_position in dictionary[word][letter]:
                                eligible = False
                                break
            # remove the word from the dictionary if it's ineligible
            if not eligible:
                prev_word = dictionary[word]["prev"]
                next_word = dictionary[word]["next"]
                if prev_word != '':
                    dictionary[prev_word]["next"] = next_word
                if next_word != '':
                    dictionary[next_word]["prev"] = prev_word
                if first_word == word:
                    first_word = next_word
                del dictionary[word]
                word = next_word
            else:
                word = dictionary[word]["next"]
        # display hints for the next guess
        print("There are now {0} eligible words.".format(len(dictionary)))
        top = min(20, len(dictionary))
        if len(dictionary) > 20:
            print("Here are the 20 most common:")
        else:
            print("Here they are sorted by the most common first:")
        top_n = 0
        top_word = first_word
        show_more = True
        while show_more:
            while top_n < top and top_word != '':
                print(top_word)
                top_word = dictionary[top_word]["next"]
                top_n += 1
            if top_n < len(dictionary):
                choice = input("Would you like to see more? (y/n)").lower()
                if choice == 'y':
                    top = min(top_n+20, len(dictionary))
                    print("Ok, here's the next {0}:".format(top-top_n))
                    continue
            show_more = False
        choice = input("Would you like to continue with another guess? (y/n) ").lower()
        if choice == 'n':
            break
        else:
            guess += 1


def ordinal(num):
    num = int(num)
    if 11 <= (num % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(num % 10, 4)]
    return str(num) + suffix


if __name__ == '__main__':
    main()
