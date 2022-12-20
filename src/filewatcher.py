### Original was copied from StackOverflow by 4Oh4. Modified by Muvox ###
import os
import sys 
import time

class FileWatcher(object):
    running = True
    refresh_delay_secs = 1

    # Constructor
    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self.filename = watch_file
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs
        self._cached_stamp = os.stat(watch_file).st_mtime

    # Look for changes
    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            print('File changed')
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    # Keep watching in a loop        
    def watch(self):
        while self.running: 
            try: 
                # Look for changes
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                print('\nDone') 
                break 
            except FileNotFoundError:
                # Action on file not found
                pass
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])

# # Example usage ##
# def custom_action(text):
#     print(text)

# watch_file = 'my_file.txt'

# # FileWatcher = FileWatcher(watch_file)  # simple
# FileWatcher = FileWatcher(watch_file, custom_action, text='yes, changed')  # also call custom action function
# FileWatcher.watch()  # start the watch going