from typing import Optional
from pydantic import BaseModel, validator


class GcodeControls(BaseModel):
    """
    Control to adjust the style and initialization of the gcode.

    Attributes:
        printer_name (Optional[str]): The name of the printer. Defaults to 'generic'.
        initialization_data (Optional[dict]): Values passed for initialization_data overwrite the default initialization_data of the printer. Defaults to an empty dictionary.
        save_as (Optional[str]): The file name to save the gcode as. Defaults to None resulting in no file being saved.
        include_date (Optional[bool]): Whether to include the date in the filename. Defaults to True.
    """
    printer_name: Optional[str] = None
    initialization_data: Optional[dict] = {} # values passed for initialization_data overwrite the default initialization_data of the printer
    save_as: Optional[str] = None
    include_date: Optional[bool] = True

    def _validate_singletool_printer(self, printer_name: str) -> bool:
        """Validate that a printer exists in the singletool directory"""
        try:
            printer_path = printer_name.replace('/', '.')
            __import__(f'fullcontrol.devices.community.singletool.{printer_path.lower()}')
            return True
        except ImportError:
            return False

    @validator('printer_name')
    def validate_printer_name(cls, v):
        if v is None:
            return 'generic'
        elif v[:10] == 'Community/' or v[:5] == 'Cura/':
            return v
        else:
            try:
                printer_path = v.replace('/', '.')
                __import__(f'fullcontrol.devices.community.singletool.{printer_path.lower()}')
                return v
            except ImportError:
                raise ValueError(f"Invalid printer_name: {v}. The printer was not found in the community singletool directory.")

    def initialize(self):
        if self.printer_name == 'generic':
            print("warning: printer is not set - defaulting to 'generic', which does not initialize the printer with proper start gcode\n   - use fc.transform(..., controls=fc.GcodeControls(printer_name='generic') to disable this message or set it to a real printer name\n")

