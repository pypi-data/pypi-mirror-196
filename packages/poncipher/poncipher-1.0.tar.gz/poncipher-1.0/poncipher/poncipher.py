class PonCipher:
    _base64 = __import__("base64")
    _zlib = __import__("zlib")

    def _zlibcompress(self, data: str):
        data = data.encode("utf-8")
        compressed = self._zlib.compress(data, level=-1)
        return compressed.hex()

    def _zlibdecompress(self, data: str):
        data = bytes.fromhex(data)
        decompressed = self._zlib.decompress(data)
        return decompressed.decode("utf-8")

    def encode(
        self, content: str, key: str, line_length: int = 50, compress: bool = False
    ):
        if compress:
            content = self._zlibcompress(content)

        start_line = "START ===="
        end_line = "END ======"

        if line_length < 10:
            raise ValueError(f"Line length cannot be smaller than 10.")

        if line_length > len(start_line):
            add = line_length - 10
            start_line += "=" * add
            end_line += "=" * add

        encrypted = ""
        for i in range(len(content)):
            encrypted += chr(ord(content[i]) ^ ord(key[i % len(key)]))

        encrypted = self._base64.b64encode(encrypted.encode("utf-8")).decode("utf-8")
        parts = [
            encrypted[i : i + line_length]
            for i in range(0, len(encrypted), line_length)
        ]

        result = start_line + "\n" + "\n".join(parts) + "\n" + end_line

        if compress:
            result += "\nZLIB =====" + ("=" * (line_length - 10))

        return result

    def decode(self, content: str, key: str):
        if "ZLIB =====" in content:
            compress = True

        else:
            compress = False

        content_extracted = ""

        is_lines_encoded = False

        for line in content.split("\n"):
            if line.startswith("END ======"):
                is_lines_encoded = False

            if is_lines_encoded:
                content_extracted += line.strip()

            if line.startswith("START ===="):
                is_lines_encoded = True

        content = self._base64.b64decode(content_extracted.encode("utf-8")).decode(
            "utf-8"
        )
        decrypted = ""
        for i in range(len(content)):
            decrypted += chr(ord(content[i]) ^ ord(key[i % len(key)]))

        if compress:
            decrypted = self._zlibdecompress(decrypted)

        return decrypted
