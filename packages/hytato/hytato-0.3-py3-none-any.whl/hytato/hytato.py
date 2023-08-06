import ast; import os; import sys; from zipfile import ZipFile, ZipInfo; import warnings; import inspect; import platform; import multiprocessing; import time
'''
Hyphens Potato is a module allowing you (more me) to store dictionaries in a way that I (yes I) would like.
I needed a middle ground between a database and json, in addition to it being light, powerful, and just simple
to interact with (for me). Main thing is probably to not lose your data while using files as a near db

Because of that last one, this is mainly for windows, but supports linux
OS is only important if you use HTATO though. Since file locking was difficult for zip archives, which is what
STATO files actually are. STATO uses a flag file inside to indicate some other process is inside. There is a 
timeout on the file though. If a process wait for more than 5 seconds (too much time in computer terms) then it
ignores it carries on. This only affects inject operations btw. Any read operations in stato do not give regard 
to the flag.
I would very much prefer STATO also use msvcrt & fcntl filelocks. The issue I faced was with file descriptors.
If someone has a suggestion on getting file descriptors from zip files hmu pls!

HTATO stands for HARD POTATO. These files must be created by the HTATO class, and has fixed keys.
Meaning you can not easily add a new key to it. This makes it more suitable for files storing the 
permanent data like status or settings.

STATO stands for SOFT POTATO. These can have a variable number of keys. Making it more suitable
for files that might be used to store temporary data.

Apart from the number of keys, HTATO and STATO have other characteristics that make it suitable for their use

.potato files are for use by potato lib only (!)
'''

system_os = platform.uname().system
if system_os == 'Windows':
    import msvcrt
    def lock_file(file_descriptor: int, file_path: str):
        msvcrt.locking(file_descriptor, msvcrt.LK_LOCK, os.path.getsize(file_path))

    def unlock_file(file_descriptor: int, file_path: str):
        msvcrt.locking(file_descriptor, msvcrt.LK_UNLCK, os.path.getsize(file_path))

