# Asterisk AGI Script for Google Authenticator
 AGI Script for Asterisk to use the Google Authenticator OTP (one time password) app.

## Abstract

This Asterisk AGI script, written in python3, allows user authentication using the Google Authenticator.

[for Android](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB&gl=US)

[for Apple](https://apps.apple.com/gb/app/google-authenticator/id388497605)

The authentication code changes every 30 seconds, offering a much higher degree of security than a simple userID and PIN combination.

### Motivation

If you are using your Asterisk server to control remote devices, e.g. for a reboot request or other operation which could disrupt service, you require more security than a simple userID and PIN.

If the RTP stream from your call were to be intercepted, it would be trivial for a nefarious actor to extract your userID and PIN [(Voice-over-IP Sniffing Attack)](https://www.giac.org/paper/gcih/442/voice-over-ip-sniffing-attack/104883).  Using an OTP mechanism such as Google Authenticator greatly protects against this type of attack.

## This example

The main script file is named `astotp.py`

You should extract the contents of the source folder into the folder:

`/var/lib/asterisk/agi-bin/otp`

or, wherever AGI scripts run on your server.  You will need to create the `otp` subfolder.  You might wish to move the sounds somewhere else.

In your `extensions.conf`, you can insert something like this:

```
; It is extremely important to check the ${ASTOTP} variable result, as a
; missing script or python exception could cause a bypass
exten => 777,1,Answer
 same => n,Set(ASTOPT="")
 same => n,AGI(otp/astotp.py)
 same => n,GotoIf($["${ASTOTP}" == "SUCCESS"]?auth_success)
 same => n(hangup),NoOp
 same => n,Hangup()
 same => n(auth_success),NoOp
 same => n,MusicOnHold(default,60)
```

You will need to edit `astotp.py` to provide a file or database lookup mechanism.  This example is hard-coded for example purposes.

The secret to enter into the Google Authenticator app for this demo is in function
```
def lookupUserSecret( self, userID ):
	return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
```

These are normally added by use of a QR code.  If you would like to contribute by writing such code, please feel free to contact me.

UserID and PIN are in function

```
def lookupUserPin( self, userID ):
```

When you authenticate successfully, you will be rewarded with some hold music, otherwise you should get a "goodbye" and hangup.  In reality, you would progress to your control IVR menu.
