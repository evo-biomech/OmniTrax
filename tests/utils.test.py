import sys
import unittest

try:
    from omni_trax.omni_trax_utils import *


    class TestUtils(unittest.TestCase):

        def test_scale_detections(self):
            values = [100, 200, 320, 320, 1920, 1080]
            target = [600, 405]

            self.assertEqual(scale_detections(x=values[0], y=values[1],
                                              network_w=values[2], network_h=values[3],
                                              output_w=values[4], output_h=values[5]),
                             target)

        def test_convert_back(self):
            values = [100, 200, 1920, 1080]
            target = (-860, -340, 1060, 740)

            self.assertEqual(convertBack(x=values[0], y=values[1], w=values[2], h=values[3]),
                             target)


    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUtils)
    success = unittest.TextTestRunner().run(suite)

    if success.errors or success.failures:
        raise Exception

except Exception:
    sys.exit(1)
