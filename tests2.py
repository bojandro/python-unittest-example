from main import open_ifc, create_selector, get_elements_by_storey
from functools import wraps
import tracemalloc
import unittest
from timeit import default_timer as timer
import os, psutil


SMALL_FILE_PATH = 'files/test-small.ifc'
MEDIUM_FILE_PATH = 'files/test-medium.ifc'
LARGE_FILE_PATH = 'files/test-large.ifc'

ONE_SELECTOR = '.IfcDoor'
FIVE_SELECTOR = '.IfcBeam | .IfcColumn | .IfcCurtainWall | .IfcDoor | .IfcMember'
TEN_SELECTOR = '.IfcBeam | .IfcColumn | .IfcCurtainWall | .IfcDoor | .IfcMember | .IfcBeam | .IfcRailing | .IfcRamp | .IfcRampFlight | .IfcRoof'


class TestSmall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up tests
        cls.file_start = timer()
        cls.ifc = open_ifc(SMALL_FILE_PATH)
        cls.file_end = timer()
        print(f'\nTime elapsed to open a SMALL file: {(cls.file_end - cls.file_start):.8f}s')
        cls.selector = create_selector()

    def setUp(self):
        # Start memory tracing
        self.start = timer()
        tracemalloc.start()

    def tearDown(self):
        # Calculate time and memory
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
        self.end = timer()
        print(f'Time elapsed to compelete parsing: {(self.end - self.start):.8f}s')
        tracemalloc.stop()

    # Decorator to print data
    def dec_test(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'\nStarting test "{func.__name__}"')
            func(*args, **kwargs)
        return wrapper

    @dec_test
    def test_small_1(self):
        # Run functions
        elements = self.selector.parse(self.ifc, ONE_SELECTOR)
        result = get_elements_by_storey(elements)

    @dec_test
    def test_small_5(self):
        # Run functions
        elements = self.selector.parse(self.ifc, FIVE_SELECTOR)
        result = get_elements_by_storey(elements)

    @dec_test
    def test_small_10(self):
        # Run functions
        elements = self.selector.parse(self.ifc, TEN_SELECTOR)
        result = get_elements_by_storey(elements)


class TestMedium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up tests
        cls.file_start = timer()
        cls.ifc = open_ifc(MEDIUM_FILE_PATH)
        cls.file_end = timer()
        print(f'\nTime elapsed to open a MEDIUM file: {(cls.file_end - cls.file_start):.8f}s')
        cls.selector = create_selector()

    def setUp(self):
        # Start memory tracing
        self.start = timer()
        tracemalloc.start()

    # Decorator to print data
    def dec_test(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'\nStarting test "{func.__name__}"')
            func(*args, **kwargs)
        return wrapper

    def tearDown(self):
        # Print out memory usage and stop memory tracing
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
        self.end = timer()
        print(f'Time elapsed to compelete parsing: {(self.end - self.start):.8f}s')
        tracemalloc.stop()

    @dec_test
    def test_medium_1(self):
        # Run functions
        elements = self.selector.parse(self.ifc, ONE_SELECTOR)
        result = get_elements_by_storey(elements)

    @dec_test
    def test_medium_5(self):
        # Run functions
        elements = self.selector.parse(self.ifc, FIVE_SELECTOR)
        result = get_elements_by_storey(elements)

    @dec_test
    def test_medium_10(self):
        # Run functions
        elements = self.selector.parse(self.ifc, TEN_SELECTOR)
        result = get_elements_by_storey(elements)


class TestLarge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up tests

        # Getting initial memory
        process = psutil.Process(os.getpid())
        cls.initialMem = process.memory_info().rss

        cls.file_start = timer()
        cls.ifc = open_ifc(LARGE_FILE_PATH)
        cls.file_end = timer()
        print(f'\nTime elapsed to open a LARGE file: {(cls.file_end - cls.file_start):.8f}s')
        cls.selector = create_selector()

    def setUp(self):
        # Start memory tracing
        self.start = timer()

    # Decorator to print data
    def dec_test(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'\nStarting test "{func.__name__}"')
            func(*args, **kwargs)
        return wrapper

    def tearDown(self):
        # Print out memory usage and stop memory tracing
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
        self.end = timer()
        print(f'Time elapsed to compelete parsing: {(self.end - self.start):.8f}s')
        tracemalloc.stop()

    @dec_test
    def test_large_1(self):
        # Run functions
        elements = self.selector.parse(self.ifc, ONE_SELECTOR)
        result = get_elements_by_storey(elements)

        # Getting final memory
        process = psutil.Process(os.getpid())
        diff = process.memory_info().rss - self.initialMem
        diff = diff

    @dec_test
    def test_large_5(self):
        # Run functions
        elements = self.selector.parse(self.ifc, FIVE_SELECTOR)
        result = get_elements_by_storey(elements)

    @dec_test
    def test_large_10(self):
        # Run functions
        elements = self.selector.parse(self.ifc, TEN_SELECTOR)
        result = get_elements_by_storey(elements)


if __name__ == '__main__':
    unittest.main()
