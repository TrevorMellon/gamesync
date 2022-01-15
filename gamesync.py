#!/usr/bin/python3

import os
import json
import sys
from shutil import copyfile
from string import Template

SYNC_JSON = "/sync.json"
JSON_EXT = ".json"
CONFIG_FOLDER = "~/.config/gamesync"

class gs_settings:
    sync = "/dev/null"
    verbose = False
    
    def __init__(self):
        self.data = []
        
    def get_available_games_dir(self):
        d = self.get_dir()
        sd = d + "/games-available"
        
        return sd
        
    def get_enabled_games_dir(self):
        d = self.get_dir()
        sd = d + "/games-enabled"        
        
        return sd
    
    def get_etc_dir(self):
        d = self.get_dir()
        e = d + "/etc" 
        return e       

    def get_dir(self):
        e = os.path.expanduser(CONFIG_FOLDER)
        return e
    
    def read_settings(self):
        e = self.get_etc_dir()
        if os.path.isfile(e + SYNC_JSON):
            #print("Settings Found!")
            self.read_settings_json(e + SYNC_JSON)            
        else:
            print("Settings not found")
            
    def read_settings_json(self, settings_file):
        print(settings_file)
        fo = open(settings_file, "r")
        j = json.load(fo)
        fo.close()
        self.sync = j['sync']
        print("Sync Dir: " + self.sync)
    
    def get_enabled_games_json(self):
        d = self.get_enabled_games_dir()
        if os.path.exists(d):
            files = os.listdir(d)
            files.sort()
            for x in files:
                # print(x)
                mypath = d + "/" + x
                if os.path.isfile(mypath):
                    o = open(mypath, "r")
                    j = json.load(o)
                    o.close()
                    s = self.sync + "/Games/" + j['game']
                    print(j['game'])
                    if not os.path.exists(s):
                        print("Creating game folder:" + j['game'])
                        os.makedirs(s)
                    
                    cmd = "rsync -auv \"" \
                        + j['gamefolder'] + "/\" " \
                        + "\"" + s +"/\""
                    
                    if not self.verbose:
                        cmd = cmd + " > /dev/null"
                    # print(cmd)
                    os.system(cmd)
                else:
                    print("Not file " + mypath)
        else:
            print("Settings Directory doesn't exist")
            print (d)
    
    def create_sync_file(self):
        d = self.get_etc_dir()
        of = d + SYNC_JSON
        f = open(of, "w")
        f.write("{\n")
        f.write("\tsync: \"\"\n")
        f.write("}\n")
        f.close()        
            
    def myinit(self):
        d = self.get_dir()
        if not os.path.exists(d):
            os.makedirs(d)
        d = self.get_enabled_games_dir()
        if not os.path.exists(d):
            os.makedirs(d)
        d = self.get_available_games_dir()
        if not os.path.exists(d):
            os.makedirs(d)
        d = self.get_etc_dir()
        if not os.path.exists(d):
            os.makedirs(d)
        
        print("Please enter the directory you want to sync with")
        print("for example: ~/Nextcloud/GameSync")
        x = input()
        xx = os.path.expanduser(x)
        
        self.create_sync_file()

        d = self.get_etc_dir()
        of = d + SYNC_JSON        
             
        o = open(of, "w")  
        o.write("{\n")
        o.write("\t\"sync\":")
        o.write("\""+xx+"\""+"\n")
        o.write("}\n")      
              
        o.close()
        
    def new(self, arg):
        d = self.get_available_games_dir()
        f = d + "/" + arg + JSON_EXT
        if os.path.exists(f):
            print( "Game already exists, not changing")
            print( "Use --edit to modify")
        else:
            of = open(f,"w")
            ttemp = Template('{ "game": "$game", "gamefolder": "$gamefolder" }')
            print("New game: " + arg)
            print("Please enter folder to sync:")
            x = input()
            xx = os.path.expanduser(x)
            
            tt = ttemp.substitute(game=arg, gamefolder=xx)
            #print(tt)
            j = json.loads(tt)
            json.dump(j, of)
            of.close()
            d = self.get_enabled_games_dir()
            fe = d + "/" + arg + JSON_EXT
            copyfile(f,fe)
            
    def enabled(self):
        d =self.get_enabled_games_dir()
        files = os.listdir(d)
        files.sort()
        for f in files:
            _, ext = os.path.splitext(f)            
            if ext == JSON_EXT:
                fo = open(d + "/" + f,"r")
                j = json.load(fo)
                print(j['game'])
                fo.close()
                
    def disabled(self):
        da = self.get_available_games_dir()
        de = self.get_enabled_games_dir()
        files = os.listdir(da)
        files.sort()
        for f in files:
            if not os.path.exists(de + "/" + f):
                fo = open(da + "/" + f)
                j = json.load(fo)
                print(j['game'])
                fo.close()
                
    def enable(self, arg):
        da = self.get_available_games_dir()
        de = self.get_enabled_games_dir()
        
        for f in os.listdir(da):
            fo = open(da + "/" + f)
            j = json.load(fo)
            game = j['game']
            fo.close()
            if game == arg:
                thegame = f
                break
        
        if os.path.exists(da + "/" + thegame):
            if not os.path.exists(de + "/" + thegame):
                copyfile(da + "/" + thegame,
                         de + "/" + thegame)
                print("Enabled: \"" + arg + "\"")
            else:
                print("Game \"" + arg + "\" is already enabled")
        else:
            print("Game \"" + arg + "\" doesn't exist")
            
    def disable(self, arg):        
        de = self.get_enabled_games_dir()
        
        files = os.listdir(de)
        for f in files:
            fo = open (de + "/" + f, "r")
            j = json.load(fo)
            game = j['game']
            if game == arg:
                thegame = f
                break
        
        if os.path.exists(de + "/" + thegame):
            os.remove(de + "/" + thegame)
            print("Disabled: " + arg)
        else:
            print("Couldn't find \"" + arg + "\"")
            print("Are you sure it's enabled?")
            
    def edit(self, arg):
        da = self.get_available_games_dir()
        de = self.get_enabled_games_dir()
        
        files = os.listdir(da)
        for f in files:
            fo = open(da + "/" + f, "r")
            j = json.load(fo)
            fo.close()
            g = j['game']
            if g == arg:
                thegame = f
                cpath = j['gamefolder']
                break
        
        if os.path.exists(da + "/" + thegame):
            print("Game \"" + arg + "\" Found")
            print("Current Path: " + cpath)
            print("")
            print("Please enter new path")  
            x = input()            
            xx = os.path.expanduser(x)
            fo = open(da + "/" + thegame, "r")
            j = json.load(fo)
            j['gamefolder'] = xx
            fo.close()
            fo = open(da + "/" + thegame, "w")
            json.dump(j, fo)
            fo.close()
            if os.path.exists(de + "/" + thegame):
                copyfile(da + "/" + thegame,
                         de + "/" + thegame
                     )
            print("Game \"" + arg + "\" edited")
            
    def view(self, arg):
        da = self.get_available_games_dir()
        
        files = os.listdir(da)
        
        for f in files:
            fo = open (da + "/" + f)
            j = json.load(fo)
            g = j['game']
            if g == arg:
                print("Game: \"" + g + "\"")
                print("Folder Path:")
                print(j['gamefolder'])
                return
                      
    def delete(self, arg):
        da = self.get_available_games_dir()
        de = self.get_available_games_dir()
        
        files = os.listdir(da)
        
        print("Searching for : " + arg)
        
        found = False
        for f in files:
            fo = open( da + "/" + f, "r")
            j = json.load(fo)
            game = j['game']
            print(game)
            if game == arg:
                thegamefile = f
                found = True
                print ("Game \""+game+"\" Found")
                break
            
        if found:
            print ("Are you sure you want to delete")
            print (thegamefile +  "?")
            print ("y/N")
            x = input()
            
            if x == "y":
                os.remove(da + "/" + thegamefile)
                
                if os.path.exists(de + "/" + thegamefile):
                    os.remove(de + "/" + thegamefile)
    
    def help(self):
        print("GameSync Options")
        print("================")
        print()
        print("--init : Initialise gamesync folders, should be called on first install")
        print()
        print("--new,-n arg :       New Game")
        print("--delete,-del arg :  Delete Game")
        print("--edit :             Edit Game")
        print("--view,-v arg :      View Game")
        print()
        print("Listing Options")
        print("===============")
        print()
        print("--enabled            List Enabled Games")
        print("--disabled           List Disabled Games")
        print()
        print("Operations")
        print("==========")
        print()
        print("--enable,-e arg :    Enable given Game")
        print("--disable,-d arg :   Disable given Game")

