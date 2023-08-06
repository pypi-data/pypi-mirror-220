class Device:
    def __init__(self, platform):
        self.platform = platform

    def click(self, x, y):
        """
        Simulate a click on the screen at position (x, y).
        This method should be overridden by subclasses to provide platform-specific implementation.
        """
        raise NotImplementedError("Subclass must implement this method")

    def swipe(self, x1, y1, x2, y2):
        """
        Simulate a swipe on the screen from position (x1, y1) to position (x2, y2).
        This method should be overridden by subclasses to provide platform-specific implementation.
        """
        raise NotImplementedError("Subclass must implement this method")

    def type(self, text):
        """
        Simulate typing a string of text.
        This method should be overridden by subclasses to provide platform-specific implementation.
        """
        raise NotImplementedError("Subclass must implement this method")

    def get_screen(self):
        """
        Capture the screen and return it.
        This method should be overridden by subclasses to provide platform-specific implementation.
        """
        raise NotImplementedError("Subclass must implement this method")
