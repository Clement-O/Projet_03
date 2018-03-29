# Maze Game
Made for my third project on [OpenClassrooms](https://openclassrooms.com/) in Python3.
Main features / rules are :
- Customize your own maze (Look at next section if you want to)
- Random spawn of items at each launch.
- One life.
- Display how many items you actually have (and how many are on the maze).
- Loot every items before pass through the guard or you're dead. (And since you have one life, it's also a GameOver).

# Maze customization
Open the file 'maze' and change whatever you want, just follow those rules :
- 'w' is for Wall.
- 'S' is for your Starting position.
- 'E' is for the End of the maze (which is the guard).
- ' ' (space) is for the ground.

Default size is 15x15 but you can go 10x10 or 20x20 or whatever, just keep it square !!!

You can also change :
- The sprites (1) : in sprites directory, just keep the name and the ".png" format.
- The sprites (2) : in settings.py, you can change the format and the size of your sprites. (It will change the size of the window).
- The number of items : go in settings.py, look for "NB_ITEMS" and change the value.