sett = gs_settings()       
if len(sys.argv) > 1:
    idx = 0
    for x in sys.argv:
        if x == "--init":
            print ( "initialising" )
            sett.myinit()
            sys.exit(0)
        elif x == "--verbose":
            sett.verbose = True
        elif x == "--new" or x == "-n":
            if idx+1 < len(sys.argv):
                a = sys.argv[idx+1]
                print(a)
                sett.new(a)                
                sys.exit(0)
            else:
                print("Command --new requires an argument")
                sys.exit(1)
        elif x == "--enabled":
            sett.enabled()
            sys.exit(0)
        elif x == "--disabled":
            sett.disabled()
            sys.exit(0)
        elif x == "--disable" or x == "-d":
            a = sys.argv[idx+1]
            sett.disable(a)
            sys.exit(0)
        elif x == "--enable" or x == "-e":
            a = sys.argv[idx+1]
            sett.enable(a)
            sys.exit(0)
        elif x == "--edit":
            a = sys.argv[idx+1]
            sett.edit(a)
            sys.exit(0)
        elif x == "--view" or x == "-v":
            a = sys.argv[idx+1]
            sett.view(a)
            sys.exit(0)
        elif x == "--delete" or x == "-del":
            a = sys.argv[idx+1]
            print(a)
            sett.delete(a)
            sys.exit(0)
        elif x == "--help" or x == "-h" or x == "/?":
            sett.help()
            sys.exit(0)
        idx+=1

s = sett.get_etc_dir()
if not os.path.exists(s + SYNC_JSON):
        print ( "initialising" )
        sett.myinit() 
 
print("=========")       
print(" Syncing")
print("=========")
print("")
sett.read_settings()   
sett.get_enabled_games_json()
sys.exit(0)





