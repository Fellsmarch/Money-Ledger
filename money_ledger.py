from sys import exit

"""This program uses user input to create a group's money ledger and calculate
   how much each person in the group owes each other person.

   Author: Harrion Cook
   Version: 1.1 April 2019
   """


class Person:
    """Defines the Person class.
    Data attributes: name of type str
                     money_spent of type float
                     money_owed of type float

    Methods: add_money_spent
             __str__()
    """

    def __init__(self, name):
        """Person constructor"""

        self.name = name
        self.money_spent = 0
        self.money_owed = 0

    def add_money_spent(self, amount, group_size):
        """Adds money spent on the group to the person's ledger

         Keyword arguments:
         self -- this person class object
         amount -- the amount of money to add
         group_size -- the size of the group of people
        """

        self.money_spent += amount

        # Takes off the portion of money that would be owed to themselves
        self.money_owed = (self.money_spent / group_size) * (group_size - 1)


def get_input(question, comparator, err_msg="Invalid input, please try again"):
    """Gets input from the user and ensures that the input is valid.

    Keyword arguments:
    question -- the question to ask the user (the text of the prompt)
    comparator -- the function to use to check if the user's input is valid
    err_msg -- the error message to display if the input is not valid
        (default "Invalid input, please try again")
    """

    user_input = None
    while True:
        user_input = input(question)
        if user_input == "q".lower():
            print("\nThank you for using Money Ledger")
            exit(0)
        else:
            input_good = comparator(user_input)
            if not input_good:
                print("ERROR: " + err_msg + "\n")
            else:
                return user_input


def get_yes_no_answer(question):
    """Gets a yes/no (y/n) answer from the user to a given question

    Keyword arguments:
    question -- the question to ask the user(the text of the prompt)
    """

    acceptable_input = ["y", "yes", "n", "no"]
    def comparator(user_input): return user_input.lower() in acceptable_input

    return get_input(question, comparator).lower()


def get_num_in_group():
    """Asks the user how many people are in their group and returns that number.
    """

    question = "How many are in your group? "
    error_message = "Input is not an integer, please try again"
    def comparator(user_input): return user_input.isdigit()

    return int(get_input(question, comparator, error_message))


def get_num_suffix(num):
    """Gets the correct English ordinal indicator(suffix) for a given number.
    """

    num = num % 100
    if num == 11 or num == 12 or num == 13:
        return "th"

    num = num % 10
    if num == 1:
        return "st"
    elif num == 2:
        return "nd"
    elif num == 3:
        return "rd"
    else:
        return "th"


def get_name(num):
    """Asks the user for the name of the nth member of the group and returns it.
    """

    suffix = get_num_suffix(num)

    question = "What is the {0}{1} person's name? ".format(num, suffix)
    def comparator(user_input): return len(user_input) > 0
    error_message = "Name must be at least one character"

    return get_input(question, comparator, error_message)


def create_group_list():
    """Constructs the list of people in the group by asking the user how many
    people there are and then what each of those people's names are, """

    group_num = get_num_in_group()
    group = []
    for person_num in range(group_num):
        name = get_name(person_num + 1)
        group.append(Person(name))

    print("\n----------------------------------------------")
    return group


def get_amount_spent(group, currency):
    """For each person in the group, asks the user for that person's
    amount spent for the group.

    Keyword arguments:
    group - - the group of people(as a list)
    currency - - the user's preferred currency symbol
    """

    template = "How much has {0} spent? {1}"
    error_message = "Input must be a non-negative number, please try again"

    def comparator(user_input):
        try:
            num = float(user_input)
            return num >= 0
        except ValueError:
            return False

    group_size = len(group)
    total_money_spent = 0

    for person in group:
        question = template.format(person.name, currency)
        money_spent = float(get_input(question, comparator, error_message))
        person.add_money_spent(money_spent, group_size)
        total_money_spent += money_spent

    return total_money_spent


def print_ledger(total_money_spent, group, currency):
    """Prints how much each person needs to pay the people they owe money.

    Keyword arguments:
    total_money_spent - - the total amount of money the group money_spent
    group - - the group of people(as a list)
    currency - - the user's preferred currency symbol
    """

    # The number of people in the group
    group_num = len(group)

    print("\n----------------------------------------------")
    print("Total money spent by the group: {0}{1:.2f}\n"
          .format(currency, total_money_spent))

    # Iterates through the group one person at a time
    for receiver in group:
        # For each person iterates through the group again
        for sender in group:
            if not receiver == sender:
                # The reciever owes the sender this much money
                receiver_owes = sender.money_owed / (group_num - 1)
                # The sender owes the reciever this much money
                sender_owes = receiver.money_owed / (group_num - 1)
                # Ensures that money will not transfer between two people more
                # than once
                sender_pays = receiver_owes - sender_owes

                """Some sender_pays values will be negative, this means that
                the reciever actually owes the sender. Since every pair of
                people are checked twice, if money is owed, on one of the
                checks sender_pays will be positive. This line ensures that
                only the positive value is printed."""
                if sender_pays > 0:
                    template = "{0} should pay {1} {2}{3:.2f}"
                    print(template.format(receiver.name, sender.name,
                                          currency, sender_pays))

    print()  # Adds a new line after printing all the owings


