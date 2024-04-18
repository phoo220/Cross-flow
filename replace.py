file_name = 'Wind_Daily.INC'
search_value = ' 300 '
replace_value = '250'

# Read the content of the file
with open(file_name, 'r') as file:
    content = file.read()

# Replace the desired value
new_content = content.replace(search_value, replace_value)

# Write the modified content back to the file
with open(file_name, 'w') as file:
    file.write(new_content)

print(f"Value {search_value} replaced with {replace_value} in {file_name}")
