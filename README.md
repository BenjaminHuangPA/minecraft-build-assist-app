# minecraft-build-assist-app
Minecraft build assistance tool I created using Python's tkinter library as a side project


This is a small Minecraft build assist tool that I wrote over the course of several months using Python’s tkinter library, as a method of practicing GUI design and working on a long-term project. 

Its purpose is to provide the user a method of “mocking out” Minecraft builds from a top-down perspective without having to actually construct them within the game. The program also calculates the precise amount of materials needed for the build, such that if the player is planning on creating it in survival mode, they will not have to estimate and possibly gather a surplus.

The program also allows users to load pre existing builds from a Minecraft world into the program directly. This feature’s intended use is for users who have constructed a build in creative mode and would like to “transfer” the build to a world in survival mode. By being able to view their builds in the Minecraft Build Assist Tool in a slice-by-slice fashion, recreating the build in the separate world becomes easy.

The program has several constraints. First, the size of a build is limited to 40 blocks by 40 blocks. Secondly, it currently only supports blocks up to and including Minecraft version 1.16 (the nether update). 

**Instructions for Running**

To run this program, you must have Python 3.7 or above installed on your computer, as well as the tkinter and PIL python libraries. 

Simply change the directory to that of the repository and type “python mcbuildassist.py” in the command line.

**Keyboard Commands**
Mouse wheel up/down - zoom in and out

Arrow keys - if a portion of blocks have been selected, hitting the down arrow key will move the selection down, hitting the left arrow key will move the selection left, etc. 

Escape - if a portion of blocks have been selected, hitting the escape key will unselect them.

“c” key - if a portion of blocks have been selected, hitting the “c” key will copy them to the clipboard.

“p” - paste blocks copied to the clipboard. This will place them in the same spot they were copied from, you can use the arrow keys to move the pasted blocks around to the desired location.

“d” key - delete the selected blocks from the current layer

“h” - flip the currently selected blocks horizontally

“v” - flip the currently selected blocks vertically

“r” - rotate the current selection 90 degrees counterclockwise

Left click - depending on the current mode, will place, delete, or select a single block.

Right click - place a selection point. Two of these must be on the grid to make a selection of blocks. The first one will be treated as the northwest selection point, and the second one will be treated as the southeast selection point. A red box will be drawn between the two points and all the blocks within will be selected.

Number keys 1 through 6 - use the quick-select bar. As you place blocks, this bar in the top right corner will become populated with your 6 most recently placed blocks. It is updated as you switch to new blocks to place. Pressing 1 will select the block at position 1 in the bar, pressing 2 will select the block at position 2 in the bar, etc
