"""
Matthew Sutter 1/27/2023
This is a gui version of the digital sign-in sheet program written for
CTS289
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from datetime import timedelta
import json
from json import JSONEncoder, JSONDecoder
from pathlib import Path
import ast

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
        return f"{self.signin} || {self.signout} || {self.ttotal} || {self.uname} || {self.pid}"

def show_header():
    print("       Sign-in      ||       Sign-out      || Cumulative time in Lab || Name || PIN\n")

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

def pool_save(obj,filename):
    try:
        with open(filename, "w") as f:
            f.write(str(obj))
    except Exception as ex:
        print("Error: ", ex)

def pool_load(filename):
    try:
        with open(filename) as f:
            ser = f.read()
            return set() if ser == str(set()) else ast.literal_eval(ser)
    except Exception as ex:
        print("No file of signed-in names found. Loading an empty list")
        return set()

"""
"""

def clear_entry():
    siname.delete(0, tk.END)
    pidi.delete(0, tk.END)
    soname.delete(0, tk.END)
    pido.delete(0, tk.END)
    monitor.delete('1.0', tk.END) # may end up moving this out

def signin_menu():
    display('signin_menu')
    clear_entry()
    siname.focus()

def signout_menu():
    display('signout_menu')
    clear_entry()
    soname.focus()

def close_win(top):
    top.destroy()

"""https://www.tutorialspoint.com/creating-a-popup-message-box-with-an-entry-field-in-tkinter
"""
def popupwin():
    top= tk.Toplevel()
    top.title("Professor Access")
    top.geometry("200x100")
    top.focus_force()

    ttk.Label(top, text="Enter Password").pack()

    entry= ttk.Entry(top, width= 25, show='*')
    entry.pack()
    entry.focus()

    ttk.Button(top,text= "Enter", command=lambda: admin_check(entry.get(),msg_label,top)).pack(pady=5,side=tk.TOP)
    top.bind('<Return>', lambda event: admin_check(entry.get(),msg_label,top)) # https://coderslegacy.com/python/tkinter-key-binding/
    msg_label = ttk.Label(top,text='')
    msg_label.pack()

def admin_check(pwd, msg_label, top,):
    if pwd == "9987": #change to what client wants
        close_win(top)
        display('admin_menu')
        clear_entry()
    else:
        msg_label.config(text="Error: retry password")

# creates window
root=tk.Tk()

# titles window
root.title('ADN Lab Sign-in Sheet')

root.geometry('640x480+50+50')

# places a label on the root window
message = ttk.Label(root, text="Nursing Lab Sign-in Program\n").pack()

#experimenting v
"""Main Menu
"""
main_menu = ttk.Frame(root)
ttk.Button(main_menu, text='Sign-in', command=signin_menu).pack(pady=1, padx=1)
ttk.Button(main_menu, text='Sign-out', command=signout_menu).pack(pady=1, padx=1)
ttk.Button(main_menu, text='Professor', command=popupwin).pack(pady=3,padx=3,side=tk.BOTTOM, anchor=tk.E)

"""Signin menu
"""
signin_menu = ttk.Frame(root)
ttk.Button(signin_menu, text='<- Back', command=lambda: display('')).pack(padx=2,pady=1,side=tk.TOP, anchor=tk.W)
ttk.Label(signin_menu, text="Sign-in").place(anchor='n', relx=0.5)
ttk.Label(signin_menu, text='Name').pack(side=tk.TOP)
siname = ttk.Entry(signin_menu)
siname.pack()
siname.focus()
ttk.Label(signin_menu, text='PIN/Password').pack()
pidi = ttk.Entry(signin_menu, show='*')
pidi.pack()
ttk.Button(signin_menu, text='Sign-in', command=lambda: print(f'{siname.get()} signed in')).pack(pady=5)
siname.bind('<Return>', lambda event: print(f'{siname.get()} signed in'))
pidi.bind('<Return>', lambda event: print(f'{siname.get()} signed in'))

"""Signout menu
"""
signout_menu = ttk.Frame(root)
ttk.Button(signout_menu, text='<- Back', command=lambda: display('')).pack(pady=3,side=tk.TOP, anchor=tk.W)
ttk.Label(signout_menu, text="Sign-out").place(anchor='n', relx=0.5)
ttk.Label(signout_menu, text='Name').pack()
soname = ttk.Entry(signout_menu)
soname.pack()
soname.focus()
ttk.Label(signout_menu, text='PIN/Password').pack()
pido = ttk.Entry(signout_menu, show='*')
pido.pack()
ttk.Button(signout_menu, text='Sign-out', command=lambda: print(f'{soname.get()} signed-out')).pack(pady=5)
soname.bind('<Return>', lambda event: print('enter'))
pido.bind('<Return>', lambda event: print('enter'))

"""Admin menu
"""
admin_menu = ttk.Frame(root)
admin_menu.columnconfigure(0, weight=1, minsize=150)
admin_menu.columnconfigure(1, weight=3)
ttk.Button(admin_menu, text='<- Back', command=lambda: display('')).grid(sticky='nesw',column=0, row=0)
ttk.Button(admin_menu, text='Show signed in names', command='' ).grid(column=0, row=1, sticky='nesw')
ttk.Button(admin_menu, text='Show Log', command=lambda: log_print(pool)).grid(column=0, row=2, sticky='nesw')
ttk.Button(admin_menu, text='Search log for name', command='' ).grid(column=0, row=3, sticky='nesw')
ttk.Button(admin_menu, text='Show final entry for\n each user', command='' ).grid(column=0, row=4, sticky='nesw')
ttk.Button(admin_menu, text='Save log to text file', command='' ).grid(column=0, row=5, sticky='nesw')

monitor = ScrolledText(admin_menu)
monitor['state'] = 'disabled'
monitor.grid(column=1,row=1,rowspan=4)

uname = ttk.Entry(admin_menu)
uname.grid(column=1, row=0)
ttk.Label(admin_menu, text='Name Entry').grid(column=1, row=0, sticky='w', padx=90)


def display(frame):
    if frame == '':
        print("main menu")
        signin_menu.pack_forget()
        signout_menu.pack_forget()
        admin_menu.pack_forget()
        clear_entry()
        return main_menu.pack(expand=True,fill=tk.BOTH)
    if frame == 'signin_menu':
        print("signin menu")
        main_menu.pack_forget()
        return signin_menu.pack(expand=True,fill=tk.BOTH)
    if frame == 'signout_menu':
        print('signout menu')
        main_menu.pack_forget()
        signin_menu.pack_forget()
        return signout_menu.pack(expand=True,fill=tk.BOTH)
    if frame == 'admin_menu':
        print("admin menu")
        main_menu.pack_forget()
        return admin_menu.pack(expand=True,fill=tk.BOTH)


def main():
    display('')
    u0=Login("Shade","0303",datetime.now().replace(microsecond=0),datetime.now().replace(microsecond=0)+timedelta(hours=3),timedelta(hours=3))
    log=list((initialize_log('log.json',u0))) # initialize log list
    pool=set(pool_load("pool.json")) # initialise the set of signed in names

    # keep the window displaying
    root.mainloop()

main()