elif system_os == 'Linux':
    import fcntl
    def lock_file(file_descriptor: int, file_path: str):
        fcntl.flock(file_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def unlock_file(file_descriptor: int, file_path: str):
        fcntl.flock(file_descriptor, fcntl.LOCK_UN)

elif bool(system_os) == False:
    warnings.warn('Platform module could not get system os. Hytato will not load')
    sys.exit()
else:
    warnings.warn('Platform module reported an unsupported os. Hytato will not load')
    sys.exit()

version_major = int(sys.version_info.major)
version_minor = int(sys.version_info.minor)

# Exceptions:

class POTATOExists(Exception):
    """Exception for when the specified potato file (whether hard or soft) already exists in the directory"""
class POTATONonExists(Exception):
    """Exception for when the specified potato file (whether hard of soft) doesn't exist in the directory"""
class NotHTATO(Exception):
    """Exception for when the path passed in class is not an HTATO file"""
class NotSTATO(Exception):
    """Exception for when the path passed in class is not an STATO file"""
class HTATOKey(KeyError):
    """Exception for when the key in data is not part of the original HTATO file"""
class InvalidSTARCH(Exception):
    """Exception for when the starch type is not supported for the method"""

# Decorators:

def CheckPotatoExistant(fn):
    """must have self parameter and the potato path inside self parameter: self.potato"""
    def func(*args, **kwargs):
        if os.path.exists(args[0].potato) == True:
            raise POTATOExists('Found existing potato file at path')
        return fn(*args, **kwargs)
    return func

def CheckPotatoNonExistant(fn):
    """must have self parameter and the potato path inside self parameter: self.potato"""
    signature = inspect.signature(fn)
    def func(*args, **kwargs):
        if os.path.exists(args[0].potato) == False:
            if signature.parameters.get('plant_if_non_existant'):
                args[0].PLANT(KEYS=list(kwargs['data'].keys()))
                warnings.warn('Did not find existing potato file at path. Created one for you')
            else:
                raise POTATONonExists('Did not find existing potato file at path')
        return fn(*args, **kwargs)
    return func

# Return classes:

class potato_returns():
    class stato():
        class StatoPlantReturn():
            def __init__(self, complete, path, keys, version_history, encryption):
                self.complete = complete
                self.path = path
                self.keys = keys
                self.version_history = version_history
                self.encryption = encryption

        class StatoInjectReturn():
            def __init__(self, complete, update, all):
                self.complete = complete
                self.update = update
                self.all = all

    class htato():
        class HtatoPlantReturn():
            def __init__(self, complete, path, keys):
                self.complete = complete
                self.path = path
                self.keys = keys

        class HtatoInjectReturn():
            def __init__(self, complete, update, all):
                self.complete = complete
                self.update = update
                self.all = all

# All Hail Potato:

class POTATO():
    class STATO():
        def __init__(self, potato: str) -> None:
            """STATO stands for SOFT POTATO. These can have a variable number of keys. Making it more suitable for files that might be used to store temporary data."""

            self.potato = os.path.realpath(potato)
            filename = os.path.basename(self.potato).split('.')
            if filename[len(filename)-1] != 'stato':
                raise NotSTATO('Not an STATO file')

        @CheckPotatoExistant
        def PLANT(self, KEYS: list, version_history: bool = True, encryption: bool = False) -> potato_returns.stato.StatoPlantReturn:
            """Creates a STATO file at the path and adds None to all keys. Users must update the keys using INJECT method.\n
            returns a StatoPlantReturn class with parameters: complete, path, keys, version_history, encryption"""

            if encryption == True:
                print('Encryption is not currently fully supported')
            configfile_string = str()
            configfile_string += 'version_history: {}'.format(version_history) + '\n'
            configfile_string += 'encryption: {}'.format(encryption) + '\n'
            potatofile_string = str()
            for x in KEYS:
                potatofile_string += '{}: None'.format(x) + '\n'

            ZipFile(self.potato, 'x').close()
            with ZipFile(self.potato, 'a') as zipfile:
                zipfile.writestr(data=configfile_string, zinfo_or_arcname='config.potato')
                zipfile.writestr(data=potatofile_string, zinfo_or_arcname='data.potato')
                zipfile.writestr(data='', zinfo_or_arcname='version_history/')
                zipfile.close()

            return potato_returns().stato().StatoPlantReturn(complete=True, path=self.potato, keys=KEYS, version_history=version_history, encryption=encryption)

        @CheckPotatoNonExistant
        def STAIN(self, starch: str = 'data', decryption_key: str = None) -> dict:
            """Reads STATO file. Starch specifies what part you want to read.\n
            Type 'data' (default) for the simple dictionary stored inside, or 'config' for the preferences set during planting. 'history' is not yet supported\n
            returns a dictionary with keys and values of python objects"""

            if starch == 'data':
                starch = 'data.potato'
            if starch == 'config':
                starch = 'config.potato'
            if starch == 'history':
                starch = 'version_history/'

            with ZipFile(self.potato, 'r') as zipfile:
                read = zipfile.read(name=starch).decode().split('\n')
                zipfile.close()

            parsed = dict()
            for x in read:
                if bool(x): #since its not .readlines() we need to make sure the string actually has something
                    x = x.replace("\n", "").split(':')  # unlikely to have "\n" in the string now but eh
                    key = x[0].strip()
                    value = ast.literal_eval(x[1].strip())
                    parsed[key] = value

            return parsed

        @CheckPotatoNonExistant
        def INJECT(self, *, data: dict, starch: str = 'data', plant_if_non_existant: bool = True) -> potato_returns.stato.StatoInjectReturn:
            """Update the data in the potato file at the path. Starch specifies the part you want to edit.\n
            Type 'data' (default) for the simple dictionary stored inside, or 'config' for the preferences set during planting. 'history' is not yet supported
            returns a StatoInjectReturn class with parameters: complete, update, all"""

            if starch == 'data':
                starch = 'data.potato'
            if starch == 'config':
                starch = 'config.potato'
            if starch == 'history':
                raise InvalidSTARCH('This starch is not supported for this method')

            #generate potato file string
            data_stained = self.STAIN(starch='data')
            old_data = data_stained     #useful in version history
            if starch == 'data.potato':
                for x in data.keys():
                    data_stained[x] = data[x]
            potatofile_string = str()
            for x in data_stained.keys():
                key = x
                value = data_stained[key]
                if type(value) == str:
                    value = '"{}"'.format(value)
                potatofile_string += '{}: {}'.format(key, value) + '\n'

            #generate config file string
            config_stained = self.STAIN(starch='config')
            if starch == 'config.potato':
                for x in data.keys():
                    config_stained[x] = data[x]
            configfile_string = str()
            for x in config_stained.keys():
                key = x
                value = config_stained[key]
                if type(value) == str:
                    value = '"{}"'.format(value)
                configfile_string += '{}: {}'.format(key, value) + '\n'

            #get history as a dict
            with ZipFile(self.potato, 'r') as zipfile:
                namelist = zipfile.namelist()
                history = dict()
                version_history_namelist = list()

                for x in namelist:
                    if x.startswith('version_history/'):
                        if bool(x.split('/')[1]):
                            name = x.split('/')[1]
                            index = int(name.split('.')[0])
                            version_history_namelist.append(index)
                            content = zipfile.read(x).decode().replace("\r", "") #for some reason there is also \r ending on new lines along with \n. Need to remove it otherwise new lines will increase on each write
                            history[x] = content    #adding x because it includes the folder

                if config_stained['version_history'] == True:
                    if bool(version_history_namelist):
                        version_history_namelist.sort()
                        index = version_history_namelist[len(version_history_namelist)-1] + 1
                    else:
                        index = int(1)
                    oldpotatofile_string = str()
                    for x in old_data.keys():
                        key = x
                        value = old_data[key]
                        if type(value) == str:
                            value = '"{}"'.format(value)
                        oldpotatofile_string += '{}: {}'.format(key, value) + '\n'
                    history['version_history/{}.txt'.format(index)] = oldpotatofile_string

                zipfile.close()


            flag_file_path = os.path.dirname(self.potato) + '\\' + (os.path.basename(self.potato).split('.')[0] + '.flag')
            green_light = False
            start = time.perf_counter()
            #about 6 - 8 seconds
            for x in range(70000000):
                if os.path.exists(flag_file_path):
                    pass
                else:
                    green_light = True
                    break
            stop = time.perf_counter()
            if green_light == False:
                warnings.warn('The inject method waited {} fractional seconds before ignoring the flag.'.format(stop-start))

            with ZipFile(self.potato, 'w') as zipfile:
                with open(flag_file_path, 'w') as flag_file:
                    flag_file.write(str([multiprocessing.process.current_process(), platform.python_build(), platform.uname()]))
                    flag_file.close()
                zipfile.writestr(data=potatofile_string, zinfo_or_arcname='data.potato')
                zipfile.writestr(data=configfile_string, zinfo_or_arcname='config.potato')
                for x in history.keys():
                    zipfile.writestr(data=history[x], zinfo_or_arcname=x)
                os.remove(flag_file_path)
                zipfile.close()

            return potato_returns.stato.StatoInjectReturn(complete=True, update=data, all=data_stained) #all needs to be edited to account for the starch

    class HTATO():
        def __init__(self, potato: str) -> None:
            """HTATO stands for HARD POTATO. These files must be created by the HTATO class, and has fixed keys. Meaning you can not easily add a new key to it. This makes it more suitable for files storing the permanent data like status or settings."""

            self.potato = os.path.realpath(potato)
            filename = os.path.basename(self.potato).split('.')
            if filename[len(filename)-1] != 'htato':
                raise NotHTATO('Not an HTATO file')

        @CheckPotatoExistant
        def PLANT(self, KEYS: list) -> potato_returns.htato.HtatoPlantReturn:
            """Creates a HTATO file at the path and adds None to all keys. Users must update the keys using INJECT method.\n
            returns a HtatoPlantReturn class with parameters: complete, path, keys"""

            potatofile_string = str()
            for x in KEYS:
                potatofile_string += '{}: None'.format(x) + '\n'
            potatofile = open(self.potato, 'w')
            potatofile.write(potatofile_string)
            potatofile.close()

            return potato_returns().htato().HtatoPlantReturn(complete=True, path=self.potato, keys=KEYS)

        @CheckPotatoNonExistant
        def STAIN(self) -> dict:
            """Reads the potato file at the path. \n
            returns a dictionary with keys and values of python objects"""

            read = open(self.potato, 'r').readlines()
            parsed = dict()
            for x in read:
                # python still sometimes read the \n ending.
                x = x.replace("\n", "").split(':')
                key = x[0].strip()
                value = ast.literal_eval(x[1].strip())
                parsed[key] = value

            return parsed

        @CheckPotatoNonExistant
        def INJECT(self, data: dict) -> potato_returns.htato.HtatoInjectReturn:
            """Update the data in the potato file at the path.\n
            returns a HtatoInjectReturn class with parameters: complete, update, all"""

            stained = self.STAIN()
            for x in data.keys():
                if bool(list(stained.keys()).count(x)) == False:
                    raise HTATOKey('The key: "{}" is not in the original hard potato file.'.format(x))
                stained[x] = data[x]
            potatofile_string = str()
            for x in stained.keys():
                key = x
                value = stained[key]
                if type(value) == str:
                    value = '"{}"'.format(value)
                potatofile_string += '{}: {}'.format(key, value) + '\n'

            potatofile = open(self.potato, 'w')
            lock_file(potatofile.fileno(), self.potato)
            potatofile.write(potatofile_string)
            unlock_file(potatofile.fileno(), self.potato)
            potatofile.close()

            return potato_returns().htato().HtatoInjectReturn(complete=True, update=data, all=stained)