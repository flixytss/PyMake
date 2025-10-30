import os
import sys

args = ""
from_folder = ""
out_folder = "build"
cache_folder = ".cache"

project_name = "Project"

Error_message = "\033[31mFATAL ERROR\033[0m:"

Taking_from_file = False
version = 1

# Compiler
CC = "g++"

command = f"{CC}"

def clean():
    print("\033[93mLog\033[0m: Cleaning...")
    for i in os.listdir(out_folder):
        os.system(f"rm {out_folder}/{i}")
def endall_correctly():
    print("\033[32mEXIT\033[0m: Exit without errors!")
    exit(0)
def endall_error1(i):
    print(f"{Error_message} The file {i} failed compiling, Fix that")
    exit(1)
files_to_compile = []
def getfiles():
    global files_to_compile
    print("\033[93mLog\033[0m: Saving files to use them later...")
    files = os.listdir(f"{from_folder}")

    files_to_compile = []

    for file in files:
        print(f"\033[93mLog\033[0m: File {file} saved in cache")
        _file = file.split('.')[0]
        _file+='.cache'

        if(not os.path.isfile(f"{cache_folder}/{_file}")): os.system(f"touch {cache_folder}/{_file}")

        with open(f"{cache_folder}/{_file}", 'r') as i: # Chosing which file gonna be compiled
            with open(f"{from_folder}/{file}", 'r') as y:
                if(not i.read()==y.read()):
                    files_to_compile.append(file)
                    print(f"\033[93mGetting files\033[0m: {file} Gonna be compiled!")
                __file = file.replace('.cpp', '.o')
                if(not os.path.isfile(f"{out_folder}/{__file}")):
                    files_to_compile.append(file)
                    print(f"\033[93mGetting files\033[0m: {__file} does not exists, So lets compile it!")

                y.close()
            i.close()
        with open(f"{cache_folder}/{_file}", 'w') as i: # Saving
            with open(f"{from_folder}/{file}", 'r') as y:
                i.write(y.read())
                print(f"\033[93mSaving\033[0m: File {cache_folder}/{_file} writted")
                y.close()
            i.close()
    
    try:
        return files_to_compile
    except FileNotFoundError:
        print(f"{Error_message} That folder does not exists")
    return None
def compile_o(link_):
    global command, args

    if(args.startswith(' ')):args = args[:0] + args[0+1:]

    files = getfiles()

    for i in range(len(files)):
        out = files[i].split('.')[0]
        out+=".o"
        command=f"{CC} {args} {from_folder}/{files[i]} -o {out_folder}/{out}"

        exit_code = os.system(command)
        exit_code = os.WEXITSTATUS(exit_code)

        percent = i/len(files)

        if(not i == len(files)-1): print(f"[ {command} ]", f"\033[32m{percent:.2%}\033[0m")
        else: print(f"[ {command} ]", "\033[32m100%\033[0m")

        if(exit_code==1):
            endall_error1(files[i])
        
    if(link_==False):endall_correctly()
    return
def link(end_):
    if(len(files_to_compile)==0):
        return

    global command, args
    print("\033[93mLog\033[0m: Linking...")

    files = ""

    for i in os.listdir(out_folder):
        if(i.endswith('.o')):
            files+=f"{out_folder}/"+i+' '
    args = args.replace("-c", '')
    command = f"{CC} {args} {files}-o {out_folder}/{project_name}"

    exit_code = os.system(command)
    exit_code = os.WEXITSTATUS(exit_code)

    if(exit_code==1):
        endall_error1(project_name)
    
    print(f"[ {command} ]", "\033[32mREADY!\033[0m")
        
    if(end_==True):endall_correctly()
