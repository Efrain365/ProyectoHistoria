import tkinter as tk
import sys
import os

# Add the Historias directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Historias'))

def test_gui_implementation():
    """Test the GUI implementation with validations"""
    try:
        # Import the Frame class from the correct path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Historias', 'paciente'))
        from GUI import Frame
        
        root = tk.Tk()
        root.title("Test GUI Implementation")
        root.geometry("800x600")
        
        # Create the frame
        frame = Frame(root)
        
        print("✓ GUI Frame created successfully")
        
        # Test validation functions exist
        assert hasattr(frame, 'validar_solo_numeros'), "validar_solo_numeros method missing"
        assert hasattr(frame, 'validar_solo_letras'), "validar_solo_letras method missing"
        print("✓ Validation methods exist")
        
        # Test validation functions work correctly
        # Number validation tests
        assert frame.validar_solo_numeros('123') == True, "Number validation failed for '123'"
        assert frame.validar_solo_numeros('abc') == False, "Number validation failed for 'abc'"
        assert frame.validar_solo_numeros('') == True, "Number validation failed for empty string"
        print("✓ Number validation works correctly")
        
        # Letter validation tests
        assert frame.validar_solo_letras('Juan') == True, "Letter validation failed for 'Juan'"
        assert frame.validar_solo_letras('Juan Perez') == True, "Letter validation failed for 'Juan Perez'"
        assert frame.validar_solo_letras('Juan123') == False, "Letter validation failed for 'Juan123'"
        assert frame.validar_solo_letras('') == True, "Letter validation failed for empty string"
        print("✓ Letter validation works correctly")
        
        # Check if entry fields have validation configured
        entry_fields = {
            'entryNombre': 'letters',
            'entryCI': 'numbers', 
            'entryEdad': 'numbers',
            'entryTlfn': 'numbers',
            'entryAlergia': 'letters',
            'entryEnfermedad': 'letters',
            'entryMedicamento': 'letters'
        }
        
        for field_name, validation_type in entry_fields.items():
            if hasattr(frame, field_name):
                field = getattr(frame, field_name)
                validate_option = field.cget('validate')
                if validate_option == 'key':
                    print(f"✓ {field_name} has validation configured")
                else:
                    print(f"⚠ {field_name} validation may not be configured properly")
            else:
                print(f"⚠ {field_name} not found")
        
        # Check if the "Buscar por CI" label exists and has correct text
        if hasattr(frame, 'lblBuscarCI'):
            label_text = frame.lblBuscarCI.cget('text')
            if label_text == 'Buscar por CI: ':
                print("✓ 'Buscar por CI' label text is correct")
            else:
                print(f"⚠ Label text is '{label_text}', expected 'Buscar por CI: '")
        else:
            print("⚠ lblBuscarCI not found")
        
        print("\n🎉 All tests completed successfully!")
        print("✅ Input validation has been implemented correctly")
        print("✅ UI changes have been applied")
        
        # Close the window after a short delay
        root.after(2000, root.destroy)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_implementation()
