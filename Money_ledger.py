"""This program uses user input to create a group's money ledger and calculate
   how much each person in the group owes each other person."""

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
        
    def add_money_spent(self, amount, group_size): #Need a place to store group_size for this method
        """Adds money spent to the person's ledger"""
        self.money_spent += amount
        self.money_owed = (self.money_spent / group_size) * (group_size - 1) #Takes off the portion of money that would be owed to themselves
        
    def __str__(self):
        """Returns the formatted string that represents this person"""
        name = self.name
        money_spent = self.money_spent
        template = "{0} has spent ${1} on the group so they are owed ${2}"
        return template.format(name, money_spent, self.money_owed)
    

def get_num_in_group():
    """Gets from the user the number of people in the money ledger group"""
    input_successful = False
    while not input_successful: #Ensures the user unit is valid (an Int)
        group_num = input("How many are in your group? ")
        try:
            group_num = int(group_num)
            return group_num
        except ValueError:
            print("Input is not a integer, please try again")    
        
        
def get_num_suffix(i):
    """Gets the correct English suffix for a given number"""
    if i == 11 or i == 12 or i == 13:
        return "th"
    i = i % 10
    if i == 1:
        return "st"
    elif i == 2:
        return "nd"
    elif i == 3:
        return "rd"
    else:
        return "th"
    

def get_name(num):
    """Gets a name for a Person from the user"""
    input_successful = False
    suffix = get_num_suffix(num)
    template = "What is the {0}{1} person's name? "
    name = input(template.format(num, suffix))
    return name

    
def create_group_list():
    """Creates the list of people in the group"""
    group_num = get_num_in_group()
    group = []
    for person_num in range(group_num):
        name = get_name(person_num + 1)
        group.append(Person(name))
    return group
    
    
def get_amount_spent(group):
    """For each person in the group, this method asks the user for that person's
    amount spent for the group **Including** that person's share of that
    amount"""
    template = "How much has {0} spent? $"
    group_size = len(group)
    for person in group:
        input_successful = False
        while not input_successful: #Ensures that the users input is valid (an int)
            money_spent = input(template.format(person.name))
            try:
                money_spent = int(money_spent)
                person.add_money_spent(money_spent, group_size)
                input_successful = True
            except ValueError:
                print("Input is not a integer, please try again")     

        
def print_ledger(group):
    """Prints the final ledger for the group"""
    group_num = len(group) #The number of people in the group
    for receiver in group:      #Iterates through the group one person at a time
        for sender in group:    #For each person iterates through the group again
            if not receiver == sender:
                receiver_owes = sender.money_owed / (group_num - 1) #The reciever owes the sender this much money
                sender_owes = receiver.money_owed / (group_num - 1) #The sender owes the reciever this much money
                sender_pays = receiver_owes - sender_owes #Ensures that money will not transfer between two people more than once
                if sender_pays > 0: #Some sender_pays values will be negative, this means that the reciever actually owes the sender. Since every pair of people are checked twice, if money is owed, on one of the checks sender_pays will be positive. This line ensures that only the positive value is printed.
                    template = "{0} should pay {1} ${2:.1f}" #Rounds to closest 10c
                    print(template.format(receiver.name, sender.name, sender_pays))                 
                
    
def main():
    group_list = create_group_list()
    get_amount_spent(group_list)
    print_ledger(group_list)
        
    
    
main()
   
#harry = Person("Harry")
#harry.add_money_spent(100)
#liam = Person("Liam")
#liam.add_money_spent(25)
#james = Person("James")
#james.add_money_spent(25)
##print_ledger([harry, liam, james])
##print_ledger_new([harry, liam, james])
#print(james)
#print(harry)
