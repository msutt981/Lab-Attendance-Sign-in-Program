"""
Matthew Sutter 1/19/2023
This is a basic start to a sign-in program.
Also a way to brush up on python which I haven't used in a while.
"""

from datetime import datetime
from datetime import timedelta
import json
from json import JSONEncoder, JSONDecoder
from pathlib import Path

# https://gist.github.com/majgis/4200488
#Taken from http://taketwoprogramming.blogspot.com/2009/06/subclassing-jsonencoder-and-jsondecoder.html
class DateTimeAwareJSONEncoder(JSONEncoder):
  """ 
  Converts a python object, where datetime and timedelta objects are converted
  into objects that can be decoded using the DateTimeAwareJSONDecoder.
  """
  def default(self, obj):
    if isinstance(obj, datetime):
      return {
        '__type__' : 'datetime',
        'year' : obj.year,
        'month' : obj.month,
        'day' : obj.day,
        'hour' : obj.hour,
        'minute' : obj.minute,
        'second' : obj.second,
        'microsecond' : obj.microsecond,
      }

    elif isinstance(obj, timedelta):
      return {
        '__type__' : 'timedelta',
        'days' : obj.days,
        'seconds' : obj.seconds,
        'microseconds' : obj.microseconds,
      }

    else:
      return JSONEncoder.default(self, obj)

class DateTimeAwareJSONDecoder(JSONDecoder):
  """ 
  Converts a json string, where datetime and timedelta objects were converted
  into objects using the DateTimeAwareJSONEncoder, back into a python object.
  """
  def __init__( self):
    JSONDecoder.__init__( self, object_hook=self.dict_to_object )

  def dict_to_object(self, d):
    if '__type__' not in d:
      return d

    type = d.pop('__type__')
    if type == 'datetime':
      return datetime(**d)
    elif type == 'timedelta':
      return timedelta(**d)
    else:
      # Oops... better put this back together.
      d['__type__'] = type
      return d


class Login: # Builds logins as objects
    def __init__(self,uname,pid,signin,signout,ttotal):
        self.uname=uname
        self.signin=signin
        self.signout=signout
        self.ttotal=ttotal
        self.pid=pid

    def __str__(self):
        return f"{self.signin} || {self.signout} || {self.ttotal} || {self.pid} || {self.uname}"

def int_input(prompt): # integer input validation
    while True:
        try:
            output=int(input(prompt).replace(" ",""))
            return output
        except ValueError:
            print("Please just type in whole numerals")

def show_header():
    print("       Sign-in      ||       Sign-out      || Cumulative time in Lab || PIN || Name\n") # Cumulative time in lab? instead of Total?

def show_menu():
    print("\nADN Lab Sign-in \n")
    print("1. Sign-in")
    print("2. Sign-out")

def admin_menu(log,pool):
    options=[1,2,3,4,5,6]
    while True:
        print(f"\n ADN Lab Admin Menu\n")
        print(f"1. Show signed-in names")
        print(f"2. Show Log")
        print(f"3. Search log for name")
        print(f"4. Show final entry for each user")
        print(f"5. Save log to text file")
        print(f"6. exit")
        admin_input=int_input(f"Your choice: ")
        while not admin_input in options:
            admin_input=int_input(f"Please enter a valid choice: ")
        if admin_input == 1:
            print(f"\n    Signed in Names:")
            log_print(pool)
        if admin_input == 2:
            print(f"\n    Log:")
            show_header()
            log_print(log)
        if admin_input == 3:
            find_name(log)
        if admin_input == 4:
          print(F"\n    Final Entry for each Student:")
          show_final(log)
        if admin_input == 5:
            log_save(log, "log.txt")
        if admin_input == 6:
            break

def find_previous(log,uname):
    for i in reversed(log):
        if i.uname == uname:
            return i
# find last instance of uname in the log and return that instance

def find_name(log):
    alist = []
    uname=input("Enter name to search for in the log: ")
    for i in log:
        if i.uname == uname:
            alist.append(i)
    if len(alist) > 0:
        print(f"")
        show_header()
        log_print(alist)
    else: print(f"\n No results found.")

