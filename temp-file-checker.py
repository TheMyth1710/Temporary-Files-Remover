import json, os, subprocess, logging
from datetime import datetime as dt
from datetime import timedelta as td
try:
        
    logging.basicConfig(filename='logs.log', format='%(levelname)s:\n%(message)s', encoding='utf-8', level=logging.DEBUG)
    date_format = dt.now().strftime('%D, %H:%M:%S')
except:
    pass
def open_json():
    with open("data.json", "r") as f:
        data = json.load(f)
        keys = ["folder_name", "folder_location", "directory", "delDelay"]
        if set(data.keys()) == set(keys):
            folder_name = data["folder_name"]
            for i in ['\\','/',':','*','?','"','<','>','|']:
                if i in folder_name:
                    logging.debug(f"Restored the default folder_name.\nOld: {folder_name}\nCurrent: temp-files\nTime: {date_format}\n")
                    data["folder_name"] = "temp-files"
                    folder_name = "temp-files"
                    f.close()
                    with open("data.json", "w") as f:
                        json.dump(data, f)
                        f.close()
            if data["directory"] == "" and "Downloads" not in data["directory"]:
                driveNames = str(subprocess.check_output('fsutil fsinfo drives'))
                drives = driveNames.split() 
                del drives[0], drives[-1]
                drives.insert(0,drives[0]+"Users\\"+os.getlogin()+"\\Downloads")
                data["directory"] = drives
                f.close()
                with open("data.json", "w") as f:
                    json.dump(data, f)
                    f.close()
            else:
                drives = data["directory"]
        else:
            folder_name = "temp-files"
            driveNames = str(subprocess.check_output('fsutil fsinfo drives'))
            drives = driveNames.split() 
            del drives[0], drives[-1]
            drives.insert(0,drives[0]+"Users\\"+os.getlogin()+"\\Downloads")
            f.close()
            with open("data.json", "w") as f:
                json.dump({"folder_name": folder_name, "folder_location": "", "directory": drives, "delDelay": "86400"}, f)
                f.close()            
            logging.debug(f"Restored the default data.json blueprint.\nTime: {date_format}\n")
    return drives, folder_name


class Find():
    def __init__(self, drive, folder_name):
        self.drive = drive
        self.folder_name = folder_name
        pass
    def find_folder(self, rootdir, target):
        file = open("data.json", "r")
        data = json.load(file)
        file.close()
        file = open("data.json", "w")
        if type(rootdir) == list:
            for r in rootdir:
                for path, dirnames, filnames in os.walk(r):
                    for dirname in dirnames:
                        full_path = os.path.join(path, dirname)
                        if target in full_path and 'Recycle.Bin' not in full_path:
                            data["folder_location"] = full_path
                            json.dump(data, file)
                            file.close()
                            return full_path
        else:
            for path, dirnames, filnames in os.walk(rootdir):
                for dirname in dirnames:
                    full_path = os.path.join(path, dirname)
                    if target in full_path:
                        data["folder_location"] = full_path
                        json.dump(data, file)
                        file.close()
                        return full_path     
        return None      
            
    def find_item(self, rootdir, target):
        f = open("data.json", "r")
        data = json.load(f)
        if os.path.isdir(data["folder_location"]):
            location = data["folder_location"]
            if location is None or location=="":
                return None
            items = [f"{location}\\{o}" for o in os.listdir(path=location)]               
        else:
            instance = Find(rootdir, target)
            location = instance.find_folder(rootdir, target)
            if location is None:
                return None
            items = [f"{location}\\{o}" for o in os.listdir(path=location)]
        f.close()
        for i in items:
            i = i.split('\\')[-1]
            if '.' not in i and not os.path.isfile(i):
                sub_items = os.listdir(path=f"{location}\\{i}")
                for s in sub_items:
                    sub_items[sub_items.index(s)] = f"{location}\\{i}\\{s}"
                items += sub_items
        return items

def time_check(items):
    times = {}
    for file in items:
        times[file] = dt.fromtimestamp(os.path.getmtime(file))
    return times
count = 0
def combine():
    global count
    info = open_json()
    instance = Find(info[0], info[1])
    items = instance.find_item(info[0], info[1])
    if items is None and count == 0:
        times = None
        count += 1
        logging.error(f"No directory found with the name '{info[1]}'\nTime: {date_format}\n")
    else:
        times = time_check(items)
        with open('data.json', 'r') as f:
            data = json.load(f)
            delay_1 = data["delDelay"]
            try: 
                delay = float(delay_1)
            except:
                delay = 86400
                extra_info = f"A proper format for delDelay in seconds wasn't entered. A default value of 86400s has been restored.\nValue Entered: {delay_1}\n"
                logging.warning(extra_info+f"Time: {date_format}\n")
                data["delDelay"] = delay
                f.close()
                with open("data.json", "w") as f:
                    json.dump(data, f)
                    f.close()
        return times, delay

def final():
    if __name__ == "__main__":
        global count
        logging.info(f"The temp-file-checker file is now on and working. All logs will come up here!\nTime: {date_format}\n")
        while True:
            try:
                combine_all = combine()
                times = combine_all[0]
                delay = combine_all[1]
                if times is not None:
                    for j, k in times.items():
                        time_passed = dt.now() - td(seconds=delay)
                        if time_passed >= k and '.' in j and os.path.isfile(j):
                            if os.path.exists(j):
                                os.remove(j)
                                logging.critical(f"File Removed: {j}\nDate Modified: {k.strftime(date_format)}\nDate Deleted: {date_format}\n")   
                                count = 0     
            except:
                pass
final()
