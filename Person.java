public class Person
	//This class could b
		{
			private String name;
			private double moneySpent = 0;
			private double moneyOwed = 0;
			
			public Person(String newName) {
				name = newName;
			}
			
			public void addMoneySpent(double amount, int groupSize) {
				moneySpent += amount;
				calculateMoneyOwed(groupSize);
			}
			
			public void calculateMoneyOwed(int groupSize) {
				moneyOwed = (moneySpent / groupSize) * (groupSize - 1);
			}
			
			public String toString() {
				return name + " has spent $" + moneySpent + " on the group so they are owed $" + moneyOwed;
			}
			
			public double getMoneySpent() {return moneySpent;}
			public double getMoneyOwed() {return moneyOwed;}
			public String getName() {return name;}
			
		}
