from random import randint, choices
import string


romek = "".join(choices(string.digits, k=13))
print(romek)