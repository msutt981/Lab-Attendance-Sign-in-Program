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
import string

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
        return f"{self.signin} || {self.signout} ||   {self.ttotal}  || {self.uname_col()} || {self.pid}"

    def uname_col(self):
        ulen = len(self.uname)
        if ulen < 17:
            whitespace = 16 - ulen
            space = " "
            spacer = space*whitespace
            final = str(f'{self.uname}{spacer}')
            return final
        else:
            return self.uname

def find_previous(log,uname):
    for i in reversed(log):
        if i.uname == uname:
            return i
# find last instance of uname in the log and return that instance

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

def save_object(obj,filename):
    try:
        with open(filename, "w") as f: #check what all the letter modifiers do
            json.dump([ob.__dict__ for ob in obj], f, cls=DateTimeAwareJSONEncoder, indent=4)
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
            f.write(f"       Sign-in      ||       Sign-out      || Total time in Lab || Name      || PIN\n")
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
def close_win(top): # ended up not using. remove when cleaning up if still not needed
    top.destroy()

"""https://www.tutorialspoint.com/creating-a-popup-message-box-with-an-entry-field-in-tkinter
"""
def popupwin(app):
    top= tk.Toplevel()
    top.title("Professor Access")
    top.geometry("200x100")
    top.focus_force()

    ttk.Label(top, text="Enter Password").pack()

    entry= ttk.Entry(top, width= 25, show='*')
    entry.pack()
    entry.focus()

    ttk.Button(top,text= "Enter", command=lambda: admin_check(entry.get(),msg_label,top, app)).pack(pady=5,side=tk.TOP)
    top.bind('<Return>', lambda event: admin_check(entry.get(),msg_label,top, app)) # https://coderslegacy.com/python/tkinter-key-binding/
    msg_label = ttk.Label(top,text='')
    msg_label.pack()

def admin_check(pwd, msg_label, top, app):
    if pwd == "9987": #change to what client wants
        close_win(top)
        app.goto_adminmenu()
        app.clear_entry()
    else:
        msg_label.config(text="Error: retry password")

"""Main Menu
"""
class Main_menu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()
        self.container = container
        self.style = ttk.Style(self)
        #self.style.configure('TFrame', background='#fbceb1')
        self.style.configure('big.TButton', font=(None, 20))

    def __create_widgets(self):
        ttk.Label(self, text="").pack(ipady=60)
        ttk.Button(self, text='Sign-in', style='big.TButton', command=lambda: self.container.goto_signin()).pack(pady=1, padx=1, anchor=tk.CENTER)
        ttk.Button(self, text='Sign-out', style='big.TButton', command=lambda: self.container.goto_signout()).pack(pady=1, padx=1, anchor=tk.CENTER)
        ttk.Button(self, text='Professor', command=lambda: popupwin(self.container)).pack(pady=3,padx=3,side=tk.BOTTOM, anchor=tk.E)
        ttk.Label(self, text="").pack()

    def add_msg(self,txt):
        alist = []
        alist.append(ttk.Label(self, text=txt, justify='center', font=("None",15)))
        alist[0].pack()
        self.after(5000,lambda: alist[0].destroy())


"""Signin menu
"""
class Signin_menu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.container = container
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Button(self, text='<- Back', command=lambda: self.container.goto_mainmenu()).pack(padx=2,pady=1,side=tk.TOP, anchor=tk.W)
        self.header = ttk.Label(self, text="Sign-in", font=('None', 15))
        self.header.place(anchor='n', relx=0.5) # fix this so when it changes it looks better
        ttk.Label(self, text='Name').pack(side=tk.TOP)
        self.siname = ttk.Entry(self, font=("None",20))
        self.siname.pack()
        self.siname.focus()
        ttk.Label(self, text='PIN/Password').pack()
        self.pidi = ttk.Entry(self, show='*', font=("None",20))
        self.pidi.pack()
        ttk.Button(self, text='Sign-in', command=lambda: self.sign_in(self.container.pool,self.container.log)).pack(pady=5)
        self.footer = ttk.Label(self, text='', font=("none",15))
        self.footer.pack()
        self.siname.bind('<Return>', lambda event: self.sign_in(self.container.pool,self.container.log))
        self.pidi.bind('<Return>', lambda event: self.sign_in(self.container.pool,self.container.log))

    def sign_in(self, pool, log):
        self.footer.config(text="")
        uname= string.capwords(self.siname.get())
        pid=self.pidi.get()
        if uname in pool:
            self.footer.config(text = 'The name you have entered is already signed into the lab')
            return
        if uname == '':
            self.footer.config(text = 'Please enter your name')
            return
        if pid == "":
            self.footer.config(text = 'Please enter (and remember) your PIN/Password. It will be required to sign-out.')
            return
        now = datetime.now().replace(microsecond=0)
        index = find_previous(log,uname)
        if index != None:
            u1 = Login(uname,pid,now,'         -         ',index.ttotal+timedelta(minutes=0))
        else:
            u1 = Login(uname,pid,now,'         -         ',timedelta(minutes=0))
        pool.add(u1.uname)
        pool_save(pool,"pool.json")
        log.append(u1)
        save_object(log,"log.json")
        self.container.goto_mainmenu()
        self.container.main_menu.add_msg(f'{uname} signed in at {now}.')

        
