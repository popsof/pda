import re

str = "01024956962"
pattern = re.compile(r"(\d{3})(\d{4})(\d{4})")

new_str = pattern.sub( r"\1-\2-\3", str )
print( new_str )

#result = re.match( pattern, str )
#if result:
#    phone = '-'.join(result.groups())
#
#print(phone)
