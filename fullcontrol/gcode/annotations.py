from typing import Optional


class GcodeComment:
    """Class for adding comments to G-code output."""
    def __init__(self, comment: str):
        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        self.comment = comment

    def gcode(self, state) -> str:
        """Return the comment in G-code format."""
        return f"; {self.comment.strip()}"
