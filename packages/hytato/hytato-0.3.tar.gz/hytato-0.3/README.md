# hytato
Module for storing python dictionaries in a different format.
Supported down to python 3.3.

### why?
cause why not?

Needed a way to store data in a way that fit *my* needs, and so decided to create potato(lib).
Potato works with dictionaries. You could use json for that but as I said, needed something for *my* needs.

### Potato types
There are two different kinds of potato files: HTATO and STATO.

HTATO or hard potato have a fixed number of keys.
STATO or soft potato don't have a fixed number of keys.

There are a number of other differences which will be made clearer in the future.
One difference being that STATO files are inherently different. The HTATO files are really just `.txt`, whereas STATO are zip files.
This means you can store a "tree" of data, and also version history

### Usage
HTATO example:

```
from hytato import POTATO

#Add the path of the potato file in HTATO class, which will have either the .htato or .stato file extension.
config_potato = POTATO.HTATO('.\\config.htato')

#if it doesn't exist yet, create the potato file
#add the list of keys you want
config_potato.PLANT(['token', 'passcode', 'fatherless'])

#when the potato has been planted, the values to the keys will all be none, so now add the data

config_potato.INJECT({'token': 112233, 'passcode': 'gugugaga', 'fatherless': True})

#if it succeeded, it won't raise an error lol
#but you can also assign it to a variable beforehand
#and then check from the class returned
#i.e:

injection = config_potato.INJECT({'token': 112233, 'passcode': 'gugugaga', 'fatherless': True})
if injection.complete == True:
    print('yipee')

#to access the data from potato, use the stain method:
config = config_potato.STAIN()
#and just use the dictionary it returns
token = config.get('token')
```
