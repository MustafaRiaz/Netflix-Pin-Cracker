# Generate and print the list of common passwords from 0000 to 9999 in text form
common_passwords_text = '\n'.join([str(i).zfill(4) for i in range(10000)])
print(common_passwords_text)
