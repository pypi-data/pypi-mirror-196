from multiprocessing import Process, Manager
import sys
from time import sleep
import shutil

## Argument Parsing Sector ##
columns = shutil.get_terminal_size().columns

# Check if tag has more than one Argument
def moreArg(tag):
    count = []
    for arg in argList:
        if (tag == argList[arg]["tag"]):
            count.append(arg)
    return count

# Show help when --help or -h argument inputed
def showHelp():
    showError(type = "help")
    try:
        print("\n" + description + "\n")
    except NameError:
        pass
    
    print("Options:")
    print("  -h, --help:")
    print("  Show this Help massage and Exit\n")
    
    isMulti = ""
    for arg in argList:
        if (arg in isMulti):
            continue
        
        tag = argList[arg]["tag"]
        isMulti = moreArg(tag)
        argp = ""
        for a in isMulti:
            argp += a + ", "
        
        argp = argp[:-2]
        
        help = argList[arg]["help"]
        print("  " + argp + ":")
        
        if not (help == ""):
            print("  " + help + "\n")
        else:
            print("  \033[3;90mNo Message Provided\n\033[0;37m")
    
    sys.exit()



# Show Error if any required argument not Passed
def showError(type = "all", argName = ""):
    fileName = argvsArgParser[0].split("/")[-1]
    blank = 8 + len(fileName)

    print("Usage: " + fileName + " [-h]")
    required = []
    isMulti = ""
    
    for arg in argList:
        if (arg in isMulti):
            continue
        isMulti = moreArg(argList[arg]["tag"])
        argp = ""
        for a in isMulti:
            required.append(a)
            argp += a + ", "
        argp = argp[:-2]

        if (argList[arg]["required"] == "true"):
            print(" " * blank + argp + " " + argList[arg]["tag"])
        elif (argList[arg]["required"] == "false"):
            print(" " * blank + "( " + argp + " " + argList[arg]["tag"] + " )")
        else:
            print(" " * blank + "[ " + argp + " " + argList[arg]["tag"] + " ]")
    
    if (type == "all"):
        print("\n" + fileName + ": Error: The following Arguments are Required:", end = "")
        for i in required:
            print(" " + i, end = ",")
        
        sys.exit("\b \n")
    elif (type == "arg"):
        print("\n" + fileName + ": Error: Argument " + argName + ": Expected One Argument")
        
        sys.exit("")
    elif (type == "optional"):
        print("\n" + fileName + ": Error: Minimum one Argument is Required:", end = "")
        for i in optional:
            print(" " + i, end = ",")
        
        sys.exit("\b \n")
    
    elif (type == "only"):
        print("\n" + fileName + ": Error: You Must Enter \033[3m" + argList[argName]["tag"] + "\033[0m as your First Argument")
        sys.exit("")
    elif (type == "help"):
        pass
    


#Parsing Arguments
def argData(argName, required, takeArg):
    try:
        if (argvsArgParser[1] == "-h") or (argvsArgParser[1] == "--help"):
            showHelp()
    except IndexError:
        pass
    
    for i in argList:
        if (argList[i]["required"] == "optional"):
            if not any(op in argvsArgParser for op in optional):
                showError(type = "optional")

    if (takeArg == "only"):
        if (len(argvsArgParser) == 1):
            showError(type = "only", argName = argName)
        
        if not (argvsArgParser[1] in argList):
            data = argvsArgParser[1]
            return data
        else:
            showError(type = "only", argName = argName)
    """
    try:
        if (argvsArgParser[1] == "-h") or (argvsArgParser[1] == "--help"):
            showHelp()
    except IndexError:
        pass
    """
    if (argName in argvsArgParser):
        if (len(argvsArgParser) >= argvsArgParser.index(argName) + 2):
            data = argvsArgParser[argvsArgParser.index(argName) + 1]
            if (data in argList):
                if (takeArg == "true"):
                    showError(type = "arg", argName = argName)
        else:
            if (takeArg == "true"):
                showError(type = "arg", argName = argName)
            data = True
    else:
        if (required == "true"):
            showError()
        
        data = False
    
    return data


#Main Class
class argparser():
    
    global argList, finalList, optional
    argList = {}
    finalList = {}
    optional = []
    
    def add_argument(self, arg, tag, required = "false", takeArg = "true", help = ""):
        if (type(arg) == tuple) or (type(arg) == list):
            for a in arg:
                if (required == "optional"):
                    optional.append(a)
                argAdd = {a : {"tag": tag, "required": required, "help": help, "takeArg": takeArg}}
                argList.update(argAdd)
        else:
            if (required == "optional"):
                optional.append(arg)
            argAdd = {arg : {"tag": tag, "required": required, "help": help, "takeArg": takeArg}}
            argList.update(argAdd)
    
    def add_description(self, desc):
        global description
        description = desc
    
    class parsed():
        def __init__(self):
            
            for arg in argList:
                tag = argList[arg]["tag"]
                required = argList[arg]["required"]
                takeArg = argList[arg]["takeArg"]
                
                argdata = argData(arg, required, takeArg)
                
                if (required == "optional") and (argdata == False):
                    continue
                
                addData = {tag: argdata}
                
                finalList.update(addData)
            
        dict = finalList
        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

argvsArgParser = sys.argv


## Background Process Executor Sector ##

# Using an Extarnal Function to Get return data from User Targer Function if exists
def get_return_func(action, arg, return_dict):
    if (type(arg) == tuple):
        data = action(*arg)
    elif (type(arg) == dict):
        data = action(**arg)
    elif not (arg == ""):
        data = action(arg)
    else:
        data = action()
    
    return_dict["return"] = data


# Convert String to a global Function
def make_func(data):
    dataList = data.split("\n")
    
    func = "def actionMade():"
    for line in dataList:
        func += "\n    " + line
    
    # Running a Function String via exec to make it Callable
    exec(func, globals())
    

def bg_process(action, anim = "line", speed = "normal", end = "", args = ""):
    # If user inputs String instead of Function, then convert the string into a Function
    if (type(action) == str):
        make_func(action)
        action = actionMade
        
    speed = str(speed)
    if (speed == "normal"):
        delay1 = 0.2
        delay2 = 0.3
    elif (speed == "fast"):
        delay1 = 0.2
        delay2 = 0
    elif (speed == "slow"):
        delay1 = 0.5
        delay2 = 0.5
    elif (speed.isdigit()):
        delay1 = int(speed) / 2
        delay2 = int(speed) / 2
    else:
        try:
            speed = float(speed)
            delay1 = speed / 2
            delay2 = speed / 2
            if (delay1 < 0.2):
                delay1 = speed
                delay2 = 0
        except ValueError:
            delay1 = 0.2
            delay2 = 0.3
    
    manager = Manager()
    return_dict = manager.dict()
    
    # Makind Argument Tuple
    pass_args = (action, args, return_dict)
    
    # Executing Process
    process = Process(target = get_return_func, args = pass_args)
    process.daemon = True
    process.start()
    
    if (anim == "line"):
        symbols = ["|", "/", "-", "\\"]
        while process.is_alive():
            for symbol in symbols:
                sleep(delay1)
                if  not (process.is_alive()):
                    break
                sys.stdout.write("\b" + symbol)
                sys.stdout.flush()
                sleep(delay2)
                if not (process.is_alive()):
                    break
    
    elif (anim == "dot"):
        while process.is_alive():
            sleep(delay1)
            if not (process.is_alive()):
                break
            sys.stdout.write(".")
            sys.stdout.flush()
            sleep(delay2)
    
    try:
        bg_process.rdata = return_dict["return"]
    except KeyError:
        bg_process.rdata = None
