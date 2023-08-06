import os
import shutil
import socket
import logging
import random
import string
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from time import sleep

logger = logging.getLogger(__name__)

class Monkey():

    def __init__(self, workdir:str=None, 
                 interval_min_s:float=.01, 
                 interval_max_s:float=1, 
                 max_file_size_mb:int=2, 
                 max_file_amount:int=400, 
                 target_file_amount:int=200,
                 path_length_limit:int=200,
                 logging_to_file_enabled:bool=True) -> None:
        
        if workdir is not None:
            self.workdir = Path(workdir)
            self.monkeydir = Path(self.workdir, 'mky')
            self.interval_min_s = float(interval_min_s)
            self.interval_max_s = float(interval_max_s)
            self.max_file_size_mb = int(max_file_size_mb)
            self.max_file_count = int(max_file_amount)
            self.target_file_amount = int(target_file_amount)
            self.path_length_limit = int(path_length_limit)

            self._filecount = None
            self._active_file_paths = set()
            self._active_dir_paths = set()

            self.logging_to_file_enabled = logging_to_file_enabled
            self.setup_logger()
            self.create_workdir()

    #### Maintenence / Helper

    def setup_logger(self):
        try:
            logging.shutdown()
        except Exception:
            pass
        
        logger = logging.getLogger(__name__)
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)

        if self.logging_to_file_enabled:
            handler = RotatingFileHandler(Path(self.workdir, f'{socket.gethostname()}.log'), maxBytes=10000, backupCount=1)
            handler.setLevel(logging.DEBUG)

        else:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    ## create workdir
    def create_workdir(self):
        os.makedirs(self.monkeydir, exist_ok=True)
        assert os.path.exists(self.monkeydir)
        self.count_files()
        logger.debug(f"Monkey-Directory succesfully createt in {self.monkeydir}")

    ## count num files and dirs
    def count_files(self):
        count = 0
        self._active_file_paths = set()
        self._active_dir_paths = set()
        self._active_dir_paths.add(self.monkeydir)

        for root, dirs, files in os.walk(self.monkeydir):
            count += len(files)

            self._active_dir_paths.add(Path(root))
            for file in files:
                self._active_file_paths.add(Path(root, file))

        logger.debug(f"counted {count} files in monkeydir")
        self._filecount = count

    ## generate random file / dir name
    def gen_random_name(self, min_length:int=5, max_length:int=12):
        valid_chars = string.ascii_letters + string.digits
        return ''.join(random.choice(valid_chars) for _ in range(random.randint(min_length, max_length)))

    ## clean up workdir
    def cleanup_monkey_dir(self):
        shutil.rmtree(self.monkeydir)
        self.create_workdir()

    #### Tasks

    # execute random Task
    def task_run_random(self):
        avaiable_tasks = [
            self.task_new_file,
            self.task_new_directory,
            self.task_delete_file,
            self.task_edit_file,
            self.task_rename_dir,
            self.task_rename_file
        ]
        random.choice(avaiable_tasks)()
        self.count_files()

    ## create new file
    def task_new_file(self):
        target_dir = random.choice( tuple(self._active_dir_paths ))
        
        if self._filecount < self.max_file_count:
            try:
                if random.randint(0,1) == 0:
                    # create a textfile
                    filename = f"{self.gen_random_name()}.txt"
                    with open( Path(target_dir,filename ), 'w') as f:
                        f.write( self.gen_random_name(min_length=10, max_length=4096))
                        logger.info(f"created new textfile {filename}")
                else:
                    # create a binary file
                    filename = f"{self.gen_random_name()}.bin"
                    num_bytes = random.randint(0, self.max_file_size_mb*1048576)
                    data = os.urandom( num_bytes )
                    with open( Path(target_dir,filename ), 'wb') as f:
                        f.write(data)
                        logger.info(f"created new binary file {filename}")

            except Exception as ex:
                logger.warning(ex)

    ## create new directory
    def task_new_directory(self):
        target_dir = random.choice( tuple(self._active_dir_paths ))
        if len(target_dir.__str__()) < self.path_length_limit:
            try:
                dirpath = Path(target_dir, self.gen_random_name())
                os.makedirs(dirpath, exist_ok=True)
                logger.info(f"created new directory {target_dir}")
            except Exception as ex:
                logger.warning(ex)

    ## delete file
    def task_delete_file(self):
        if self._filecount > self.target_file_amount:
            try:
                target_file = random.choice(tuple(self._active_file_paths))
                os.remove(target_file)
                logger.info(f"deleted file {target_file}")
            except Exception as ex:
                logger.warning(ex)

    ## delte directory
    def task_delete_file(self):
        if self._filecount > self.target_file_amount:
            try:
                target_dir = random.choice(tuple(self._active_dir_paths))
                shutil.rmtree(target_dir)
                logger.info(f"deleted directory {target_dir}")
            except Exception as ex:
                logger.warning(ex)

    ## edit file
    def task_edit_file(self):
        try:
            target_file = random.choice(tuple(self._active_file_paths))
            _, file_extension = os.path.splitext(target_file)
            if file_extension == '.txt':
                with open( target_file, 'a') as f:
                    f.write( self.gen_random_name(min_length=10, max_length=4096))
                    logger.info(f"edited textfile {target_file}")
            
            elif file_extension == '.bin':
                num_bytes = random.randint(0, self.max_file_size_mb*1048576)
                data = os.urandom( num_bytes )
                with open(target_file, 'ba') as f:
                    f.write(data)
                    logger.info(f"edited binary file {target_file}")
        except Exception as ex:
            logger.warning(ex)

    ## rename file
    def task_rename_file(self):
        try:
            target_file = random.choice(tuple(self._active_file_paths))
            dir, extension = target_file.parent, os.path.splitext(target_file)[1]
            new_path = Path(dir, f"{self.gen_random_name()}{extension}")
            os.rename( target_file, new_path )
            logger.info(f"renamed file to {new_path}")
        except Exception as ex:
            logger.warning(ex)

    def task_rename_dir(self):
        try:
            target_dir = random.choice(tuple(self._active_dir_paths))
            if target_dir == self.monkeydir:
                # do not rename monkeydir
                return
            new_path = Path( target_dir.parent, self.gen_random_name())
            os.rename(target_dir, new_path)
            logger.info(f"renamed directory to {new_path}")
        except Exception as ex:
            logger.warning(ex)

    #### Runtime
    def run(self):
        logger.info("Program started")
        self.task_new_file()
        self.count_files()
        while True:
            try:
                self.task_run_random()
                sleep(random.uniform( self.interval_min_s, self.interval_max_s))

            except KeyboardInterrupt:
                logger.handlers.clear()
                logging.shutdown()
                exit()

            except Exception as ex:
                logger.critical(ex)
                logger.handlers.clear()
                logging.shutdown()
                exit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            if sys.argv[1][0] == '"' and sys.argv[1][-1] == '"':
                workdir = Path(sys.argv[1])
            else:
                print(f"Use Quotation marks for your path. Ex. \"L:\\monkey work\\test\\\"")
                exit()

            if not os.listdir(workdir) or '-f' in sys.argv[2:]:
                print (f"Target directory is empty or '-f' was set. {workdir} will be used\n!! FILES IN TARGET DIRECTORY WILL BE DELETED !!")
                sleep(5)

                monkey = Monkey(workdir=workdir)
                print ("start")
                monkey.run()

            else:
                print(f"Target directory is not empty!\nUse empty target or option '-f'\n!! FILES IN TARGET DIRECTORY WILL BE DELETED !!")
                exit()
        else:
            print ("The target direcotry does not exists")
            exit()

    else:
        print ("invalid target directory was provided! Use format: monkeywork.py [target_dir] [OPTIONS]")