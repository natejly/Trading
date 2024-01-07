import robin_stocks.robinhood as robin
import pyotp
from dataframe import get_spy
def login():
    logindir = 'login.txt'
    lfile = open(logindir).readlines()
    print(lfile)
    username = lfile[0][:-1]
    print(username)
    password = lfile[1][:-1]
    print(password)
    key = lfile[2][:-1]
    print(key)

    totp  = pyotp.TOTP(key).now()
    print(totp)
    #login = robin.login(username, password, mfa_code=totp)
login()
# my_stocks = robin.build_holdings()
# for key,value in my_stocks.items():
#     print(key,value)