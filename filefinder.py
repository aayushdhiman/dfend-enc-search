import os

def print_info(full_info):
    print('Filename: ' + full_info[0] + '\nFile length: ' + str(full_info[1]) + ' bytes\n' + 'Password length: ' + str(full_info[2]) + ' digits\n' + 
           'Encryption algorithm: ' + str(full_info[3]) + '\nEncryption Mode: ' + full_info[4] + '\n')


def get_password_length(hexfile): 
    password_len = hexfile[18:20]
    int_len = int(password_len, 16)
    return 16 - int_len


def get_enc_algo(hexfile):
    full_hex = hexfile[64:104]

    algor = ''
    if(full_hex[:8] == '00000000'):
        algor = full_hex[18:20]
    elif(int(full_hex[18:20], 16) > 4):
        algor = full_hex[2:4]
    else: 
        algor = full_hex[18:20]


    if(algor == '00'):
        return 'AES'
    elif(algor == '01'):
        return 'Blowfish'
    elif(algor == '02'):
        return 'CAST5'
    elif(algor == '03'):
        return 'IDEA'
    else:
        return 'Unknown'


def get_enc_mode(hexfile):
    enc = hexfile[76:82]
    if(enc == '000000'):
        return 'Electronic Cipherbook'
    else:
        return 'Cipher Blockchaining'


def get_file_length(hexfile):
    file_len = hexfile[10:16]

    if(file_len[2:] == '0000'):
        return int(file_len[:2], 16)
    elif(file_len[4:] == '00'):
        return int(file_len[:4], 16)
    else:
        return(int(file_len, 16))



filepath = input("Enter filepath to search for encrypted files: ")

encrypted = []
signature = "4446454e44"

# filepath = "C:\\Users\\student\\Documents\\working"

file_list = os.listdir(filepath)


for i in range(len(file_list)):
    fileinfo = []
    filename = filepath + "\\" + file_list[i]
    with open(filename, 'rb') as f:
        hexfile = f.read().hex()
        if(hexfile[:10] == signature):
            encrypted.append(filename)
            fileinfo.append(file_list[i])
            
            fileinfo.append(get_file_length(hexfile))            
            fileinfo.append(get_password_length(hexfile))
            fileinfo.append(get_enc_algo(hexfile))
            fileinfo.append(get_enc_mode(hexfile))


            print_info(fileinfo)
