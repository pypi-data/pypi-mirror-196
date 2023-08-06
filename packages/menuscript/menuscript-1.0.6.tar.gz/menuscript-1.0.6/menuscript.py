import os
import argparse
import re
import subprocess
import sys

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
            variables = re.findall(r'\$.*$', cmd)
            if variables:
                cmds[option_name] = cmd
                print(f"Warning: The following variables are used in the command for option {option_name}: {', '.join(variables)}")
            else:
                cmds[option_name] = str(cmd)
                print(f"No variables found in command for option {option_name}. Command set to {cmd}")
        else:
            cmds[option_name] = ""
            print(f"No variables found in command for option {option_name}. Command set to empty string")

    options.append("Exit")
    func_names.append("exit_menu")

    file_name = re.sub(r'[^\w\s_]', '', script_name)

    with open(f"{file_name}.py", "w") as f:
        f.write("#!/usr/bin/env python\n\n")
        f.write("###===Import Modules Go Here===###\n")
        f.write("import os\n\n")
        f.write("###===Setting your variables to blank values===###\n")


        # Count the variables and write their definitions to the file
        variable_counts = {}
        for cmd in cmds.values():
            variables = set(re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', cmd))
            for variable in variables:
                if variable not in variable_counts:
                    variable_counts[variable] = [i+1 for i in range(num_options) if options[i].find(variable) != -1]
                else:
                    variable_counts[variable].extend([i+1 for i in range(num_options) if options[i].find(variable) != -1])
        for variable in sorted(variable_counts):
            f.write(f"{variable} = \"\"\n")
        f.write("\n")
        f.write("###===Separator Function For Pretty Menu===###\n")
        f.write("def print_separator():\n")
        f.write("    print(\"=\" * 50)\n\n")
        f.write("###===Your Viewable Menu===###\n")
        f.write("def menu():\n")
        f.write("    clear_screen()\n")
        f.write(f"    print('{script_name.replace('_', ' ').title()}')\n")
        if bool(variable_counts):
            f.write("    variable_counts = {}\n")
            for cmd in cmds.values():
                variables = set(re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', cmd))
                for variable in variables:
                    if variable not in variable_counts:
                        variable_counts[variable] = [i+1 for i in range(num_options) if options[i].find(variable) != -1]
                    else:
                        variable_counts[variable].extend([i+1 for i in range(num_options) if options[i].find(variable) != -1])
            variable_names = sorted(variable_counts.keys())
            variable_list = ", ".join([f"${v}" for v in variable_names])
            f.write(f"    print('Your script has some variables {variable_list}')\n")
        f.write("    print_separator()\n")
        for i in range(num_options):
            f.write(f"    print('{i+1}. {options[i].title()}')\n")
        f.write("    variable_counts = {}\n")
        for cmd in cmds.values():
            variables = set(re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', cmd))
            for variable in variables:
                if variable not in variable_counts:
                    variable_counts[variable] = [i+1 for i in range(num_options) if options[i].find(variable) != -1]
                else:
                    variable_counts[variable].extend([i+1 for i in range(num_options) if options[i].find(variable) != -1])
        for variable in sorted(variable_counts):
            f.write(f"    print(f'set_{variable} | current variable {variable} = {{{variable}}}')\n")
        f.write("    print('(exit) Exit')\n\n")
        f.write("###===Making Clear Screen Work On Windows And Linux===###\n")
        f.write("def clear_screen():\n")
        f.write("    os.system('cls' if os.name == 'nt' else 'clear')\n\n")
        f.write("###===When You Choose An Option It Runs One Of These===###")
        f.write(f"\n")
        for i in range(num_options):
            # Get function name based on option name
            func_name = func_names[i]
            func_name_stripped = re.sub(r'[^a-zA-Z0-9_]', '', func_name)
            func_name_safe = func_name_stripped or f"option{i+1}"
            f.write(f"def {func_name_safe}():\n")
            f.write(f"    print('You selected {options[i]}')\n")
            # Check if option has a command
            if options[i] in cmds:
                cmd = cmds[options[i]]
                # Replace variables with curly brackets
                cmd = re.sub(r'\$([\w]+)', r'{\1}', cmd)
                cmd_var_name = options[i].lower().replace(' ', '_').replace('-', '').replace('.', '')
                cmd_var_name_safe = re.sub(r'[^a-zA-Z0-9_]', '', cmd_var_name) or f"option{i+1}_cmd"
                f.write(f"    {cmd_var_name_safe} = f\"{cmd}\"\n")
                f.write(f"    try:\n")
                f.write(f"        os.system({cmd_var_name_safe})\n")
                f.write(f"    except KeyboardInterrupt:\n")
                f.write(f"        print('{cmd_var_name_safe} interrupted by user')\n")
            f.write("    input('Press enter to return to menu...')\n\n")
        for variable in variables:
            variable_counts = {}
            for cmd in cmds.values():
                variables = set(re.findall(r'\$[a-zA-Z_][a-zA-Z0-9_]*', cmd))
                for variable in variables:
                    if variable not in variable_counts:
                        variable_counts[variable] = 1
                    else:
                        variable_counts[variable] += 1
            for i, variable in enumerate(sorted(variable_counts)):
                # Create a function for each variable
                variable = re.sub(r'[^\w\s]', '', variable)
                variable = variable.replace(' ', '')
                func_name = f"set_{variable.lower()}"
                func_name_stripped = re.sub(r'[^\w\s_]', '', func_name)
                f.write(f"def {func_name_stripped}():\n")
                f.write(f"    global {variable}\n")
                f.write(f"    {variable} = input('Enter a new target:')\n")
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
            func_name_stripped = re.sub(r'[^\w\s]', '', func_name)
            f.write(f"            {func_name_stripped}()\n")
            # Add the function as a choice to the menu
        for variable in variables:
            variable_counts = {}
            for cmd in cmds.values():
                variables = set(re.findall(r'\$[a-zA-Z_][a-zA-Z0-9_]*', cmd))
                for variable in variables:
                    if variable not in variable_counts:
                        variable_counts[variable] = 1
                    else:
                        variable_counts[variable] += 1
            for i, variable in enumerate(sorted(variable_counts)):
            # Create a function for each variable
                variable = re.sub(r'[^\w\s]', '', variable)
                variable = variable.replace(' ', '')
                func_name = f"set_{variable.lower()}"
                f.write(f"        if choice == 'set_{variable.lower()}':\n")
                func_name_stripped = re.sub(r'[^\w\s]', '', func_name)
                f.write(f"            {func_name_stripped}()\n")
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
    print(f"\nScript '{file_name}.py' created successfully!")
    response = input("Would you like to run it now? (y/n) ")
    
    if response.lower() == "y":
        try:
            subprocess.run(["python", f"{file_name}.py"])
        except FileNotFoundError:
            subprocess.run(["python3", f"{file_name}.py"])


clear_screen()
create_script()