def readfile(file):
    global args, project_name, from_folder, out_folder, CC
    try:
        with open(file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                division = line.split('=')
                if("Args" in division[0]):
                    args = division[1]
                if("Project-Name" in division[0]):
                    project_name = division[1]
                if("Folder" in division[0]):
                    from_folder = division[1]
                if("Out" in division[0]):
                    out_folder = division[1]
                if("CC" in division[0]):
                    CC = division[1]
            args = args.replace('\n','')
            project_name = project_name.replace('\n','')
            from_folder = from_folder.replace('\n','')
            out_folder = out_folder.replace('\n','')
            CC = CC.replace('\n','')

            if(args.startswith(' ')):args = args[:0] + args[0+1:]
            if(project_name.startswith(' ')):project_name = project_name[:0] + project_name[0+1:]
            if(from_folder.startswith(' ')):from_folder = from_folder[:0] + from_folder[0+1:]
            if(out_folder.startswith(' ')):out_folder = out_folder[:0] + out_folder[0+1:]
            if(CC.startswith(' ')):CC = CC[:0] + CC[0+1:]

            with open(f"{cache_folder}/last.cache", 'w') as a:
                a.write(project_name)
                a.close()

            file.close()
    except FileNotFoundError:
        print(f"{Error_message} That file does not exists")
        exit(1)

help = """
\033[32mPyMake\033[0m is a tool, Making a little bit easy to compile C++ files with args and stuff like that
The paramethers are:

\033[32m-v\033[0m: Display the actual pymake version
\033[32m-h\033[0m: Display the help text
\033[32m-c\033[0m: Compile with the next paramethers
    \033[32m-f\033[0m: Specify the folder with the files to compile
\033[32m-a\033[0m: Specify the paramethers with a file
\033[32m-file\033[0m: Specify the settings file, That's have the parametheres as variables
\033[32m-run\033[0m: Run the App by the project name
\033[32m-clean\033[0m: Clean the out directory
\033[32m-save\033[0m: Save the files that are in the chosed folder, To not compile things that are already compiled
"""

if __name__=="__main__":
    try:
        print("\033[93mLog\033[0m: Creating the output folder...")
        os.mkdir(out_folder)
    except Exception as e:
        pass
    try:
        print("\033[93mLog\033[0m: Creating the .cache folder...")
        os.mkdir(cache_folder)
    except Exception as e:
        pass

    index = 0
    if(len(sys.argv)>1):
        for i in sys.argv:
            index+=1
            if(i=="-file"):
                Taking_from_file = True
                try:
                    readfile(sys.argv[index])
                    compile_o(True)
                    link(False)
                except IndexError:
                    readfile("config.conf")
                    compile_o(True)
                    link(False)
            if(i=="-clean"):
                clean()
            if(i=="-save"):
                getfiles()
            if(i=="-a"): # SETTING ARGS
                try:
                    try:
                        with open(f"{sys.argv[index]}", 'r') as o:
                            r = o.readlines()
                            for y in r:
                                definition = y.split('=')[0]
                                args = y.split('=')[1]
                            o.close()
                    except FileNotFoundError:
                        print(f"{Error_message} That settings file does not exists")
                        exit(1)
                except IndexError:
                    print(f"{Error_message} Please specify the settings file")
                    exit(1)
                print("\033[33mOption\033[0m: set Args")
            if(i=="-c" and not Taking_from_file): # COMPILE
                try:
                    if(sys.argv[index]=="-f"):
                        try:
                            from_folder=sys.argv[index+1]
                            print(f"\033[33mFolder\033[0m: {from_folder}")
                            compile_o(True)
                            link(False)
                        except IndexError:
                            print(f"{Error_message} Please specify the folder location.")
                            exit(1)
                        print("\033[33mOption\033[0m: Compile from a folder")
                except IndexError:
                    print(f'{Error_message} Compile what?, "-h" To a little help')
                    exit(1)
            if(i=="-run"): # RUN
                print("\033[32mSuccess\033[0m: Running App!")
                with open(f"{cache_folder}/last.cache", 'r') as s:
                    exit_code = os.system(f"./{out_folder}/{s.read()}")
                    s.close()
                exit_code = os.WEXITSTATUS(exit_code)
                if(exit_code):
                    print(f'{Error_message} Run what?')
            if(i=="-v"): # RUN
                print(f"\033[32mPyMake Version\033[0m: {version}")
            if(i=="-h"): # RUN
                print(help)
                
        endall_correctly()
    else:
        print("Please specify the files to compile")
        print('"Make" on python :), "-h" to display help')
        print(f"\033[32mPyMake Version\033[0m: {version}")