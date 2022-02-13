#!/usr/bin/env python3

from GoogleOTP import GoogleOTP

otp = GoogleOTP()

strSecret = otp.generateSecret()

print("New secret: ",strSecret)
