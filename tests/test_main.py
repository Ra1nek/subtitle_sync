import pytest
from PyQt5.QtWidgets import QApplication
from subtitle_sync.gui.main_window import MainWindow

@pytest.fixture
def app(qtbot):
    """Fixture to create and return the QApplication instance."""
    app = QApplication([])
    return app

def test_main_window_creation(app, qtbot):
    """Test that the MainWindow is created and shown correctly."""
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    main_window.show()
    
    # Assert that the main window is visible
    assert main_window.isVisible()
    
    # Optionally, check if the window has a title or other attributes
    assert main_window.windowTitle() == "Expected Title"  # Replace with actual title

    # Test if the main window has a specific widget
    # Example: Check if a QPushButton with a specific text exists
    button = main_window.findChild(QPushButton, "Expected Button Name")  # Replace with actual widget name
    assert button is not None
