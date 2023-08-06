# Cryplimp

Cryplimp is a cryptography library that provides functions for encrypting and decrypting messages using the AES algorithm in CBC mode.

Installation
------------
You can install Cryplimp using pip:

    pip install cryplimp

Usage
-----
To encrypt a message, import the `encrypt` function from the `cryplimp` module and pass in the message and key as arguments:

    from cryplimp import encrypt
    
    message = "hello world"
    key = "secret key"
    
    encrypted_message = encrypt(message, key)

To decrypt the encrypted message, import the `decrypt` function from the `cryplimp` module and pass in the encrypted message and key as arguments:

    from cryplimp import decrypt
    
    decrypted_message = decrypt(encrypted_message, key)

License
-------
Cryplimp is licensed under the MIT License. See LICENSE for more information.