def show_final(log):
  alist=[]
  uuname=set()
  for i in reversed(log):
    if i.uname not in uuname:
      uuname.add(i.uname)
      alist.append(i)
  show_header()
  log_print(alist)
      
  
def sign_in(pool,log):
    uname=input("Enter name to sign in: ")
    if uname in pool: # check for uname in pool of signed in names
        print("\nThe name you entered is already signed in to a lab")
        return
    if uname == "": # a way to drop back to the menu
        return
    pid=input("Enter personal pin/password: ")
    if pid == "":
        return
    now = datetime.now().replace(microsecond=0)
    index = find_previous(log,uname)
    if index != None:
        u1 = Login(uname,pid,now,'         -         ',index.ttotal+timedelta(minutes=0))
    else:
        u1 = Login(uname,pid,now,'         -         ',timedelta(minutes=0))
    return u1

def sign_out(pool,log):
    uname=input("Enter name to sign out: ")
    if uname not in pool: # check if uname is NOT in pool of signed in names
        print("\n The name you entered was not signed in to a lab")
        return
    now = datetime.now().replace(microsecond=0)
    index = find_previous(log,uname)
    pid = str(input("Enter personal pin/password: "))
    if pid == "":
        print(f"Entry was blank, returning to menu")
    if pid != index.pid:
        print(f"Personal pin/password didn't match sign-in. Please Try again.")
        pid = str(input("Enter personal pin/password: "))
        if pid == "":
            print(f"Entry was blank. Returning to main menu")
            return
    u1 = Login(uname,pid,index.signin,now,(now-index.signin)+index.ttotal)
    return u1

def initialize_log(filename,u0):
    path = Path(filename)
    log = []
    if path.is_file():        
        interdict=load_object(filename)
        for i in interdict:
          u1=Login(i['uname'],i['pid'],i['signin'],i['signout'],i['ttotal'])
          log.append(u1)
    else:
        log=[u0]
    return log
# ^ initializes the log list with either previously saved data or a clean list

def log_print(log):
    for x in log:
        print(x)
# used to loop through list and print the objects in it in human readable form

def save_object(obj,filename):
    try:
        with open(filename, "w") as f: #check what all the letter modifiers do
            json.dump([ob.__dict__ for ob in obj], f, cls=DateTimeAwareJSONEncoder, indent=2)
    except Exception as ex:
        print("Error: ", ex)

def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return json.load(f, cls=DateTimeAwareJSONDecoder)
    except Exception as ex:
        print("Error: ", ex)

def log_save(obj, filename):
    now = datetime.now().replace(microsecond=0).strftime("%Y-%m-%d_%H.%M.%S.")
    try:
        with open(now+filename, "w+") as f:
            for x in obj:
                f.write(f"{x}\n")
    except Exception as ex:
        print("Error: ", ex)

def main():
    options=[1,2,9987]
    u0=Login("Shade","0303",datetime.now().replace(microsecond=0),datetime.now().replace(microsecond=0)+timedelta(hours=3),timedelta(hours=3))
    #log=[u0] # running log sheet, list
    log=list((initialize_log('log.json',u0))) # initialize log list
    pool=set() # initialise the set of signed in names
    while True:
        show_menu()
        user_input=int_input("Your choice: ")
        while not user_input in options:
            user_input=int_input("Please enter a valid choice: ") #possible softlock here?
        if user_input == 1:
            u1 = sign_in(pool,log)
            if u1 != None:
                pool.add(u1.uname)
                print(f"\n{u1.uname} has signed in at {u1.signin}.")
        if user_input == 2:
            u1 = sign_out(pool,log)
            if u1 != None:
                pool.remove(u1.uname)
                print(f"\n{u1.uname} has signed out at {u1.signout}. Session time was {u1.signout - u1.signin}. Have a nice day.")
        if user_input == 9987:
            u1 = admin_menu(log,pool)
        if u1 != None:
            log.append(u1)
            save_object(log,"log.json")

main()
