from profanityfilter import ProfanityFilter
from profanity_check import predict

pf = ProfanityFilter()


def checkprofanity():
    with open("data/input.sql") as file_in:
        profanitycount = 0
        linecount = 0

        # start iterating through the lines in the input text file
        for line in file_in:
            linecount += 1

            # use the predict() function from profanity-check first.
            # it's much faster than ProfanityFilter.is_profane().
            # however, it generates a lot of false positives.  Use ProfanityFilter
            # as a second test.
            #
            # note:  using both is considerably faster than relying only
            # on ProfanityFilter.is_profane, which is prohibitively slow
            # to use without filtering out most of the lines with predict().
            if predict([line])[0] and pf.is_profane(line):
                profanitycount = profanitycount + 1

                profane_words = [
                    word for word in line.split() if predict([word])[0] and pf.is_profane(word)
                ]

                with open('output.txt', 'a') as file:
                    file.write(line)
                    file.write('\n')
                    file.write(','.join(profane_words))
                    file.write('\n')
                    file.write('\n')

            if linecount % 1000 == 0:
                print(
                    f"lines checked: {linecount} lines with profanity(so far): {profanitycount}")


if __name__ == '__main__':
    checkprofanity()
