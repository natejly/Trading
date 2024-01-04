import robin_stocks.robinhood as robin
import pyotp
totp  = pyotp.TOTP("SP5XR4TP34V26ONP").now()
logindir = '/Users/nately/Documents/login.txt'
lfile = open(logindir).readlines()
username = lfile[0][:-1]
password = lfile[1][:-1]
login = robin.login(username, password, mfa_code=totp)
my_stocks = robin.build_holdings()
for key,value in my_stocks.items():
   print(key,value)
####