import csv
from random import *
global letter_count 

letter_count = 0


class Letter:
    # Each letter has a lowercase character, an uppercase character, and
    # identifiers as vowel or consonant.
    def __init__(self, lowerchar, upperchar, is_vowel, is_consonant):
        global letter_count
        self.upperchar = upperchar
        self.lowerchar = lowerchar
        self.is_vowel = is_vowel
        self.is_consonant = is_consonant
        self.num = letter_count
        letter_count += 1


# Define the alphabet.
global alphabet
alphabet = [Letter('a', 'A', True, False),
            Letter('b', 'B', False, True),
            Letter('c', 'C', False, True),
            Letter('d', 'D', False, True),
            Letter('e', 'E', True, False),
            Letter('f', 'F', False, True),
            Letter('g', 'G', False, True),
            Letter('h', 'H', False, True),
            Letter('i', 'I', True, False),
            Letter('j', 'J', False, True),
            Letter('k', 'K', False, True),
            Letter('l', 'L', False, True),
            Letter('m', 'M', False, True),
            Letter('n', 'N', False, True),
            Letter('o', 'O', True, False),
            Letter('p', 'P', False, True),
            Letter('q', 'Q', False, True),
            Letter('r', 'R', False, True),
            Letter('s', 'S', False, True),
            Letter('t', 'T', False, True),
            Letter('u', 'U', True, False),
            Letter('v', 'V', False, True),
            Letter('w', 'W', False, True),
            Letter('x', 'X', False, True),
            Letter('y', 'Y', True, True),
            Letter('z', 'Z', False, True)
            ]


class Prob:
    """Read in Probability Matrix"""
    def __init__(self, race):
        try:
            self.prob_matrix = self.get_matrix(f'{race}.csv')
        except FileNotFoundError:
            self.create_initial_state(race)
            self.prob_matrix = self.get_matrix(f'{race}.csv')
        self.normalize()

    def create_initial_state(self, race):
        prob_matrix = self.get_matrix('default prob.csv')

        # Read list of pre-generated names. Names should be stored one per line in file.
        file_name = f'{race} names.csv'
        with open(file_name, newline='') as csvfile:
            name_reader = csv.reader(csvfile, delimiter=',', quotechar='|')  # Record file contents.
            for names in name_reader:  # Loop over names in list.
                name = names[0]
                # Loop over letters in the current name.
                for i in range(0, len(name) - 1):
                    letter1 = name[i]
                    letter2 = name[i + 1]
                    num1 = 0
                    num2 = 0
                    for i in range(0, len(alphabet)):
                        if letter1 == alphabet[i].lowerchar or letter1 == alphabet[i].upperchar:
                            num1 = alphabet[i].num
                        if letter2 == alphabet[i].lowerchar or letter2 == alphabet[i].upperchar:
                            num2 = alphabet[i].num
                    # Add one to the number of times letter number i is followed by letter number i+1.
                    prob_matrix[num1][num2] += 1

        # Normalize the probability matrix.
        prob = self.normalize(prob_matrix)

        # Write probability matrix to file. This file will be read by the name generator.
        file_name = f'{race}.csv'
        with open(file_name, 'w', newline='') as csvfile:
            prob_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(alphabet)):
                prob_writer.writerow(prob[i])

    @staticmethod
    def get_matrix(file_name):
        probability = []
        with open(file_name, newline='') as csvfile:
            prob_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in prob_reader:
                probability.append([])
                for num in row:
                    probability[len(probability) - 1].append(float(num))
        return probability

    def normalize(self, matrix=None):
        global alphabet
        if matrix is not None:
            new_prob = matrix
            ref_matrix = matrix
        else:
            new_prob = self.prob_matrix
            ref_matrix = self.prob_matrix
        for i in range(0, len(alphabet)):
            total = 0
            for j in range(0, len(alphabet)):
                total += ref_matrix[i][j]
            if total > 0:
                for j in range(0, len(alphabet)):
                    new_prob[i][j] = ref_matrix[i][j] / total
        return new_prob


class NameGenerator:

    race = 'elf'
    prob = Prob(race)

    def __init__(self, race):
        self.race = race
        self.prob = Prob(race)

    @staticmethod
    def uniform(x1, x2):
        # Generate a random floating-point number between x1 and x2.
        r = x1 + random()*(x2-x1)
        return r

    @staticmethod
    def rand_int(x1, x2):
        # Generate a random integer number between x1 and x2.
        r = int( int(x1) + random()*(int(x2)-int(x1)) )
        return r

    def make_name(self):
        # Determine name length.
        lmin = 3  # Minimum length.
        lmax = 10  # Maximum length.
        name_length = self.rand_int(lmin, lmax)

        # Initialize string.
        my_name = ""
        my_name_nums = []

        prev_vowel = False  # Was the previous letter a vowel?
        prev_consonant = False  # Was the previous letter a consonant?
        prev2_vowel = False  # Were the previous 2 letters vowels?
        prev2_consonant = False  # Were the previous 2 letters consonants?
        prev_num = 0
        # Generate letters for name.
        for i in range(0, name_length):
            if i == 0:
                a = alphabet[self.rand_int(0, 25)]
                my_name = my_name + a.upperchar
            else:
                a = self.get_letter(prev_num, prev2_vowel, prev2_consonant)
                my_name = my_name + a.lowerchar
            prev2_vowel = (a.is_vowel and prev_vowel)
            prev2_consonant = (a.is_consonant and prev_consonant)
            prev_vowel = a.is_vowel
            prev_consonant = a.is_consonant
            prev_num = a.num
            my_name_nums.append(a.num)
        return [my_name,my_name_nums]

    def get_letter(self, prev_num,need_consonant,need_vowel):
        global alphabet
        # Generate a random letter.
        done = False
        while not done:
            # a = alphabet[rand_int(0,25)]
            a = self.pick_letter(prev_num)
            if (need_consonant and a.is_vowel) or (need_vowel and a.is_consonant):
                done = False
            else:
                done = True
        return a

    def pick_letter(self, i):
        global alphabet
        r = random()
        total = 0
        for j in range(0, len(alphabet)):
            total += self.prob.prob_matrix[i][j]
            if r <= total or j == len(alphabet):
                return alphabet[j]
        print("problem!")
        return alphabet(25)

    def train(self, count):
        for num in range(count):
            name1 = self.make_name()
            print(name1[0])

            input_string = f"Was this a good {self.race} name? y/n"
            good = input(input_string)
            if good == "y":
                for i in range(0, len(name1[1])-1):
                    self.prob.prob_matrix[name1[1][i]][name1[1][i+1]] *= 1.01
            if good == "n":
                for i in range(0, len(name1[1])-1):
                    self.prob.prob_matrix[name1[1][i]][name1[1][i+1]] *= 0.99

            prob = self.prob.normalize()

            with open(f'{self.race}.csv', 'w', newline='') as csvfile:
                prob_writer = csv.writer(csvfile, delimiter=',',
                                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, len(alphabet)):
                    prob_writer.writerow(prob[i])
        return 0