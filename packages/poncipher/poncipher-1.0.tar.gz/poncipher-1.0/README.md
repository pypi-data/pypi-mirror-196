# PonCipher
### PonCipher is library for encoding data (include your Python projects)
```python
from poncipher import PonCipher
pon = PonCipher()

# Encoding main.py file and writing encoded content to encoded.txt file
with open("main.py", "r", encoding="utf-8") as source_file:
    with open("encoded.txt", "w", encoding="utf-8") as encoded_file:
        source = source_file.read()

        encoded = pon.encode(
            content = source, # Source file content (or string)
            key = "YOUR_KEY", # Cipher key
            line_length = 30, # Length of line in encoded file
            compress = False, # If true, enables zlib compress
        )
        encoded_file.write(encoded)

# Decoding main.py file and running it with exec()
with open("encoded.txt", "r", encoding="utf-8") as encoded_file:
    encoded = encoded_file.read()

    decoded = pon.decode(
        content = encoded, # Encoded file (or string)
        key = "YOUR_KEY",  # Cipher key
    )
    exec(decoded)
```