import os
import shutil
import time
class TestRunner:
    def __init__(self):
        self.runner = None

    def runTests(self):
        shutil.copyfile('grade/input_01.txt','input.txt')
        # shutil.copyfile('testcase/input1.txt', 'input.txt')
        os.system('python homework.py')
        # upper_bound = 33
        upper_bound = 18
        test_fail = False
        for i in range(1, upper_bound + 1, 1):
            file_no_str = None
            if i < 10:
                file_no_str = "0" + str(i)
                # file_no_str = str(i)

            else:
                file_no_str = str(i)
            expected_file = 'grade/input_' + file_no_str + '.txt'
            # expected_file = 'testcase/input' + file_no_str + '.txt'
            print("\n " + str(i) + ": Running Test : ", expected_file)

            shutil.copyfile(expected_file,'input.txt')
            time.sleep(0.3)
            os.system('python homework.py')
            time.sleep(1)
            ifp = open('output.txt', 'r')
            test_run_output = ifp.readlines()
            ifp.close()

            ifp2 = open('grade/output_' + file_no_str + '.txt', 'r')
            # ifp2 = open('testcase/output' + file_no_str + '.txt', 'r')
            expected_run_output = ifp2.readlines()
            ifp2.close()

            print(test_run_output)
            print(expected_run_output)
            if len(test_run_output) != len(expected_run_output):
                print('Test failed for : tests/input_' + file_no_str + '.txt')
                test_fail = True
                break
            ind = 0
            while ind < len(test_run_output):
                if test_run_output[ind] != expected_run_output[ind]:
                    print('Test failed for : tests/input_' + file_no_str + '.txt')
                    print('Test Output : ', test_run_output)
                    print('Expected Output : ', expected_run_output)
                    test_fail = True
                    break
                ind += 1
        if test_fail == False:
            print("All Tests Passed!")

t = TestRunner()
t.runTests()
