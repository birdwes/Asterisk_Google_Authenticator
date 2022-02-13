#!/bin/env python3

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

"""
class GoogleOTP:
    def generateSecret(self):
        secret = secrets.token_bytes(20)
        secretencoded = base64.b32encode(secret).decode("utf-8")
        secretstring = re.sub('=', '',secretencoded,0)
        return secretstring 

    def dynamicTruncationFn(self,hmacValue):
        offset = hmacValue[ len( hmacValue ) - 1] & 0x0f

        return \
            ((hmacValue[offset] & 0x7f) << 24) | \
            ((hmacValue[offset + 1] & 0xff) << 16) | \
            ((hmacValue[offset + 2] & 0xff) << 8) | \
            (hmacValue[offset + 3] & 0xff)
    

    def generateHOTP(self, secret, counter):
        decodedSecret = base64.b32decode( secret )
        liBuffer = []
        for i in range( 8 ):
            liBuffer.insert(0, counter & 0xff )
            counter >>= 8

        bytes = bytearray(liBuffer)

        hmc = hmac.new( decodedSecret, bytes , hashlib.sha1 )
        code = self.dynamicTruncationFn( hmc.digest() )

        return code % 1000000

    def generateTOTP(self, secret, window = 0):
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        counter = math.floor( utc_timestamp / 30 )
        return str( self.generateHOTP(secret, counter + window) ).zfill(6)

    def verifyTOTP(self, token, secret, window = 1):
        if window < 1 or window > 10:
            print( "Window too large" )
            return False

        for errorWindow in range( 0 - window, 1 + window ):
            totp = self.generateTOTP( secret, errorWindow )
            # print( totp )
            if totp == token:
                return True

        return False

    def lookupUserSecret( self, userID ):
        return ""

    def verify( self, userID, pin ):
        secret = self.lookupUserSecret( str( userID ) )
        if len( secret ) == 0:
            return False

        bResult = self.verifyTOTP(pin, secret, window = 1)
        return bResult 
"""

class GoogleOTPfileLookup( GoogleOTP ):
    def lookupUserSecret( self, userID ):
        return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

otp = GoogleOTPfileLookup()
#secret = otp.lookupUserSecret( '0001' )

pin = input("Enter 6 digit OTP: ")
bResult = otp.verify( "0001", pin )
#bResult = otp.verifyTOTP(pin, secret, window = 1)

print(bResult)
