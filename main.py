#!/usr/bin/env python

from PlayfairCipher import PlayfairCipher

if __name__=='__main__':
    cipher = PlayfairCipher('MYSECRETCODY')
    cipher.set_message("helelele my name is ashubham")
    encrypted_message = cipher.encrypt()
    print(encrypted_message)
    cipher.set_encrypted_message(encrypted_message)
    print(cipher.decrypt())