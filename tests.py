from main import open_ifc, create_selector, get_elements_by_storey, edit_path, write_to_json
from functools import wraps
from parameterized import parameterized_class
import tracemalloc
import unittest
from timeit import default_timer as timer


SMALL_FILE_PATH = 'files/test-small.ifc'
MEDIUM_FILE_PATH = 'files/test-medium.ifc'
LARGE_FILE_PATH = 'files/test-large.ifc'

ONE_SELECTOR = '.IfcBeam'
FIVE_SELECTOR = '.IfcBeam | .IfcSlab | .IfcCurtainWall | .IfcDoor'
TEN_SELECTOR = '.IfcBeam | .IfcSlab | .IfcCurtainWall | .IfcDoor | .IfcBeam | .IfcRailing | .IfcRamp | .IfcRampFlight | .IfcRoof'


# Decorator to print data
def dec_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'\nStarting test "{func.__name__}"')
        func(*args, **kwargs)
    return wrapper

@parameterized_class([
    {'file_path': SMALL_FILE_PATH},
    {'file_path': MEDIUM_FILE_PATH},
    # {'file_path': LARGE_FILE_PATH},
])
class TestIfc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up tests
        cls.file_start = timer()
        cls.ifc = open_ifc(cls.file_path)
        cls.file_end = timer()
        print(f'\nTime elapsed to open a {cls.file_path} file: {(cls.file_end - cls.file_start):.8f}s')
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
        write_to_json(edit_path(self.file_path[6:-4]), self.result)

    @dec_test
    def test_1(self):
        # Run functions
        elements = self.selector.parse(self.ifc, ONE_SELECTOR)
        self.result = get_elements_by_storey(elements)

    @dec_test
    def test_5(self):
        # Run functions
        elements = self.selector.parse(self.ifc, FIVE_SELECTOR)
        self.result = get_elements_by_storey(elements)

    @dec_test
    def test_10(self):
        # Run functions
        elements = self.selector.parse(self.ifc, TEN_SELECTOR)
        self.result = get_elements_by_storey(elements)


if __name__ == '__main__':
    unittest.main()
