from hashlib import sha256
from Crypto.Cipher import AES
from operator import xor
import numpy as np
import csv
import os
ENCRYPTION_KEY = 'Sixteen byte keySixteen byte key'#32 bytes key
# global row_max 
# global col_max 
def hash_data(data):
    '''
    create hash function
    by using hash = hash_data(data)
    '''
    return sha256(data.encode('utf-8')).digest()
def read_file(filename):
    '''
    read the data from csv file
    '''
    f = open(filename,'r',encoding='utf-8-sig')
    reader = csv.reader(f)
    data = [row for row in reader]
    f.close()
    return data
# xor
xorWord = lambda ss,cc: b''.join(bytes([s^c]) for s,c in zip(ss,cc))

def next_word(data,row):
    '''
    get the next word
    '''
    for i in range(len(data[row])):
        yield data[row][i]
plaintext = 'This is uuuuuuuu'
class AEScipher:
    def __init__(self,key):
        self.key = key
    def encrypt(self,raw):
        iv  = plaintext
        cipher = AES.new(self.key,AES.MODE_CBC,iv)
        return cipher.encrypt(raw)

def encryptFile():
    # global row_max
    # global col_max
    cipher = AEScipher(ENCRYPTION_KEY)
    data = read_file('data.csv')
    row_nums = len(data)
    # row_max = row_nums + 1
    # col_max = len(data[0]) + 1
    encode_file = open('encode_data.enc','wb')
    # writer = csv.writer(encode_file)
    first_word = True
    for row in range(row_nums):
        # Trd = []
        for word in next_word(data,row):
            # print('word:',word)
            if first_word:
                print('first word:',word)
                new_data = xorWord(hash_data(word),ENCRYPTION_KEY.encode('utf-8'))
                last_Trd = cipher.encrypt(new_data)               
                first_word = False
            else:
                print('newWord:',word)
                new_data = xorWord(hash_data(word),last_Trd)
                last_Trd = cipher.encrypt(new_data)
                # Trd = Trd+last_Trd             
            encode_file.write(last_Trd)
            # encode_file.write(os.linesep.encode('GBK'))
        # writer.writerow(Trd)
    encode_file.close()
def search_word(row_max,col_max):
    while True:
        cipher = AEScipher(ENCRYPTION_KEY)
        # f = read_file('encode_data.csv')
        f = open('encode_data.enc','rb')
        data = f.read()
        # row_max = 6
        # col_max = 4
        # print('row_max,col_max:{0}{1}'.format(row_max,col_max))
        row_num = int(input('\ninput row number:'))
        if row_num > row_max:
            row_num = int(input('\nplease re-input row number:'))
        col_num = int(input('\ninput column number:'))
        if col_num > col_max:
            col_num = int(input('\nplease re-input column number:'))
        data_to_search = input('\ninput data:')
        if not data_to_search:
            data_to_search = input('\nyou must input something to search:')
        position = (row_num-1)*col_max+(col_num-1)
        encode_data = data[position*32:position*32+32]
        print('encode_data:',encode_data)
        if row_num == 1 and col_num == 1: 
            new_data = xorWord(hash_data(data_to_search),ENCRYPTION_KEY.encode('utf-8'))
        else:
            Trd = data[(position-1)*32:(position-1)*32+32]
            print('Trd:',Trd)
            new_data = xorWord(hash_data(data_to_search),Trd)
        data_to_exam = cipher.encrypt(new_data)
        print('data_to_exam:',data_to_exam)
        if encode_data == data_to_exam:
            print('True!')
        else:
            print('False!')                
encryptFile()
search_word(row_max=6,col_max=4)