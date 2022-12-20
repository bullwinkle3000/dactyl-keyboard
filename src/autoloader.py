import time
import os.path as path
import getopt, sys
import os
import json

from filewatcher import FileWatcher
from generate_configuration import save_config

got_opts = False
config_path = os.path.join(r".", "src", 'run_config.json')

def startup():
    global got_opts
    global config_path

    config = 'run_config'
    opts, args = getopt.getopt(sys.argv[1:], "", ["config=", "save_path="])
    for opt, arg in opts:
        print(arg)
        print(os.getcwd())
        if opt in '--config':
            print(f"Custom configuration file: {arg+'.json'}")
            config_path = os.path.join(r".", "configs", arg + '.json')
            config = arg
            if os.path.exists(config_path):
                print(f"Config with name {arg+'.json'} found.")
            else:
                print(f"Config with name {arg+'.json'} not found, generating new config.")
                save_config()
                while not os.path.exists(config_path):
                    time.sleep(1)
                print("Config created")
            got_opts = True


    if not got_opts:
        print("Using run_config.json")
    else:
        print(f"Using {config}.json")


    return config

def trigger_dactyl(custom, config):
    if custom:
        os.system(f'python src/dactyl_manuform.py --config {config}')
    else:
        os.system(f'python src/dactyl_manuform.py')

    print("Changes detected, dactyl has been re-generated!")

def main():
    global got_opts
    global config_path

    config = startup()
    print(config_path)
    watcher = FileWatcher(config_path, trigger_dactyl, custom=got_opts, config=config)
    print(f"Watching file {config}.json for changes")
    watcher.watch()
    # check_for_config_update(config)

if __name__ == "__main__":
    main()