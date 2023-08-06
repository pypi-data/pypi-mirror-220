import logging
import time
from . import DeviceUtilities

class GrepUtilities(DeviceUtilities):

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        self.get_logger(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")
    
    def find_and_replace_line_in_file(self, find_string, replace_string, filename, options=None):
        self.messenger.fun_name = "find_and_replace_line_in_file: " + filename
        if options:
            options = options.split(",")
            if "nonewline" in options:
                replace_string = replace_string.replace("\n", "")

        # print(find_string, replace_string)
        self.print_debug_log("Started")
        
        lines = []
        found_string = False
        check = False
        with open(filename, "r") as f:
            for line in f:
                if "startswith" in options:
                    check = line.startswith(find_string)
                else:
                    check = (find_string in line)
                if check:
                    print(line)
                    # line.replace(find_string, replace_string)
                    line = replace_string
                    print(line)
                    found_string = True
                lines.append(line)
            
        if line == "" or line.replace("\n", "") == "":
            print("EMTPY line")
        if not found_string:
            self.print_debug_log("String Not found")
            if "canadd" in options:
                self.print_debug_log("Can add")
                self.print_debug_log(replace_string)
                lines.append(replace_string)

        with open(filename, "w") as f:
            f.writelines(lines)

        
        self.print_debug_log("Ended")