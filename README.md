This is a digital replacement for a clipboard sign-in sheet that will auto calculate time spent in the lab. This program is for a course project.

## Install
1. Python needs to be installed to run the program.
2. Download the gui.py file and place it in a folder that has write premissions (files will be created by the program)
3. Change the name of gui.py to `anythingyouwant.pyw` (the name of the file is unimportant, but make sure the extension is pyw)
4. You can now run the .pyw file. The program will generate and save the log and pool files as needed.

## Options
- The default professor password is 9987. To change it, edit the .pyw file and search for 9987 and change it to whatever you would like it to be. Just make sure it is still between the `"`s ie: `"the changed password"`

## Sign-in/out usage
- Sign-in/out names are case insensitive. They should be automatically initial capitalized as one would expect names to be.
- The pin/password is more of a signature and not an authorization lock out. It is also stored in plaintext so shouldn't be a password used elsewhere or something that shouldn't be seen by any number of people authorized to view the log (professors, auditors, ect.). It is used so that someone else cannot accidentally, or purposefully, sign-out someone else and to "sign" that you **are** the person who signed in. Students chosen password should be emailed to the professor (or however the professor wishes to recieve it) so sign-ins can be personally validated in the log.
- One cannot sign-in if they are already signed in, and one cannot sign-out if they are not currently signed-in.
- To sign-out one must input the pin/password they input when they signed in. This is why it is **vital** that it be remembered and input carefully.

## Professor Operations
- **Show signed in names**: Displays a list of all signed in names. 
  - Recommended to use this at the end of the day or after students have left the lab to check if anyone forgot to sign-out. The professor will have to decide how to handle this event. The easiest way to resolve this is to delete the pool.json file (making sure that only studnts who forgot to log out are signed-in). This will allow them to sign-in the next time they enter the lab. This doesn't add time for when they forgot to log out and retains their sign-in on the log so it can be seen that they forgot to sign-out. This also doesn't add any time from the session where they forgot to sign-out.
- **Show Log**: displays the full log
- **Search log for name**: Searches the log for the name typed in the Search Name text box. One can also just press enter after typing a name in the box to search without pressing the button.
- **Date Search**: One can also search by date using the Search Date text box. Like the name search, you can press enter after typing the box to search. Searches should be input like the date is displayed. ie: `-01-` to search all January dates; `-02-18` to search for entries on February 18th; or `2023-01-30` to search for entries specifically on January 30th of 2023.
- **Show final entry for each user**: This will display the last entry for each unique sign-in name. This is useful for quickly seeing all the student's final amount of time spent in the lab.
- **Save log to text file**: This saves the whole log to a text file with the date and time .log.txt as its filename. This is for backup purposes and in case the log needs to be sent to another party.


