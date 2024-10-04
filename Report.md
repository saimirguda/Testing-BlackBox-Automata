## QS Assignment 3: Group 23

## Theoretical Questions

## Practical Notes

### Task 1

#### Correct Vending Machine: Matthias
The vending machine implemented by Matthias behaves correctly. It consistently manages the coin input and product selection operations:

- Accepts up to a maximum of 5 coins.
- Returns "coin_returned" when an attempt is made to insert more coins once the maximum is reached.
- Charges the correct amount for each product:
	Coke: 2 coins
	Water: 1 coin
	Peanuts: 3 coins
- Correctly updates the current balance by subtracting the cost of the dispensed item, ensuring accurate transaction management.

#### For each faulty vending machine, describe the fault

Faulty Vending Machine: Tamim

Fault Description:

- The Tamim machine incorrectly updates the balance to 6 coins when a coke is purchased, despite the price being 2 coins. This occurs even though no sixth coin is inserted. This leads to a state (s5) that theoretically represents a balance of 6 coins, which should be impossible since the machine should reject any further coins once 5 coins are inserted and should return "coin_returned" for any additional coins.

Faulty Vending Machine: Sebastian

Fault Description:

- Sebastian's vending machine incorrectly handles the balance updates after dispensing water. Assuming there is sufficient balance (minimum of 1 coin, the price of water), the machine dispenses water but fails to deduct this amount from the balance. Subsequently, it continues to dispense water without deducting further coins, essentially allowing "free" water, which is a fault in the machine's transaction management.

Faulty Vending Machine: Edi

Fault Description:

When sufficient coins are inserted and peanuts are selected, the machine charges only 1 coin instead of the required 3 coins. This leads to an incorrect pricing fault, undercharging for the item.

### Task 3

MessageBoard 0
Unexpected behavior is observed during liking and disliking of the messages.
The message points get unexpected values when multiple people like and dislike some messages.
The points system fails to correctly update when multiple likes and dislikes are performed in quick succession.
This indicates a potential issue with the concurrency handling of the points update mechanism.
Test Case: The following sequence of actions was tested to observe this behavior:

    UserA publishes a message "Hi".
    User1 likes UserA's message "Hi".
    User1 dislikes UserA's message "Hi".
    User2 likes UserA's message "Hi".
    User2 dislikes UserA's message "Hi".
    Retrieve points for UserA's message.

Test Method: The system was tested using a learning-based approach with the RandomWordEqOracle and L* algorithm.
Observation: Points for UserA's message were not updated correctly when likes and dislikes were performed rapidly in succession.
After comparison you will get a message saying that Models are not equivalent.

MessageBoard 1
Banned users are not actually banned, allowing them to continue publishing messages.
Even after being reported multiple times, the user is not banned from publishing new messages.
This indicates a failure in the banning mechanism where the reported status is not correctly enforced.
This was noticed, if a user who has already banned someone reports them again, it allows the banned user to become unbanned, showing a flaw in the banning logic.
Test Case: The following sequence of actions was tested to observe this behavior:

    UserA publishes a message "Hi".
    User1 reports UserA.
    User2 reports UserA.
    User3 reports UserA.
    User4 reports UserA.
    User5 reports UserA.
    User5 reports UserA again.
    UserA publishes another message "still alive".

Test Method: The system was tested using a learning-based approach with the RandomWordEqOracle and L* algorithm.
Observation: UserA was able to publish a new message "still alive" even after being reported multiple times, indicating that the banning mechanism failed.
After comparison you will get a message saying that Models are not equivalent.

MessageBoard 2
Editing messages and retrieving them showed unexpected behavior.
When multiple messages were edited and retrieved, the updates were not consistent across different users.
Test Case: The following sequence of actions was tested to observe this behavior:

    UserA publishes a message "Hi".
    UserB publishes a message "Hi".
    UserC publishes a message "Hi".
    UserA edits their message from "Hi" to "Yo".
    UserB edits their message from "Hi" to "Yo".
    UserC edits their message from "Hi" to "Yo".
    Retrieve messages for UserA.
    Retrieve messages for UserB.
    Retrieve messages for UserC.
Test Method: The system was tested using a learning-based approach with the RandomWordEqOracle and L* algorithm.

Observation: Edited messages were not consistently updated across different users.
After testing it i could ovserve a new message that was not published or entered by any user instead of the edited message.
Unforunately using the learning-based approach, the bug was not detected. The bug was detected by running the test multiple times and increasing the number of iterations.
Though it is still inculded in the test.py but commented out.
#### Describe the bugs for each implementation. Add a shortest test-case that reproduces the bug 

### Task 4

#### Describe the bug
