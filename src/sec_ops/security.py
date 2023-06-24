import base64

class SecurityManager:
    def __init__(self):
        pass
    
    def _encode_b64(self, string, encoding="ascii"):
        '''Encode a string to base64'''
        string_bytes = string.encode(encoding)
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string
    
    def _decode_b64(self, b64_string, encoding="ascii"):
        '''Decode a base64 string to string'''
        base64_bytes = b64_string.encode(encoding)
        string_bytes = base64.b64decode(base64_bytes)
        string = string_bytes.decode(encoding)
        return string

    def encode(self, string, method="b64", encoding="ascii", key=None):
        '''Encode a string based on method specified'''
        if method == "b64":
            return self._encode_b64(string, encoding)

        else:
            raise Exception("Security - Method not found for encoding string")
        
    def decode(self, b64_string, method="b64", encoding="ascii", key=None):
        '''Decode a string based on method specified'''
        if method == "b64":
            return self._decode_b64(b64_string, encoding)

        else:
            raise Exception("Security - Method not found for decoding string")