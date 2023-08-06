import os
import argparse

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_script():
    parser = argparse.ArgumentParser(description='Create a menu-based script.')
    parser.add_argument('-n', '--name', type=str, help='name of the script')
    parser.add_argument('-o', '--options', type=int, help='number of menu options')

    args, _ = parser.parse_known_args()

    if args.name and args.options:
        script_name = args.name.replace(" ", "_").replace("-", "").replace(".", "")
        num_options = args.options
    else:
        print("         _nnnn_ ")
        print("        dGGGGMMb ")
        print("       @p~qp~~qMb ")
        print("       M|@||@) M| ")
        print("       @,----.JM| ")
        print("      JS^\__/  qKL ")
        print("     dZP        qKRb ")
        print("    dZP          qKKb ")
        print("   fZP            SMMb ")
        print("   HZM            MMMM ")
        print("   FqM            MMMM ")
        print(" __| \".        |\\dS\"qML ")
        print(" |    `.       | `' \\Zq ")
        print("_)      \\.___.,|     .' ")
        print("\\____   )MMMMMP|   .' ")
        print("     `-'       `--' Mr. Robot ")
        print("Menu Script Generator")
        script_name = input("What do you want to call your script?: ")
        script_name = script_name.replace(" ", "_").replace("-", "").replace(".", "")
        while True:
            try:
                num_options = int(input("How many menu options do you want?: "))
                break
            except ValueError:
                print("Please enter a valid number.")

    options = []
    func_names = []
    cmds = {}
    for i in range(num_options):
        while True:
            option_name = input(f"Name of option {i+1}: ")
            if not option_name.strip():
                print("Option name cannot be blank.")
                continue
            elif option_name == "exit":
                print("Note: 'exit' is already included as an option and does not need to be added.")
                continue
            elif option_name.isdigit():
                print("Option name cannot be only digits.")
                continue
            else:
                break
        func_name = option_name.lower().replace(" ", "_").replace("-", "").replace(".", "")
        options.append(option_name)
        func_names.append(func_name)
        # Check if option has a command
        cmd_choice = input(f"Does option {option_name} have a command that can be run via command line? (y/n): ")
        if cmd_choice.lower() == "y":
            cmd = input(f"Enter the command exactly how you would type it in console for option {option_name}: ")
            cmds[option_name] = cmd

    options.append("Exit")
    func_names.append("exit_menu")

    with open(f"{script_name}.py", "w") as f:
        f.write("#!/usr/bin/env python\n\n")
        f.write("###===Import Modules Go Here===###")
        f.write(f"\n")
        f.write("import os\n")
        f.write(f"\n")
        f.write("###===Separator Function For Pretty Menu===###")
        f.write(f"\n")
        f.write(f"def print_separator():\n")
        f.write("    print(\"=\" * 50)\n\n")
        f.write(f"###===Your Viewable Menu===###")
        f.write(f"\n")
        f.write(f"def menu():\n")
        f.write("    clear_screen()\n")
        f.write(f"    print('{script_name.replace('_', ' ').title()}')\n")
        f.write("    print_separator()\n")
        for i in range(num_options):
            f.write(f"    print('{i+1}. {options[i].title()}')\n")
        f.write(f"    print('(exit) Exit')\n\n")
        f.write("###===Making Clear Screen Work On Windows And Linux===###")
        f.write(f"\n")
        f.write(f"def clear_screen():\n")
        f.write("    os.system('cls' if os.name == 'nt' else 'clear')\n\n")
        f.write("###===When You Choose An Option It Runs One Of These===###")
        f.write(f"\n")
        for i in range(num_options):
            # Get function name based on option name
            func_name = func_names[i]
            f.write(f"def {func_name}():\n")
            f.write(f"    print('You selected {options[i]}')\n")
            # Check if option has a command
            if options[i] in cmds:
                cmd = cmds[options[i]]
                f.write(f"    {options[i].lower().replace(' ', '_').replace('-', '').replace('.', '')}_cmd = f\"{cmd}\"\n")
                f.write(f"    os.system({options[i].lower().replace(' ', '_').replace('-', '').replace('.', '')}_cmd)\n")
            f.write("    input('Press enter to return to menu...')\n\n")
        f.write(f"def exit_menu():\n")
        f.write("    print('Goodbye!')\n")
        f.write("    exit()\n\n")
        f.write("###===Enter Your Choice And Then It Will Activate That Option===###")
        f.write(f"\n")
        f.write(f"if __name__ == '__main__':\n")
        f.write("    while True:\n")
        f.write("        menu()\n")
        f.write("        choice = input('Enter your choice: ')\n")
        for i in range(num_options):
            f.write(f"        if choice == '{i+1}':\n")
            func_name = func_names[i]
            f.write(f"            {func_name}()\n")
        if "exit" in options:
            f.write("        elif choice.lower() == 'exit' or choice == '0':\n")
        else:
            f.write("        elif choice.lower() == 'exit':\n")
        f.write("            exit_menu()\n")
        f.write("        else:\n")
        f.write("            print('Invalid choice. Try again.')\n")
        clear_screen()
        
    print("Menu options:")
    for i in range(num_options):
        print(f"{i+1}) {options[i]}")
        if options[i] in cmds:
            print(f"command set  = {cmds[options[i]]}")
    print(f"{len(options)}) Exit")
    print(f"\nScript '{script_name}.py' created successfully!")
    response = input("Would you like to run it now? (y/n) ")
    if response.lower() == "y":
        os.system(f"python3 {script_name}.py")

clear_screen()
create_script()
