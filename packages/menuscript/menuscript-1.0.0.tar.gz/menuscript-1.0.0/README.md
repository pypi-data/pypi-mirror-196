# Script for Creating a Menu-Driven Python Script
This script allows you to create a simple menu-driven Python script with options specified by the user. The resulting script will be saved as a .py file and can be run from the command line.

# Note
Do not use only numbers as your menu names. You can have a1 as a menu name but not 1

## How to Use
1. Run the script in your terminal or command prompt.
2. Enter a name for your script (without the .py extension).
3. Enter the number of menu options you want to include.
4. For each option, enter a name for the option (cannot be "exit").
5. The script will generate a .py file with the specified name and menu options.
6. Run the generated script from the command line and choose your desired option.


## Dependencies
This script requires the os module, which is included in the Python standard library.

## Functionality
The generated Python script will display a menu of options based on the input provided during script creation. Each option will be numbered, and the user can enter the corresponding number to select an option. The generated script will include a separate function for each option, with the name option_i where i is the option number. Each function will print a message indicating which option was selected, then prompt the user to press enter to return to the main menu. If the user enters "exit" at the main menu, the script will terminate.

![Alt Text](https://i.imgur.com/ILzp4VD.gif)
