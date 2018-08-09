#!/usr/bin/env python

import random
import string

from exceptions import InvalidKeyFormat, InvalidMessageFormat

class PlayfairCipher:
    
    def __init__(self, key):
        self._check_key_validity(key)
        self.key = self._attenuate_key(key)
        self.message = None

    def set_message(self, message):
        self._check_message_validity(message)
        self.message = message

    def _check_key_validity(self, key):
        if len(key)>25 or not key.isupper():
            raise InvalidKeyFormat("Key must be in uppercase and less than 25 characters!")

    def _check_message_validity(self, message):
        if not message.islower():
            raise InvalidMessageFormat("Message must be in lowercase english letters!")

    def _generate_key(self):
        initial_key = list(self.key)
        letters = "".join(string.ascii_lowercase.split('j'))
        for letter in letters:
            if letter not in self.key.lower():
                initial_key.append(letter)
        return initial_key

    def _insert_token_char(self, message, position, repeated_character):
        delimetter = 'z' if repeated_character=='x' else 'x'
        new_message = message[:position] + delimetter + message[position:]
        return new_message

    def _attenuate_key(self, key):
        new_key = key
        for counter in range(0, len(key)):
            if key[counter]=='J':
                if counter==len(key)-1:
                    new_key = new_key[:counter] + 'I'
                else:
                    new_key = new_key[:counter] + 'I' + new_key[counter+1:]
        return new_key

    def _attenuate_message(self, message):
        message = ''.join(char for char in message if char not in '!?,. ;\"\'')
        new_message = message
        for counter in range(0, len(message)):
            if message[counter]=='j':
                if counter==len(message)-1:
                    new_message = new_message[:counter] + 'i'
                else:
                    new_message = new_message[:counter] + 'i' + new_message[counter+1:]
        return new_message

    def _remove_repetetion(self, message):
        prev = message[0]
        new_message = message
        insertions = 0
        for counter in range(1, len(message)):
            if message[counter]==message[counter-1]:
                new_message = self._insert_token_char(new_message, counter+insertions, new_message[counter+insertions])
                insertions += 1
        return new_message

    def _break_message(self, message):
        plain_text = []
        for i in range(0, len(message)-1, 2):
            plain_text.append(message[i:i+2])
        if len(message)%2 is not 0:
            plain_text.append(message[len(message)-1] + random.choice(string.ascii_lowercase))
        return plain_text

    def _process_plain_text(self, message):
        message = self._attenuate_message(message)
        message = self._remove_repetetion(message)
        plain_text = self._break_message(message)
        return plain_text

    def encrypt(self):
        return self._process_plain_text(self.message)

    def decrypt(self):
        pass

a = PlayfairCipher("ANOTHER")
a.set_message("my name is shubham anand!!! xxx heeej")
b = a.encrypt()
print(a._generate_key())
print(b)
