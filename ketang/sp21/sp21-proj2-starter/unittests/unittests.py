from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):
    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)
    def test_minus_one(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)


class TestArgmax(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # TODO
        # load address of the array into register a0
        t.input_array("a0", array0)
        # TODO
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # TODO
        # call the `argmax` function
        t.call("argmax")
        # TODO
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 8)
        # TODO
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)


class TestDot(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        #raise NotImplementedError("TODO")
        array1 = t.array([1,2,3,4,5,6,7,8,9])
        array2 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # TODO
        # load array addresses into argument registers
        t.input_array("a0", array1)
        t.input_array("a1", array2)
        # TODO
        # load array attributes into argument registers
        t.input_scalar("a2", len(array2))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # TODO
        # call the `dot` function
        t.call("dot")
        # check the return value
        # TODO
        t.check_scalar("a0",285)
        t.execute()
    def test_simple2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        #raise NotImplementedError("TODO")
        array1 = t.array([ 1, -2,  3, -4,  5, -6,  7, -8,  9])
        array2 = t.array([-1,  2, -3,  4, -5,  6, -7,  8, -9])
        # TODO
        # load array addresses into argument registers
        t.input_array("a0", array1)
        t.input_array("a1", array2)
        # TODO
        # load array attributes into argument registers
        t.input_scalar("a2", len(array2))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # TODO
        # call the `dot` function
        t.call("dot")
        # check the return value
        # TODO
        t.check_scalar("a0",-285)
        t.execute()

    def test_stride(self):
        t = AssemblyTest(self, "dot.s")
        array1 = t.array([1,2,3,4,5,6,7,8,9])
        array2 = t.array([1,2,3,4,5,6,7,8,9])
        t.input_array("a0", array1)
        t.input_array("a1", array2)
        t.input_scalar("a2", 4)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 2)
        t.call("dot")
        t.check_scalar("a0", 50)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)


class TestMatmul(TestCase):

    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        #raise NotImplementedError("TODO")
        # TODO
        t.input_array("a0", array0)
        t.input_array("a3", array1)
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)

        # load address of output array
        # TODO
        t.input_array("a6", array_out)

        # call the matmul function
        t.call("matmul")
        # check the content of the output array
        # TODO
        t.check_array(array_out, result)


        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1,1,1], 3, 1,
            [6,15,24]
        )

    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)


class TestReadMatrix(TestCase):

    def do_read_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/test_read_matrix/test_input.bin")
        # t.input_read_filename("a0", "test_input.bin")


        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        #raise NotImplementedError("TODO")
        # TODO
        t.input_array("a1",rows)
        t.input_array("a2",cols)

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        # TODO
        t.check_array(rows, [2])
        t.check_array(cols, [4])
        t.check_array_pointer("a0", [-1,-2,-3,-4,-5,-6,-7,-8])

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def do_read_matrix2(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/simple0/bin/m0.bin")
        # t.input_read_filename("a0", "test_input.bin")


        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        #raise NotImplementedError("TODO")
        # TODO
        t.input_array("a1",rows)
        t.input_array("a2",cols)

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        # TODO
        t.check_array(rows, [3])
        t.check_array(cols, [3])
        t.check_array_pointer("a0", [1,3,5,7,9,11,13,15,17])

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
    def test_simple(self):
        self.do_read_matrix()

    def test_read_Main(self):
        self.do_read_matrix2()

    def test_malloc(self):
        self.do_read_matrix(fail='malloc', code=116)

    def test_fopen(self):
        self.do_read_matrix(fail='fopen', code=117)

    def test_fread(self):
        self.do_read_matrix(fail='fread', code=118)

    def test_fclose(self):
        self.do_read_matrix(fail='fclose', code=119)

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)


class TestWriteMatrix(TestCase):

    def do_write_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/student.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        #raise NotImplementedError("TODO")
        arr = t.array([1,2,3,4,5,6,7,8,9])
        t.input_array("a1", arr)
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 3)
        # TODO
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.do_write_matrix()

    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def test_simple0_input0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/student0.bin"
        ref_file = "outputs/test_basic_main/reference0.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]
        # call classify function
        t.input_scalar("a2", 0) # printout
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)

        # compare the output file and
        #raise NotImplementedError("TODO")

        # TODO
        # compare the classification output with `check_stdout`
        t.check_file_output(out_file, ref_file)
        t.check_stdout("4")

    @classmethod
    def tearDownClass(cls):
        print_coverage("classify.s", verbose=False)


# The following are some simple sanity checks:
import subprocess, pathlib, os
script_dir = pathlib.Path(os.path.dirname(__file__)).resolve()

def compare_files(test, actual, expected):
    assert os.path.isfile(expected), f"Reference file {expected} does not exist!"
    test.assertTrue(os.path.isfile(actual), f"It seems like the program never created the output file {actual}!")
    # open and compare the files
    with open(actual, 'rb') as a:
        actual_bin = a.read()
    with open(expected, 'rb') as e:
        expected_bin = e.read()
    test.assertEqual(actual_bin, expected_bin, f"Bytes of {actual} and {expected} did not match!")

class TestMain(TestCase):
    """ This sanity check executes src/main.S using venus and verifies the stdout and the file that is generated.
    """

    def run_main(self, inputs, output_id, label):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin",
                f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"

        t= AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args)
        t.check_stdout(label)
        t.check_file_output(args[-1], reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")
