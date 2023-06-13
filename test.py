# All tests should not error out and also return True.
import os, shutil
import code_in_a_box

test_fold = '_test'

def _reset_dir():
    _dir = os.path.dirname(os.path.abspath(__file__))
    print('Reset dir to:', _dir)
    os.chdir(_dir)

def _delete_test_folder():
    _reset_dir()
    code_in_a_box.power_delete('./'+test_fold, tries=12, retry_delay=1.0)

def test_bootstrap():
    _reset_dir()
    _delete_test_folder()

    os.makedirs(test_fold)

    with open('./'+'install.txt', 'r') as file:
        boot_txt = file.read()
    lines = boot_txt.replace('\r\n','\n').split('\n')

    os.chdir(test_fold)
    for line in lines:
        try:
            exec(line)
        except Exception as e:
            if "name 'python' is not defined" not in str(e) and "name 'python3' is not defined" not in str(e):
                raise e
    _reset_dir()
    with open('./'+test_fold+'/code_in_a_box.py','r') as file:
        txt1 = file.read()

    _reset_dir()
    _delete_test_folder()

    return 'power_delete(fname,' in txt1 and "in this case {self.origin}')" in txt1

def test_download_git():
    # Tests downloading a Git repo.
    _reset_dir()
    _delete_test_folder()

    code_in_a_box.download('https://github.com/benycze/python-tetris', './'+test_fold, clear_folder=False)

    with open('./'+test_fold+'/block.py','r', encoding='UTF-8') as file:
        txt1 = file.read()

    _reset_dir()
    _delete_test_folder()

    return 'pygame.Rect(bx,by,constants.BWIDTH,constants.BHEIGHT)' in txt1 and 'tmp_shape = self.shape[shape_i]' in txt1

def run():
    out = True
    out = out and test_bootstrap()
    out = out and test_download_git()
    if out is True:
        print('ALL TESTS PASS')
    else:
        print('SOME/ALL TEST FAIL')
    return out
