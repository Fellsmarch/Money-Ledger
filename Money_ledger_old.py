"""Calculates how much each person in a group owes each other"""
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
        
    def add_money_spent(self, amount):
        """Adds money spent to the person's ledger"""
        self.money_spent += amount
        self.money_owed = (self.money_spent / 5) * 4 #These numbers are per group, too lazy to move them 
        
    def __str__(self):
        """Returns the formatted string that represents this person"""
        name = self.name
        money_spent = self.money_spent
        template = "{0} has spent ${1} on the group so they are owed ${2}"
        self.money_owed = (money_spent / 5) * 4 #These numbers are per group, too lazy to move them
        return template.format(name, money_spent, self.money_owed)
    

def get_num_in_group():
    """Gets the number of people in the money ledger group"""
    input_successful = False
    while not input_successful: #Ensures the user unit is valid
        group_num = input("How many are in your group? ")
        try: #Could replace
            group_num = int(group_num)
            return group_num
        except:
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
    """Gets a name from the user"""
    input_successful = False
    suffix = get_num_suffix(num)
    template = "What is the {0}{1} person's name? "
    name = input(template.format(num, suffix))
    return name

    
def create_group_list():
    """Creates the list of people in the group"""
    group_num = get_num_in_group()
    group = []
    for i in range(group_num):
        name = get_name(i+1)
        group.append(Person(name))
    return group
    
    
def get_amount_spent(group):
    """For each person asks the user for their amount spent on the group"""
    template = "How much has {0} spent? "
    for person in group:
        input_successful = False
        while not input_successful:
            money_spent = input(template.format(person.name))
            try:
                money_spent = int(money_spent)
                person.add_money_spent(money_spent)
                input_successful = True
            except:
                print("Input is not a integer, please try again")          
        
def print_ledger(group):
    """Prints the final ledger"""
    for receiver in group:
        for sender in group:
            if not receiver == sender:
                receiver_owes = sender.money_owed / 4 #Again could replace this using group_num - 1
                #print(receiver.name + " owes " + sender.name + " " + str(receiver_owes) + "           **DEBUG**") ###Debug
                sender_owes = receiver.money_owed / 4  #  ^^^^^^^^^^
                #print(sender.name + " owes " + receiver.name + " " + str(sender_owes) + "            **DEBUG**") ###Debug
                #if receiver_owes < sender_owes:
                sender_pays = receiver_owes - sender_owes
                #print(sender.name + " pays " + str(sender_pays) + "            **DEBUG**") ###Debug
                if sender_pays > 0:
                    template = "{0} should pay {1} ${2:.1f}"
                    print(template.format(receiver.name, sender.name, sender_pays))
                    
                
    
def main():
    group_list = create_group_list()
    get_amount_spent(group_list)
    #for person in group_list: ###Debug
    #    print(person) ###Debug
    print_ledger(group_list)
        
    
    
main()
