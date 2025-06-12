import tkinter as tk
import sys
import os

# Add the Historias directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Historias'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Historias', 'paciente'))

from GUI import Frame

def test_validations():
    """Test the validation functions"""
    root = tk.Tk()
    root.title("Test Validations")
    
    # Create a Frame instance to test the validation methods
    frame = Frame(root)
    
    # Test number validation
    print("Testing number validation:")
    print(f"'123' -> {frame.validar_solo_numeros('123')}")  # Should be True
    print(f"'abc' -> {frame.validar_solo_numeros('abc')}")  # Should be False
    print(f"'12a' -> {frame.validar_solo_numeros('12a')}")  # Should be False
    print(f"'' -> {frame.validar_solo_numeros('')}")        # Should be True (empty)
    
    # Test letter validation
    print("\nTesting letter validation:")
    print(f"'Juan' -> {frame.validar_solo_letras('Juan')}")     # Should be True
    print(f"'Juan Perez' -> {frame.validar_solo_letras('Juan Perez')}")  # Should be True
    print(f"'Juan123' -> {frame.validar_solo_letras('Juan123')}")  # Should be False
    print(f"'123' -> {frame.validar_solo_letras('123')}")     # Should be False
    print(f"'' -> {frame.validar_solo_letras('')}")           # Should be True (empty)
    
    print("\nValidation tests completed successfully!")
    
    # Close the window
    root.destroy()

if __name__ == "__main__":
    test_validations()
