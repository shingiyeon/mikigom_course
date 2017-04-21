import subprocess
import unittest
import sys
import filecmp

bash_call = './' + sys.argv[1]

def subprocess_pipe(cmd_list):
    prev_stdin = None
    last_p = None
    
    for str_cmd in cmd_list:
        cmd = str_cmd.split()
        last_p = subprocess.Popen(cmd, stdin=prev_stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        prev_stdin = last_p.stdout
    
    (stdoutdata, stderrdata) = last_p.communicate()
    return stdoutdata, stderrdata

class BashTest(unittest.TestCase):
    def test1(self):
        test_cmd = 'ls'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)

    def test2(self):
        test_cmd = 'ls > out'
        cmd_list = [bash_call, test_cmd + '_homebrew']
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)
        self.assertTrue(filecmp.cmp('out', 'out_homebrew'), msg = None)

    def test3(self):
        test_cmd = 'cat	< code.c'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)


    def test4(self):
        test_cmd = 'cat	< code.c > out'
        cmd_list = [bash_call, test_cmd + '_homebrew']
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)
        self.assertTrue(filecmp.cmp('out', 'out_homebrew'), msg = None)

    """
    def test5(self):
        test_cmd = 'cat	>> out'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh, _ = subprocess_pipe(cmd_list)
        naive_sh = subprocess.check_output(test_cmd, shell=True)
        self.assertEqual(homebrew_sh, naive_sh)
    """

    def test6(self):
        test_cmd = 'cat < code.c | more'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)
   
    def test7(self):
        test_cmd = 'who | grep hjnam && echo "hjnam is logged in"'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)

    def test8(self):
        test_cmd = 'who | grep hjnam || echo "hjnam not logged in"'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh_stdout, homebrew_sh_stderr = subprocess_pipe(cmd_list)
        naive_sh = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = naive_sh.communicate()
        if out is None:
            self.assertEqual(homebrew_sh_stdout, '')
        else:
            self.assertEqual(homebrew_sh_stdout, out)
        if err is None:
            self.assertEqual(homebrew_sh_stderr, '')
        else:
            self.assertEqual(homebrew_sh_stderr, err)

    """
    def test9(self):
        test_cmd = 'exit'
        cmd_list = [bash_call, test_cmd]
        homebrew_sh, _ = subprocess_pipe(cmd_list)
        naive_sh = subprocess.check_output(test_cmd, shell=True)
        self.assertEqual(homebrew_sh, naive_sh)
    """

if __name__ == '__main__':
    TS = unittest.makeSuite(BashTest, "test")

    runner = unittest.TextTestRunner()
    runner.run(TS)