"""Signout menu
"""
class Signout_menu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()
        self.container = container

    def __create_widgets(self):
        ttk.Button(self, text='<- Back', command=lambda: self.container.goto_mainmenu()).pack(pady=3,side=tk.TOP, anchor=tk.W)
        self.header = ttk.Label(self, text="Sign-out", font=('None', 15))
        self.header.place(anchor='n', relx=0.5)
        ttk.Label(self, text='Name').pack()
        self.soname = ttk.Entry(self, font=("None",20))
        self.soname.pack()
        self.soname.focus()
        ttk.Label(self, text='PIN/Password').pack()
        self.pido = ttk.Entry(self, show='*', font=("None",20))
        self.pido.pack()
        ttk.Button(self, text='Sign-out', command=lambda: self.sign_out(self.container.pool,self.container.log)).pack(pady=5)
        self.footer = ttk.Label(self, text="", font=("none",15))
        self.footer.pack()
        self.soname.bind('<Return>', lambda event: self.sign_out(self.container.pool,self.container.log))
        self.pido.bind('<Return>', lambda event: self.sign_out(self.container.pool,self.container.log))

    def sign_out(self, pool, log):
        self.footer.config(text='')
        uname = string.capwords(self.soname.get())
        if uname not in pool:
            self.footer.config(text="The name you entered was not signed into the lab")
            return
        now = datetime.now().replace(microsecond=0)
        index = find_previous(log,uname)
        pid = self.pido.get()
        if pid == "":
            self.footer.config(text="Please enter PIN/Password you used to sign-in")
            return
        if pid != index.pid:
            self.footer.config(text="Personal PIN/password didn't match signin. Please try again.")
            return
        u1 = Login(uname,pid,index.signin,now,(now-index.signin)+index.ttotal)
        pool.remove(u1.uname)
        pool_save(pool,"pool.json")
        log.append(u1)
        save_object(log,"log.json")
        self.container.goto_mainmenu()
        self.container.main_menu.add_msg(f'{uname} signed out at {now}.\nHave a nice day.')

"""Admin menu
"""
class Admin_menu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1, minsize=150)
        self.columnconfigure(1, weight=4, minsize=300)

        self.__create_widgets()
        self.container = container

    def __create_widgets(self):
        ttk.Button(self, text='<- Back', command=lambda: self.container.goto_mainmenu()).grid(sticky='nesw',column=0, row=0)
        ttk.Button(self, text='Show signed in names', command=lambda: self.print_pool()).grid(column=0, row=1, sticky='nesw')
        ttk.Button(self, text='Show Log', command=lambda: self.print_log()).grid(column=0, row=2, sticky='nesw')
        ttk.Button(self, text='Search log for name', command=lambda: self.search_log()).grid(column=0, row=3, sticky='nesw')
        ttk.Button(self, text='Show final entry for\n each user', command=lambda: self.show_final()).grid(column=0, row=4, sticky='nesw')
        ttk.Button(self, text='Save log to text file', command=lambda: log_save(self.container.log, "log.txt")).grid(column=0, row=5, sticky='nesw')

        self.monitor = ScrolledText(self, width=300)
        self.monitor.grid(column=1,row=1,rowspan=4)

        self.search_frame = Container_frame(self)

        ttk.Label(self.search_frame, text='Search Name').pack(side=tk.LEFT, padx=5)
        self.uname = ttk.Entry(self.search_frame, width = 22) # width was 55
        self.uname.pack(side=tk.LEFT, padx=5)
        self.uname.bind('<Return>', lambda event:self.search_log())

        self.udate = ttk.Entry(self.search_frame, width = 12)
        ttk.Label(self.search_frame, text='| OR |  Search Date').pack(side=tk.LEFT, padx=5)
        self.udate.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.search_frame, text='Date Search', command=lambda: self.search_date()).pack()
        self.udate.bind('<Return>', lambda event:self.search_date())
        self.search_frame.grid(column=1, row=0)

    def print_mon(self,txt):
        #self.container.admin_menu.monitor.delete('1.0', tk.END)
        i=2
        for x in txt:
            self.monitor.insert(f'{i}.0', f'{x}\n')
            i+=1

    def print_log(self):
        self.container.admin_menu.monitor.delete('1.0', tk.END)
        self.monitor.insert('1.0', "       Sign-in      ||       Sign-out      || Total time in Lab || Name      || PIN\n")
        i = 2
        for x in self.container.log:
            self.monitor.insert(f'{i}.0', f'{x}\n')
            i+=1

    def print_pool(self):
        self.container.admin_menu.monitor.delete('1.0', tk.END)
        if self.container.pool == set():
            self.monitor.insert('1.0', "No names signed in")
        else:
            i=1
            for x in self.container.pool:
                self.monitor.insert(f'{i}.0', f'{x}\n')
                i+=1

    def search_log(self):
        self.container.admin_menu.monitor.delete('1.0', tk.END)
        i=2 # might not be required anymore. check and clean
        alist = []
        uname = self.uname.get()
        for x in self.container.log:
            if (uname.lower() in x.uname.lower()) and uname != "": # remove 'and' to : to have blank entry show full log
                alist.append(x)
        if len(alist) > 0:
            self.monitor.insert('1.0', "       Sign-in      ||       Sign-out      || Total time in Lab || Name      || PIN\n")
            self.print_mon(alist)
        else:
            self.monitor.insert('1.0', "No results found.")

    def search_date(self):
        self.container.admin_menu.monitor.delete('1.0', tk.END)
        i=2 # might not be required anymore. check and clean
        alist = []
        uname = self.udate.get()
        for x in self.container.log:
            if uname in x.signin.strftime("%Y-%m-%d") and uname != "": # going to need to seperate this into various searches? Well, use of dashes makes it not need multi searches. add to documentation
                alist.append(x)
        if len(alist) > 0:
            self.monitor.insert('1.0', "       Sign-in      ||       Sign-out      || Total time in Lab || Name      || PIN\n")
            self.print_mon(alist)
        else:
            self.monitor.insert('1.0', "No results found.")

    def show_final(self):
        self.container.admin_menu.monitor.delete('1.0', tk.END)
        self.monitor.insert('1.0', "       Sign-in      ||       Sign-out      || Total time in Lab || Name      || PIN\n")
        alist=[]
        uuname=set()
        for x in reversed(self.container.log):
            if x.uname not in uuname:
                uuname.add(x.uname)
                alist.append(x)
        self.print_mon(alist)

