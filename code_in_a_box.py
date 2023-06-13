# Downloads projects from Github or a local folder.
import io, sys, os, shutil

def _unwindoze_attempt(f, name, tries, retry_delay):
    for i in range(tries):
        try:
            f()
            break
        except PermissionError as e:
            if 'being used by another process' not in str(e):
                f() # Throw actual permission errors.
            if i==tries-1:
                raise Exception('Windoze error: Retried too many times and this file stayed in use:', name)
            print('File-in-use error (will retry) for:', name)
            time.sleep(retry_delay)

def power_delete(fname, tries=12, retry_delay=1.0):
    fname = os.path.realpath(fname)
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE) # rmtree can't remove internal read-only files, but the explorer can. This will remov read-only related errors.
        func(path)
    def f():
        if not os.path.exists(fname):
            return
        if is_folder(fname):
            shutil.rmtree(fname, onerror=remove_readonly)
        else:
            os.remove(fname)
    _unwindoze_attempt(f, fname, tries, retry_delay)

def clear_pycaches(folder):
    # Clears all the __pycache__ in the given folder.
    for pwd, dirs, files in os.walk(folder_path):
        if pwd.replace('\\','/').split('/')[-1] == '__pycache__':
            for fl in files:
                power_delete(fl)

def download(url, dest_folder, clear_folder=False):
    # Downloads a project to dest_folder.
    dest_folder = os.path.realpath(dest_folder)
    if os.path.exists(dest_folder) and clear_folder:
        power_delete(dest_folder)
    if os.path.exists(dest_folder):
        clear_pycaches(dest_folder)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    qwrap = lambda txt: '"'+txt+'"'

    if '//github.com' in url or '//www.github.com' in url:
        print('Fetching from GitHub')
        qwrap = lambda txt: '"'+txt+'"'
        cmd = ' '.join(['git','clone', qwrap(self.origin), qwrap(self.dest)])
        if os.path.exists(dest_folder+'/.git'): # Git will complain if there is already a .git
            power_delete(dest_folder+'/.git')
        os.system(cmd) #i.e. git clone https://github.com/the_use/the_repo the_folder. os.system will wait for the cmd to finish.
        print('Git Clones saved into this folder:', self.dest)
    elif url.startswith('http'):
        raise Exception(f'TODO: support other websites besides GitHub; in this case {self.origin}')
    elif url.startswith('ftp'):
        raise Exception('FTP requests not planned to be supported.')
    else:
        url = os.path.realpath(url)
        if url != dest_folder:
            if not os.path.exists(url):
                raise Exception(f'The origin is a folder on a local machine: {folder} but that folder does not exist.')
            shutil.copytree(folder, dest_folder)
