import robin_stocks.robinhood as robin
import pyotp
from dataframe import get_spy

totp  = pyotp.TOTP('SP5XR4TP34V26ONP').now()
print(totp)