import os
import datetime
import inspect


filename_p = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def mkdir():
    fun_name = inspect.stack()[1][3].split("_")[-1]
    filename = "./" + str(filename_p) + fun_name
    os.mkdir(filename)
    
    
