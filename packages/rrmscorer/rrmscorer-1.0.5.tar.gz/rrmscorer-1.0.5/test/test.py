import unittest
import subprocess

class TestStringMethods(unittest.TestCase):

    def test_UP_input(self):
        bashCmd = ["python",
                   "rrmscorer_runner.py",
                   "-u", "P19339",
                   "-r", "UUUUU",
                   "-w", "5"
                   ]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.assertEqual(stdout.decode().splitlines()[1].split(" ")[0], "2")
        self.assertEqual(round(
            float(stdout.decode().splitlines()[3].split(" ")[1]), 2), -0.38)
        self.assertEqual(round(
            float(stdout.decode().splitlines()[5].split(" ")[1]), 2), -0.68)

    def test_fasta_input(self):
        bashCmd = ["python",
                   "rrmscorer_runner.py",
                   "-f", "test/input_files/4ED5.fasta",
                   "-r", "UUUUU",
                   "-w", "5"
                   ]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.assertEqual(stdout.decode().splitlines()[1].split(" ")[0], "2")
        self.assertEqual(round(
            float(stdout.decode().splitlines()[3].split(" ")[1]), 2), -0.52)
        self.assertEqual(round(
            float(stdout.decode().splitlines()[5].split(" ")[1]), 2), -0.61)

if __name__ == '__main__':
    unittest.main()