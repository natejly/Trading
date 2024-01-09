import robin_stocks.robinhood as robin
import pyotp
from dataframe import get_spy
def login():
    logindir = '/Users/nately/Desktop/login.txt'
    lfile = open(logindir).readlines()
    username = lfile[0][:-1]
    password = lfile[1][:-1]
    totp  = pyotp.TOTP(lfile[2][:-1]).now()
    login = robin.login(username, password, mfa_code=totp)
my_stocks = robin.build_holdings()