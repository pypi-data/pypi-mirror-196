def vigenere(encdec, msg, key):
    if encdec == 'encode':
        checkinmessage = []
        punctuation = []
        encodelist = []
        for i, c in enumerate(msg):
            if ord(c) >= 65 and ord(c) <= 90 or ord(c) >= 97 and ord(c) <= 122:
                checkinmessage.append(c)
            else:
                punctuation.append(i)
                punctuation.append(c)

        newmsg = list('_' * len(''.join(checkinmessage)))
        for x in key:
            if ord(x) >= 65 and ord(x) <= 90:
                encodelist.append(ord(x) - 65)
            if ord(x) >= 97 and ord(x) <= 122:
                encodelist.append(ord(x) - 97)
        for z in range(0, len(key)):
            for y in range(0 + z, len(''.join(checkinmessage)), len(key)):
                if ord(''.join(checkinmessage)[y]) >= 65 and ord(''.join(checkinmessage)[y]) <= 90:
                    newmsg[y] = chr((ord(''.join(checkinmessage)[y]) - ord('A') + encodelist[z]) % 26 + ord('A'))
                elif ord(''.join(checkinmessage)[y]) >= 97 and ord(''.join(checkinmessage)[y]) <= 122:
                    newmsg[y] = chr((ord(''.join(checkinmessage)[y]) - ord('a') + encodelist[z]) % 26 + ord('a'))
        for i, c in enumerate(punctuation):
            if i % 2 == 0:
                newmsg.insert(int(c), punctuation[i + 1])
    elif encdec == 'decode':
        checkinmessage = []
        punctuation = []
        encodelist = []
        for i, c in enumerate(msg):
            if ord(c) >= ord('A') and ord(c) <= ord('Z') or ord(c) >= ord('a') and ord(c) <= ord('z'):
                checkinmessage.append(c)
            else:
                punctuation.append(i)
                punctuation.append(c)

        newmsg = list('_' * len(''.join(checkinmessage)))
        for x in key:
            x = x.lower()
            if ord(x) >= ord('a') and ord(x) <= ord('z'):
                encodelist.append(ord(x) - ord('a'))
        for z in range(0, len(key)):
            # instead of + encodelist[z] it is - encode list z so it takes away the shift instead of adding it
            for y in range(0 + z, len(''.join(checkinmessage)), len(key)):
                if ord(''.join(checkinmessage)[y]) >= ord('A') and ord(''.join(checkinmessage)[y]) <= ord('Z'):
                    newmsg[y] = chr((ord(''.join(checkinmessage)[y]) - ord('A') - encodelist[z]) % 26 + ord('A'))
                elif ord(''.join(checkinmessage)[y]) >= ord('a') and ord(''.join(checkinmessage)[y]) <= ord('z'):
                    newmsg[y] = chr((ord(''.join(checkinmessage)[y]) - ord('a') - encodelist[z]) % 26 + ord('a'))
        for i, c in enumerate(punctuation):
            if i % 2 == 0:
                newmsg.insert(int(c), punctuation[i + 1])
    else:
        newmsg = 'Error'
    return ''.join(newmsg)
