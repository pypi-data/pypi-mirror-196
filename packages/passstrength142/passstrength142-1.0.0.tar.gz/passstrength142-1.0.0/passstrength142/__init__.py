from password import check_password_strength, generate_random_password

option = input("Enter 1 to check password strength or 2 to generate a random password: ")

if option == "1":
    password = input("Enter password to check: ")
    check_password_strength(password)
elif option == "2":
    length = int(input("Enter length of password to generate: "))
    password = generate_random_password(length)
    print("Generated password:", password)
else:
    print("Invalid option. Please enter 1 or 2.") 