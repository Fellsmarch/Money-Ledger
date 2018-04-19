import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Scanner;

public class MoneyLedger
	{
		ArrayList<Person> group = new ArrayList<Person>();
		private int numInGroup;
		
		public int getValidInputNum(int minNum) {
			Scanner scanner = new Scanner(System.in);
			int toReturn = 0; //Have to instantiate to something since method has to return an int
			boolean inputGood = false;
			while (!inputGood) {
					String userInput = scanner.next();
					try {
						int userChoice = Integer.parseInt(userInput); //Checks if input is an int
						if (userChoice >= minNum) {
							inputGood = true;
							toReturn = userChoice;
						}else {
							System.out.println("Input must be " + minNum + " or more!");
						}
					} catch (NumberFormatException e) {
						System.out.println("Input was not an integer, please try again.");
				}
			}
			System.out.println(".\n.\n.");
			//scanner.close(); --> This closes the scanner for the whole program, not just for the method
			return toReturn; //This is only done this way since the method needs to return an int
		}
		
		public void createGroup() {
			System.out.println("How many are in your group?");
			numInGroup = getValidInputNum(1);
			for (int i = 0; i < numInGroup; i++) {
				System.out.println("What is the " + (i+1) + getSuffix(i+1) + " person's name?");
				String newName = getName();
				group.add(new Person(newName));
			}
		}
		
		public String getName() {
			Scanner scanner = new Scanner(System.in);
			return scanner.next();
		}
		
		public String getSuffix(int num) {
			num %= 100;
			if (num == 11 || num == 12 || num == 13) {return "th";}
			else {
				num %= 10;
				if(num == 1) {return "st";}
				else if (num == 2) {return "nd";}
				else if (num == 3) {return "rd";}
				else {return "th";}
			}
		}
		
		public void getAmountSpent() {
			for (Person person : group) {
				System.out.println("How much money has " + person.getName() + " spent on the group?");
				int moneySpent = getValidInputNum(0);
				person.addMoneySpent(moneySpent, numInGroup);
			}
		}
		
		public void printLedger() {
			for (Person receiver : group) {
				for (Person sender : group) {
					if (receiver != sender) {
						double receiverOwes = sender.getMoneyOwed() / (numInGroup - 1);
						double senderOwes = receiver.getMoneyOwed() / (numInGroup - 1);
						double senderPays = receiverOwes - senderOwes;
						if (senderPays > 0) {
							NumberFormat formatter = new DecimalFormat("#0.00");
							String output = receiver.getName() + " should pay " + sender.getName() + " $" + formatter.format(senderPays);
							System.out.println(output);
						}
					}
				}
			}
		}
		
		public static void main(String[] args)
			{
				MoneyLedger moneyLedger = new MoneyLedger();
				moneyLedger.createGroup();
				moneyLedger.getAmountSpent();
				moneyLedger.printLedger();

			}
	}
		

