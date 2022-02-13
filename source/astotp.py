#!/bin/env python3

"""
MIT License

Copyright (c) 2022 Iain W. Bird

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# See https://github.com/rdegges/pyst2
# pip install pyst2

# Asterisk CLI debug
# agi set debug on

# WAV prompts were recorded from this:
# https://www.ibm.com/demos/live/tts-demo/self-service/home

from asterisk.agi import *
from GoogleOTP import GoogleOTP
import os


# This class is hard-coded for demonstration purposes only.
# Replace the methods too look up from a file or a database.

class GoogleOTPfileLookup( GoogleOTP ):
    def lookupUserSecret( self, userID ):
        return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    def lookupUserPin( self, userID ):
        if userID == "0001":
            return "1234"
        if userId == "0002":
            return "5678"
        return ""

# End of class



def getDigits( agi, nDigits ):
    strResult = ""
    for x in range( nDigits ):
        try:
            result = agi.wait_for_digit(7000)
        except AGIError:
            result = ""

        if result.isdigit():
            strResult += result
        else:
            return ""

    return strResult

agi = AGI()
otp = GoogleOTPfileLookup()

agi.verbose( os.getcwd() )
# Path to the audio files
path = "/var/lib/asterisk/agi-bin/otp/sounds/"

# raise AGIError("TEST")

agi.control_stream_file( path + "need_to_be_authenticated")
agi.wait_for_digit(1000)    # Not getting digits, just a pause

for retries in range(3):
    agi.control_stream_file( path + "please_enter_userid")
    userId = getDigits(agi,4)
    if userId == "":
        if retries < 2:
            agi.control_stream_file( path + "please_try_again")
        else:
            agi.wait_for_digit(1000)    # Not getting digits, just a pause
            agi.control_stream_file( path + "goodbye")
            agi.hangup()
    else:
        break

agi.control_stream_file( path + "thank_you")
expected_pin = otp.lookupUserPin( userId )

blnMatch = False

for retries in range(3):
    agi.control_stream_file( path + "enter_pin")
    pin = getDigits(agi,4)
    if pin != expected_pin:
        agi.control_stream_file( path + "did_not_match")
        if retries < 2:
            agi.control_stream_file( path + "please_try_again")
    else:
        blnMatch = True
        break

if blnMatch == False:
    agi.wait_for_digit(1000)    # Not getting digits, just a pause
    agi.control_stream_file( path + "goodbye")
    agi.hangup()

blnMatch = False

for retries in range(3):
    agi.control_stream_file( path + "enter_authenticator_code")
    otpcode = getDigits(agi,6)
    if otp.verify( userId, otpcode ):
        blnMatch = True
        break
    else:
        agi.control_stream_file( path + "did_not_match")
        if retries < 2:
            agi.control_stream_file( path + "please_try_again")

if blnMatch == False:
    agi.wait_for_digit(1000)    # Not getting digits, just a pause
    agi.control_stream_file( path + "goodbye")
    agi.hangup()

agi.control_stream_file( path + "auth_success")
agi.wait_for_digit(1000)    # Not getting digits, just a pause
agi.set_variable("ASTOTP","SUCCESS")