"""container frame
"""
class Container_frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

"""App
"""
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ADN Lab Sign-in Sheet')
        self.geometry('900x520+50+50')
        ttk.Label(self, font=('None', 20), text="Nursing Lab Sign-in\n", anchor=tk.S).pack(ipadx=5, ipady=5, pady=0)
        self.configure(bg = '#fbceb1') # a splash of color
        #self.style = ttk.Style(self)
        #self.style.configure('TLabel', background='#fbceb1')
        #self.style.configure('TFrame', background='#fbceb1')

        self.u0=Login("Shade","0303",datetime.now().replace(microsecond=0),datetime.now().replace(microsecond=0)+timedelta(hours=3),timedelta(hours=3))
        self.log=list((initialize_log('log.json',self.u0))) # initialize log list
        self.pool=set(pool_load("pool.json")) # initialise the set of signed in names

        self.__create_widgets()
        self.show_mainmenu()
        

    def __create_widgets(self):
        self.main_menu = Main_menu(self)
        self.signin_menu = Signin_menu(self)
        self.signout_menu = Signout_menu(self)
        self.admin_menu = Admin_menu(self)

    def show_mainmenu(self):
        self.main_menu.pack(expand=True,fill=tk.BOTH)

    def hide_mainmenu(self):
        self.main_menu.pack_forget()

    def show_signinmenu(self):
        self.signin_menu.pack(expand=True,fill=tk.BOTH)

    def hide_signinmenu(self):
        self.signin_menu.pack_forget()

    def show_signoutmenu(self):
        self.signout_menu.pack(expand=True,fill=tk.BOTH)

    def hide_signoutmenu(self):
        self.signout_menu.pack_forget()

    def show_adminmenu(self):
        self.admin_menu.pack(expand=True,fill=tk.BOTH)

    def hide_adminmenu(self):
        self.admin_menu.pack_forget()

    def goto_signin(self):
        self.hide_mainmenu()
        self.show_signinmenu()
        self.signin_menu.footer.config(text = "")
        self.signin_menu.siname.focus()

    def goto_mainmenu(self):
        self.hide_signinmenu()
        self.hide_signoutmenu()
        self.hide_adminmenu()
        self.clear_entry()
        self.show_mainmenu()

    def goto_signout(self):
        self.hide_mainmenu()
        self.show_signoutmenu()
        self.signout_menu.footer.config(text = "")
        self.signout_menu.soname.focus()

    def goto_adminmenu(self):
        self.hide_mainmenu()
        self.show_adminmenu()
        self.admin_menu.uname.config(text = "")
        self.admin_menu.uname.focus()

    def clear_entry(self):
        self.signin_menu.siname.delete(0, tk.END)
        self.signin_menu.pidi.delete(0, tk.END)
        self.signout_menu.soname.delete(0, tk.END)
        self.signout_menu.pido.delete(0, tk.END)
        self.admin_menu.monitor.delete('1.0', tk.END)

def main():
    u0=Login("Shade","0303",datetime.now().replace(microsecond=0),datetime.now().replace(microsecond=0)+timedelta(hours=3),timedelta(hours=3))
    #log=list((initialize_log('log.json',u0))) # initialize log list
    #pool=set(pool_load("pool.json")) # initialise the set of signed in names
    app = App()
    
    # keep the window displaying
    #root.mainloop()
    app.mainloop()

if __name__ == "__main__":
    main()
