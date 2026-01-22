import random
import string
import sys


def generate_password(length, use_letters=True, use_digits=True, use_symbols=True):
   
    characters = ""
    
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    # Ensure at least one character type is selected
    if not characters:
        raise ValueError("At least one character type must be selected!")
    
    # Ensure minimum length
    if length < 1:
        raise ValueError("Password length must be at least 1!")
    
    # Generate password using random.choices for better randomness
    password = ''.join(random.choices(characters, k=length))
    
    return password


def get_user_preferences():
    """
    Get password generation preferences from the user via command-line input.
    
    Returns:
        tuple: (length, use_letters, use_digits, use_symbols)
    """
    print("\n" + "="*50)
    print("Password Generator")
    print("="*50)
    
    # Get password length
    while True:
        try:
            length = int(input("\nEnter the desired password length: "))
            if length < 1:
                print("Password length must be at least 1. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")
    
    # Get character type preferences
    print("\nSelect character types to include:")
    
    use_letters = input("Include letters (a-z, A-Z)? (y/n, default: y): ").lower()
    use_letters = use_letters != 'n' if use_letters else True
    
    use_digits = input("Include digits (0-9)? (y/n, default: y): ").lower()
    use_digits = use_digits != 'n' if use_digits else True
    
    use_symbols = input("Include special symbols (!@#$%^&* etc.)? (y/n, default: y): ").lower()
    use_symbols = use_symbols != 'n' if use_symbols else True
    
    # Validate that at least one character type is selected
    if not (use_letters or use_digits or use_symbols):
        print("\nError: At least one character type must be selected!")
        print("Defaulting to letters only.")
        use_letters = True
    
    return length, use_letters, use_digits, use_symbols


def display_password_info(length, use_letters, use_digits, use_symbols):
    """Display the password generation settings."""
    print("\n" + "-"*50)
    print("Password Settings:")
    print(f"  Length: {length}")
    print(f"  Letters: {'Yes' if use_letters else 'No'}")
    print(f"  Digits: {'Yes' if use_digits else 'No'}")
    print(f"  Symbols: {'Yes' if use_symbols else 'No'}")
    print("-"*50)


def main():
    """Main function to run the password generator."""
    try:
        while True:
            # Get user preferences
            length, use_letters, use_digits, use_symbols = get_user_preferences()
            
            # Display settings
            display_password_info(length, use_letters, use_digits, use_symbols)
            
            # Generate password
            password = generate_password(length, use_letters, use_digits, use_symbols)
            
            # Display generated password
            print(f"\nGenerated Password: {password}")
            print(f"Password Length: {len(password)} characters")
            
            # Ask if user wants to generate another password
            print("\n" + "="*50)
            another = input("Generate another password? (y/n): ").lower()
            if another != 'y':
                print("\nThank you for using Password Generator!")
                break
            
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
