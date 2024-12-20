

# Fish Tycoon
Simion Andrei, Ciociea Rares-Andrei - 325CA

## Short Description

* The tycoon is about completing the three levels and catching the golden fish
* There are two types of income: active and passive
* There is a **manual fishing tank** which, by pressing **H**, will add money to the balance
* Also the fishing tank can be upgraded by using the **upgrade table**, which has 3 levels of upgrading
* The passive mode of income is the **idle fishing tanks** which are not generating money at the start of the game. The player can buy **fishermen** which fish for you and have a specific **money per second**

## Dependencies

* PyGame
* Pillow

## Modules

* **Main**
	* The main module contains the **Player** class which handles the drawing of the player and its animation
	* Also, it contains functions that stop the player from colliding with the tanks
	* The objects that the player can collide with are inserted in the **collisionables** array
	* This module contains handling key presses and moving the player, and fading the screen when reaching a new level, and the main **loop** of the game that calls all of the classes' loops, and finally, rendering the **win screen**

* **Walkable**
	* A class that draws a sprite that has no collision detection
	* Used for drawing the floor

* **Block**
	* A class that draws a sprite that has collision detection
	* Used for drawing the walls

* **Money**
	* The **Money** Class contains the balance of the player and handles the drawing of the balance in the top right corner of the screen
	* It contains the **money per second** generated by the **idle fishing tanks** and it updates the balance each second

* **Tank Fishing**
	* The **TankFishing** class draws the **manual fishing tank** which will be a collidable object
	* It handles the pressing of the **H** key to manually fish, and while fishing it locks the player and shows a loading bar above the player's head, signaling the progress of the fishing
	* After the bar dissapears, the player can fish again
	* It draws a prompt telling the player the instructions and how much it generates per press

* **Tank Idle**
	* The **TankIdle** class draws the **idle tak** which will be a collidable object
	* If the player can't afford to buy the tank, it draws a prompt in red telling the player the price and pressed key needed to buy a **fishermen**
	* If the player can afford the fishermen, then the same prompt is drawn in green
	* After the tank is bought, it adds **money per second** to the balance, the fishermen appears next to it, and when nearby the tank, it draws a prompt which tells the player how much it generates

* **Rod Upgrade**
	* The **RodUpgarde** class handles the **upgrade table** underneath the **manual fishing tank**
	* It draws the object, and when nearby, a prompt telling the player the price of the upgrade and how much will it add to the manual fishing tank's *money per action*
	* It has three levels of upgrade, after that it prints a prompt telling the player that the maximum upgrade has been achieved

* **Door**
	* The **Door** is the object that enables the player to advance to the next level
	* It handles the game's level and drawing the prompt which tells the player how much money he needs to advance to the next level