def user_requires_explanation(first_time=True):
    """Asks the user if they wants an explanation as to how the program came to
    the conclusion it did. Returns True if the user wants an explanation and
    False if they do not.
    """

    question = "Would you like {0} explanation for a person? (y/n): "
    question = question.format("an" if first_time else "another")

    user_input = get_yes_no_answer(question)

    if user_input == "y" or user_input == "yes":
        return True
    else:
        return False


def get_person_for_explanation(group):
    """Asks the user what person's ledger in the group they want explained.

    Keyword arguments:
    group - - the group of people(as a list)
    """

    question = "What person's owings would you like an explanation for? "
    error_message = "That person is not in the group, please try again"

    def comparator(person_input, return_person=False):
        for person in group:
            # Checks if the person the user input is in the list
            if person.name.lower() == person_input.strip().lower():
                if not return_person:
                    return True
                else:
                    return person
        return False

    # Calls the comparator function to find the person who the user is looking
    # for, and uses get_input to get the person's name from the user
    person = comparator(get_input(question, comparator, error_message), True)

    return person


def explain_persons_owings(explainee, group, currency):
    """Explains the given person's owings to the user by printing how the
    program came to the conclusion that it did.

    Keyword arguments:
    explainee - - the person to explain the owings of
    group - - the group of people(as a list)
    currency - - the user's preferred currency
    """

    group_size = len(group)
    name = explainee.name
    money_spent = explainee.money_spent
    money_owed = explainee.money_owed
    money_owed_individual = money_owed / (group_size - 1)

    print("\n----------------------------------------------")
    print("{0} spent {1}{2} on the group".format(name, currency, money_spent))
    print("Hence {0} \"owe themselves\" {1}{2:.2f} ({1}{3:.2f} / {4} people)"
          .format(name, currency, money_spent / group_size, money_spent,
                  group_size))
    print("The rest of the group as a whole owes {0} {1}{2:.2f}"
          .format(name, currency, money_owed))
    print("So each person in the group owes {0} {1}{2:.2f}"
          .format(name, currency, money_owed_individual))

    for person in group:
        if person == explainee:
            continue
        print()
        person_owed = person.money_owed / (group_size - 1)
        explainee_final_owing = person_owed - money_owed_individual
        print(name + " owes {0} {1}{2:.2f}".format(person.name, currency,
                                                   person_owed))
        print(("Taking off the amount {0} owes {1} ({2}{3:.2f}), {1} now " +
               "owes {0} {2}{4:.2f}")  # Parenthesis so it formats whole string
              .format(person.name, name, currency,
                      money_owed_individual, explainee_final_owing))

        if explainee_final_owing < 0:
            print(("Since {0} now owes {1} a negative amount of money " +
                   "({2}{3:.2f}), {1} actually owes {0} {2}{4:.2f}")
                  .format(name, person.name, currency, explainee_final_owing,
                          abs(explainee_final_owing)))


def get_currency():
    """Gets the user's desired currency"""

    question = "Please input your desired currency symbol: "
    def comparator(user_input): return len(user_input) == 1
    err_msg = "Please input only a single character for the currency symbol"

    return get_input(question, comparator, err_msg)


def run_program_again():
    """Checks if the user would like to run the program again"""

    question = "Would you like to run the program again? (y/n): "
    user_input = get_yes_no_answer(question)

    if user_input == "y" or user_input == "yes":
        main()
    else:
        print("\nThank you for using Money Ledger")


def main():
    """The main function"""

    print("Welcome to Money Ledger! Press q to exit at any time\n")

    # Run the core of the program, asking user for information and printing
    # the ledger
    currency = get_currency()
    group_list = create_group_list()
    total_money_spent = get_amount_spent(group_list, currency)
    print_ledger(total_money_spent, group_list, currency)

    # After core has run, ask user if they need an explanation, or multiple
    explanation = user_requires_explanation()
    while explanation:
        person = get_person_for_explanation(group_list)
        explain_persons_owings(person, group_list, currency)
        explanation = user_requires_explanation(False)

    # Ask the user if they would like to run the program again
    run_program_again()
    exit(0)


if __name__ == "__main__":
    main()
