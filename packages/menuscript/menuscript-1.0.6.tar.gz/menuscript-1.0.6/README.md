# MenuScript

MenuScript is a Python script for creating and managing menus in your command line interface (CLI) application. With MenuScript, you can easily create custom menus with options that perform various actions when selected by the user.

![Alt Text](https://i.imgur.com/M46G4UR.gif)

It can be download and ran from github or installed using:
```pip install menuscript```

## Installation

1. Clone this repository:

    ```
    git clone https://github.com/AIMadeScripts/createmenus
    ```

2. Navigate to the cloned directory:

    ```
    cd createmenus
    ```

3. Run the script:

    ```
    python create.py
    ```

## Usage

To use MenuScript, simply run the script as menuscript if installed from pip or menuscript.py if downloaded from github and follow the prompts to create your menu. You can customize the menu by adding, removing, or modifying options as needed. You can also use the following options when creating your menu:

```
-n, --name: Specify a title for your menu.
-o, --options: Specify the amount of options to add to the menu.
```

Example usage:
```
menuscript -n "My Menu Script" -o "4"
```

This will create a new script called my_menu_script.py with 4 menu options. It will also prompt you to enter the names of those options and any commands those options will execute.


After each naming of a menu option you will be prompted to define a command for that menu option to execute. Upon selecting "y" you could do something such as:
```
ping google.com
```

This would then assign that command to that menu option in the new file it creates.

I have added in variables and symbol stripping. If you do
```ping $website```

In this example the menu will add an option called "set_website" which if typed in, will allow you to set that variable and then choose the menu option you assigned that command.

It will automatically identify a variable has been set and add it to the menu script you create so you can define that variable whenever you would like.
This works for as many variables as you want.

Each variable is recognized via the dollar symbol ($) so you can define a variable as whatever you would like. In most cases you will only want one or two and the rest of your commands will read from that when required. 

## Contributing

If you would like to contribute to MenuScript, please fork this repository and submit a pull request with your changes.
