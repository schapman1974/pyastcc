def reverse(str):
    "Reverse the string str"
    buf = ""
    a = 0
    while (a < len(str)):
        a += 1
        buf += str[-a]
    return buf

def doubler(digit):
    "Double digit, add its digits together if they are >= 10"
    digit = int(digit)
    digit = digit * 2
    if digit < 0:
        print("Error!  digit < 0 sent: " + str(digit))
        sys.exit(1)
    if digit > 18:
        print("Error!  digit > 18 sent: " + str(digit))
        sys.exit(1)
    if digit < 10:
        return digit
    return digit - 9

def checkcc(cc):
    "Given a cc number (string), will return True if it passes mod10 check, False otherwise"
    cc = reverse(cc)
    a = 0
    total = 0
    while (a < len(cc)):
           if (a % 2) == 1:
               total = total + doubler(cc[a])
           else:
               total = total + int(cc[a])
           a += 1
    if (total % 10) == 0:
        return True
    else:
        return False

def cardtype(prefix,thelen):
    if prefix[0:1]=="4":
      return "visa"
    if int(prefix[0:2])>=51 and int(prefix[0:2])<=55:
      return "mastercard"
    if prefix[0:2]=="34" or prefix[0:2]=="37":
      return "amex"
    if prefix[0:4]=="6011":
      return "discover"
    if int(prefix[0:6])>=622126 and int(prefix[0:6])<=622925:
      return "discover"
    if int(prefix[0:3])>=644 and int(prefix[0:3])<=649:
      return "discover"
    if prefix[0:2]=="65":
      return "discover"
    return "unsupported"
