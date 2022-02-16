#!/usr/bin/env python3

# Implementation of Google Authenticator verification

# To generate secrets:
#   secret = generateSecret()
#   print( secret )

# Based on https://github.com/enquirer/enquirer?ref=hackernoon.com
# https://hackernoon.com/how-to-implement-google-authenticator-two-factor-auth-in-javascript-091wy3vh3
#
# License is MIT

"""
The MIT License (MIT)

Copyright (c) 2016-present, Jon Schlinkert.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Modifications to convert to python
    Copyright (c) 2022, Iain W. Bird.
"""

import sys
import hashlib
import hmac
import base64
import secrets
import re
import datetime
from datetime import timezone
import math

class GoogleOTP:
    def generateSecret(self):
        """
        Returns a newly generated secret.

        This would normally be issued to a new user, or
        to replace one where their authenticator device
        has been lost, replaced or compromised.
        """

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
        """
        Abstract placeholder for a derrived class to fetch
        the secret belonging to a specific userID
        """
        return ""

    def verify( self, userID, token ):
        secret = self.lookupUserSecret( str( userID ) )
        if len( secret ) == 0:
            return False

        bResult = self.verifyTOTP(token, secret, window = 1)
        return bResult 
