import hashlib
import uuid


salt = '405e45c08f7f4fa798e323b59cab69e4'


def encrypt(password):
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    pwd = 'Register123456'
    print('Password: {pwd}')

    for _ in range(10):
        encrypted = encrypt(pwd)
        print('-----------------------------------------')
        print(f'Ecnrypted: {encrypted}, {len(encrypted)}')
