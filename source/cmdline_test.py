#!/usr/bin/env python3

import sys
import hashlib
import hmac
import base64
import secrets
import re
import datetime
from datetime import timezone
import math

from GoogleOTP import GoogleOTP

# Implementation of Google Authenticator verification

# To generate secrets:
#   secret = generateSecret()
#   print( secret )

# Based on https://github.com/enquirer/enquirer?ref=hackernoon.com
# https://hackernoon.com/how-to-implement-google-authenticator-two-factor-auth-in-javascript-091wy3vh3
#
# License is MIT


class GoogleOTPfileLookup( GoogleOTP ):
    def lookupUserSecret( self, userID ):
        return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

otp = GoogleOTPfileLookup()
#secret = otp.lookupUserSecret( '0001' )

pin = input("Enter 6 digit OTP: ")
bResult = otp.verify( "0001", pin )
#bResult = otp.verifyTOTP(pin, secret, window = 1)

print(bResult)
