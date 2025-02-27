import unittest
from fullcontrol.gcode.manual_gcode import ManualGcode

class TestManualGcodeParameters(unittest.TestCase):
    """Tests to verify correct parameter handling in ManualGcode."""

    def test_correct_gcode_parameter(self):
        """Test ManualGcode creation with correct 'gcode' parameter."""
        # This should work fine
        mgcode = ManualGcode(gcode="G1 X10 Y20")
        self.assertEqual(mgcode.gcode, "G1 X10 Y20")  # Access as attribute, not method

    def test_incorrect_text_parameter(self):
        """Test that using 'text' parameter raises TypeError."""
        # This should raise TypeError
        with self.assertRaises(TypeError) as context:
            mgcode = ManualGcode(text="G1 X10 Y20")
        
        # Check the error message
        self.assertIn("unexpected keyword argument 'text'", str(context.exception))
        
    def test_empty_gcode(self):
        """Test that empty or None gcode is handled properly."""
        mgcode1 = ManualGcode()
        self.assertEqual(mgcode1.gcode, "")  # Empty string, not None
        
        mgcode2 = ManualGcode(gcode="")
        self.assertEqual(mgcode2.gcode, "")
        
    def test_non_string_gcode(self):
        """Test that non-string gcode raises ValueError."""
        with self.assertRaises(ValueError):
            ManualGcode(gcode=123)


if __name__ == "__main__":
    unittest.main()