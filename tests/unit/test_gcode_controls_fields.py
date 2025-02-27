import unittest
from fullcontrol.gcode.controls import GcodeControls
from pydantic import ValidationError

class TestGcodeControlsFields(unittest.TestCase):
    """Tests to verify correct field access in GcodeControls."""

    def test_printer_name_attribute_access(self):
        """Test accessing printer_name as an attribute."""
        controls = GcodeControls(printer_name="generic")
        # This should work fine - accessing as an attribute
        self.assertEqual(controls.printer_name, "generic")

    def test_printer_name_field_access(self):
        """Test that accessing printer_name as a field raises an error."""
        controls = GcodeControls(printer_name="generic")
        
        # Attempting to access controls["printer_name"] should fail
        with self.assertRaises(Exception) as context:
            value = controls["printer_name"]
        
        # The error message might be different depending on the implementation
        # This checks if it's either a KeyError or TypeError
        self.assertTrue(
            isinstance(context.exception, (KeyError, TypeError, AttributeError)),
            f"Expected KeyError, TypeError, or AttributeError but got {type(context.exception)}"
        )

    def test_initialization_data_access(self):
        """Test accessing initialization_data values."""
        controls = GcodeControls(
            printer_name="generic", 
            initialization_data={"print_speed": 1500}
        )
        
        # Using the get_config method should work
        self.assertEqual(controls.get_config("print_speed"), 1500)
        
        # Default values should be applied
        self.assertEqual(controls.get_config("extrusion_width"), 0.4)


if __name__ == "__main__":
    unittest.main()