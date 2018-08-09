#!/usr/bin/env python

import random
import string

from exceptions import InvalidKeyFormat, InvalidMessageFormat

class PlayfairCipher:
    
    def __init__(self, key):
        self._check_key_validity(key)
        self.key = self._attenuate_key(key)
        self.keymap = self._generate_keymap()
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

    def _generate_key(self, key):
        initial_key = list(key)
        letters = "".join(string.ascii_uppercase.split('J'))
        for letter in letters:
            if letter not in key:
                initial_key.append(letter)
        return initial_key

    def _generate_keymap(self):
        key = self._generate_key(self.key)
        keymap = []
        for i in range(0,5):
            submap = []
            for j in range(0,5):
                submap.append(key[(i*5)+j])
            keymap.append(submap)
        return keymap

    def _get_right(self, x, y):
        index = y+1 if y+1<5 else 0
        return self.keymap[x][index]

    def _get_below(self, x, y):
        index = x+1 if x+1<5 else 0
        return self.keymap[index][y]

    def _get_left(self, x, y):
        index = y-1 if y-1>=0 else 4
        return self.keymap[x][index]

    def _get_top(self, x, y):
        index = x-1 if x-1>=0 else 0
        return self.keymap[index][y]
        
    def _is_same_row(self, l1, l2):
        search_l1 = self._search_letter(l1)
        search_l2 = self._search_letter(l2)
        if search_l1[0]==search_l2[0]:
            return (True, "{0}{1}".format(
                self._get_right(search_l1[0], search_l1[1]), 
                self._get_right(search_l2[0], search_l2[1])
            ))
        return (False, None)

    def _is_same_column(self, l1, l2):
        search_l1 = self._search_letter(l1)
        search_l2 = self._search_letter(l2)
        if search_l1[1]==search_l2[1]:
            return (True, "{0}{1}".format(
                self._get_below(search_l1[0], search_l1[1]), 
                self._get_below(search_l2[0], search_l2[1])
            ))
        return (False, None)

    def _matrix_match(self, l1, l2):
        search_l1 = self._search_letter(l1)
        search_l2 = self._search_letter(l2)
        return "{0}{1}".format(
            self.keymap[search_l1[0]][search_l2[1]],
            self.keymap[search_l2[0]][search_l1[1]]
        )

    def _search_letter(self, letter):
        for i in range(0,5):
            for j in range(0,5):
                if self.keymap[i][j] == letter:
                    return (i, j)

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
        if self.message is None:
            raise NoMessageAttached("Please attach a message by calling the set_message method!")

        encrypted_message = ""

        plain_text = self._process_plain_text(self.message)

        for text in plain_text:
            same_row_try = self._is_same_row(text[:1].upper(), text[1:].upper())
            same_column_try = self._is_same_column(text[:1].upper(), text[1:].upper())
            if same_row_try[0]:
                encrypted_message += same_row_try[1]
            elif same_column_try[0]:
                encrypted_message += same_column_try[1]
            else:
                encrypted_message += self._matrix_match(text[:1].upper(), text[1:].upper())
        
        return encrypted_message


    def decrypt(self):
        pass

a = PlayfairCipher("ANOTHER")
a.set_message("we live in a world full of beauty")
b = a.encrypt()
print(b)
