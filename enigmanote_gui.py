import PySimpleGUI as sg
import pyperclip as clipboard
import os.path
from os import path
import time
from smtplib import SMTP, SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected, SMTPSenderRefused, SMTPHeloError
from getpass import getpass
import smtplib, ssl
from email.message import EmailMessage
sg.theme('Default1')
#gui layout
layout = [  [sg.Text('Welcome to Enigma Note.')],
            [sg.Text('Enter rotor 1 setting'), sg.Radio('I', "rotori", default = True, key = 'rotori_one'), sg.Radio('II', "rotori", key = 'rotori_two'), sg.Radio('III', "rotori", key = 'rotori_three')],
            [sg.Text('Enter rotor 2 setting'), sg.Radio('I', "rotorii", default = True, key = 'rotorii_one'), sg.Radio('II', "rotorii", key = 'rotorii_two'), sg.Radio('III', "rotorii", key = 'rotorii_three')],
            [sg.Text('Enter rotor 3  setting'), sg.Radio('I', "rotoriii", default = True, key = 'rotoriii_one'), sg.Radio('II', "rotoriii", key = 'rotoriii_two'), sg.Radio('III', "rotoriii", key = 'rotoriii_three')],
            [sg.Text('Enter ring setting'), sg.InputText('', key ='ringsettingi')],
            [sg.Text('Ring Position'), sg.InputText('', key ='ringpositioni')],
            [sg.Text('Enter Text to Encode/Decode'), sg.InputText('', key ='rawplaintext')],
            [sg.Text('Your Encoded/Decoded Text: '), sg.Text(size=(30,1), key ='cipheroutput')],
            [sg.Button('Enter'), sg.Button('Close'), sg.Button('Help'), sg.Button('Copy Result', visible = False), sg.Button('Save Settings', visible = False), sg.Button('Send as Email', visible = False)]]
mail_layout = [
    [sg.Text('To:'), sg.InputText('', key = 'to_address')],
    [sg.Text('From:'), sg.InputText('', key = 'from_address')],
    [sg.Text('Email password:'), sg.InputText('', password_char='*', key = 'password')],
    [sg.Text('Mail server address: '), sg.Checkbox('Gmail', key = 'gmail'), sg.InputText('Other', key = 'serv_address')],
    [sg.Button('Submit'), sg.Button('Cancel')]]
# Create the Window
window = sg.Window('Enigma Note', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    def rotorRadio(rotor_num): # Translates the rotor selection buttons into roman numerals for the machine to read
        if rotor_num == 'rotori':
            if values['rotori_one'] == True:
                _rotori_ = 'I'
            if values['rotori_two'] == True:
                _rotori_ = 'II'
            if values['rotori_three'] == True:
                _rotori_ = 'III'
            return _rotori_
        if rotor_num == 'rotorii':
            if values['rotorii_one'] == True:
                _rotorii_ = 'I'
            if values['rotorii_two'] == True:
                _rotorii_ = 'II'
            if values['rotorii_three'] == True:
                _rotorii_ = 'III'
            return _rotorii_
        if rotor_num == 'rotoriii':
            if values['rotoriii_one'] == True:
                _rotoriii_ = 'I'
            if values['rotoriii_two'] == True:
                _rotoriii_ = 'II'
            if values['rotoriii_three'] == True:
                _rotoriii_ = 'III'
            return _rotoriii_
    if event == 'Enter':
        # Runs the rotorRadio function 3 times to get the settings of each rotor
        _rotoridecision_ = rotorRadio('rotori') 
        _rotoriidecision_ = rotorRadio('rotorii') 
        _rotoriiidecision_ = rotorRadio('rotoriii')

        # ----------------- Settings ------------------------
        rotors = (_rotoridecision_,_rotoriidecision_, _rotoriiidecision_) #this was harder than it should have been
        reflector = "UKW-B" # Choose between UKW-B and UKW-C
        ringSettings = values['ringsettingi'].upper() #Choose any three letters
        ringPositions = values['ringpositioni'].upper() # Choose any three letters
        plugboard = "AT BS DE FM IR KN LZ OW PV XY" # not too much of a need to change this but whatever makes ya happy!
        # ---------------------------------------------------

        # Behind the curtain...
        def caesarShift(str, amount):
            output = ""

            for i in range(0,len(str)):
                c = str[i]
                code = ord(c)
                if ((code >= 65) and (code <= 90)):
                    c = chr(((code - 65 + amount) % 26) + 65)
                output = output + c
            
            return output

        def encode(plaintext):
            global rotors, reflector,ringSettings,ringPositions,plugboard
            #Rotors and reflectors
            rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            rotor1Notch = "Q"
            rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            rotor2Notch = "E"
            rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
            rotor3Notch = "V"
            rotor4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            rotor4Notch = "J"
            rotor5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
            rotor5Notch = "Z" 
            
            rotorDict = {"I":rotor1,"II":rotor2,"III":rotor3,"IV":rotor4,"V":rotor5}
            rotorNotchDict = {"I":rotor1Notch,"II":rotor2Notch,"III":rotor3Notch,"IV":rotor4Notch,"V":rotor5Notch}  
            
            reflectorB = {"A":"Y","Y":"A","B":"R","R":"B","C":"U","U":"C","D":"H","H":"D","E":"Q","Q":"E","F":"S","S":"F","G":"L","L":"G","I":"P","P":"I","J":"X","X":"J","K":"N","N":"K","M":"O","O":"M","T":"Z","Z":"T","V":"W","W":"V"}
            reflectorC = {"A":"F","F":"A","B":"V","V":"B","C":"P","P":"C","D":"J","J":"D","E":"I","I":"E","G":"O","O":"G","H":"Y","Y":"H","K":"R","R":"K","L":"Z","Z":"L","M":"X","X":"M","N":"W","W":"N","Q":"T","T":"Q","S":"U","U":"S"}
            
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            rotorANotch = False #ehh
            rotorBNotch = False
            rotorCNotch = False
            
            if reflector=="UKW-B":
                reflectorDict = reflectorB
            else:
                reflectorDict = reflectorC
            
            #A = Left,  B = Mid,  C= Right 
            rotorA = rotorDict[rotors[0]]
            rotorB = rotorDict[rotors[1]]
            rotorC = rotorDict[rotors[2]]
            rotorANotch = rotorNotchDict[rotors[0]]
            rotorBNotch = rotorNotchDict[rotors[1]]
            rotorCNotch = rotorNotchDict[rotors[2]]
            
            rotorALetter = ringPositions[0]
            rotorBLetter = ringPositions[1]
            rotorCLetter = ringPositions[2]
            
            rotorASetting = ringSettings[0]
            offsetASetting = alphabet.index(rotorASetting)
            rotorBSetting = ringSettings[1]
            offsetBSetting = alphabet.index(rotorBSetting)
            rotorCSetting = ringSettings[2]
            offsetCSetting = alphabet.index(rotorCSetting)
            
            rotorA = caesarShift(rotorA,offsetASetting)
            rotorB = caesarShift(rotorB,offsetBSetting)
            rotorC = caesarShift(rotorC,offsetCSetting)
            
            if offsetASetting>0:
                rotorA = rotorA[26-offsetASetting:] + rotorA[0:26-offsetASetting]
            if offsetBSetting>0:
                rotorB = rotorB[26-offsetBSetting:] + rotorB[0:26-offsetBSetting]
            if offsetCSetting>0:
                rotorC = rotorC[26-offsetCSetting:] + rotorC[0:26-offsetCSetting]

            ciphertext = ""
            
            #put Conver plugboard settings into a dictionary
            plugboardConnections = plugboard.upper().split(" ")
            plugboardDict = {}
            for pair in plugboardConnections:
                if len(pair)==2:
                    plugboardDict[pair[0]] = pair[1]
                    plugboardDict[pair[1]] = pair[0]
            
            plaintext = plaintext.upper()  
            for letter in plaintext:
                encryptedLetter = letter  
                
                if letter in alphabet:
                    #Rotate Rotors - This happens as soon as a key is pressed
                    rotorTrigger = False
                #Third rotor rotates by 1 for every key being pressed
                if rotorCLetter == rotorCNotch:
                    rotorTrigger = True 
                rotorCLetter = alphabet[(alphabet.index(rotorCLetter) + 1) % 26]
                #Check if rotorB needs to rotate
                if rotorTrigger:
                    rotorTrigger = False
                    if rotorBLetter == rotorBNotch:
                        rotorTrigger = True 
                        rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]
            
                    #Check if rotorA needs to rotate
                    if (rotorTrigger):
                        rotorTrigger = False
                        rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]
                        
                else:
                    #Checks for double step sequence
                    if rotorBLetter == rotorBNotch:
                        rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]
                        rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]
                    
                #Plugboard encryption
                if letter in plugboardDict.keys():
                    if plugboardDict[letter]!="":
                        encryptedLetter = plugboardDict[letter]
                
                #Rotors and Reflector Encryption
                offsetA = alphabet.index(rotorALetter)
                offsetB = alphabet.index(rotorBLetter)
                offsetC = alphabet.index(rotorCLetter)

                # Wheel 3 Encryption
                pos = alphabet.index(encryptedLetter)
                let = rotorC[(pos + offsetC)%26]
                pos = alphabet.index(let)
                encryptedLetter = alphabet[(pos - offsetC +26)%26]
                
                # Wheel 2 Encryption
                pos = alphabet.index(encryptedLetter)
                let = rotorB[(pos + offsetB)%26]
                pos = alphabet.index(let)
                encryptedLetter = alphabet[(pos - offsetB +26)%26]
                
                # Wheel 1 Encryption
                pos = alphabet.index(encryptedLetter)
                let = rotorA[(pos + offsetA)%26]
                pos = alphabet.index(let)
                encryptedLetter = alphabet[(pos - offsetA +26)%26]
                
                # Reflector encryption!
                if encryptedLetter in reflectorDict.keys():
                    if reflectorDict[encryptedLetter]!="":
                        encryptedLetter = reflectorDict[encryptedLetter]
                
                #Back through the rotors 
                # Wheel 1 Encryption
                pos = alphabet.index(encryptedLetter)
                let = alphabet[(pos + offsetA)%26]
                pos = rotorA.index(let)
                encryptedLetter = alphabet[(pos - offsetA +26)%26] 
                
                # Wheel 2 Encryption
                pos = alphabet.index(encryptedLetter)
                let = alphabet[(pos + offsetB)%26]
                pos = rotorB.index(let)
                encryptedLetter = alphabet[(pos - offsetB +26)%26]
                
                # Wheel 3 Encryption
                pos = alphabet.index(encryptedLetter)
                let = alphabet[(pos + offsetC)%26]
                pos = rotorC.index(let)
                encryptedLetter = alphabet[(pos - offsetC +26)%26]
                
                #Implement plugboard encryption!
                if encryptedLetter in plugboardDict.keys():
                    if plugboardDict[encryptedLetter]!="":
                        encryptedLetter = plugboardDict[encryptedLetter]

                ciphertext = ciphertext + encryptedLetter
            
            return ciphertext
        #Temporary fix for spaces
        dirtyplaintext = values['rawplaintext']
        plaintext = dirtyplaintext.replace(' ','placeholdertextiii')
        ciphertext = encode(plaintext)
        cleanedciphertext = ciphertext.replace('PLACEHOLDERTEXTIII', ' ')
        window['cipheroutput'].update(cleanedciphertext)
        #Makes copy and save buttons visible
        window.Element('Copy Result').Update(visible = True) 
        window.Element('Save Settings').Update(visible = True)
        window.Element('Send as Email').Update(visible = True)
        #----------------------------------------------------
    def getEmail():
        window2 = sg.Window('Send Email', mail_layout)
        while True:
            event, values = window2.read()
            if event == 'Submit':
                toaddy = values['to_address']
                fromaddy = values['from_address']
                servaddy = values['serv_address']
                passwordi = values['password']
                gmailaddy = values['gmail']
                TO = toaddy
                FROM = fromaddy
                message = cleanedciphertext
                port = 465  # For SSL
                if gmailaddy == True:
                    serveri = 'smtp.gmail.com'
                else: 
                    serveri = servaddy
                password = passwordi
                # Create a secure SSL context
                context = ssl.create_default_context()
                try: 
                    with smtplib.SMTP_SSL(serveri, port, context=context) as server:
                        server.login(FROM, password)
                        server.sendmail(FROM, TO, message)
                        sg.popup('Email sent Successfully')
                        server.quit()
                except SMTPAuthenticationError:
                    sg.Popup("AUTHENTICATION ERROR: Possible causes: \n Incorrect username/password \n Security settings prohibit access. (example: make sure <less secure app access> is enabled for gmail users)")
                except SMTPConnectError:
                    sg.popup("ERROR: Unable to connect to SMTP server. The server may be down, or you entered it incorrectly. ")
                except SMTPServerDisconnected:
                    sg.popup("ERROR: SMTP Server disconnected unexpectedly")
                except SMTPSenderRefused:
                    sg.popup("ERROR: Sender address refused by server")
                except SMTPHeloError:
                    sg.popup("ERROR: SMTP server refused HELO/EHLO message")
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break 
    def saveStuff():
        rotor_i_save = values['rotori']
        rotor_ii_save = values['rotorii']
        rotor_iii_save = values['rotoriii']
        ring_setting_save = values['ringsettingi']
        ring_position_save = values['ringpositioni']
        with open('machinesettings.txt', 'w') as f:
            f.writelines("""
d88888b d8b   db d888888b  d888b  .88b  d88.  .d8b.       d8b   db  .d88b.  d888888b d88888b 
88'     888o  88   `88'   88' Y8b 88'YbdP`88 d8' `8b      888o  88 .8P  Y8. `~~88~~' 88'     
88ooooo 88V8o 88    88    88      88  88  88 88ooo88      88V8o 88 88    88    88    88ooooo 
88~~~~~ 88 V8o88    88    88  ooo 88  88  88 88~~~88      88 V8o88 88    88    88    88~~~~~ 
88.     88  V888   .88.   88. ~8~ 88  88  88 88   88      88  V888 `8b  d8'    88    88.     
Y88888P VP   V8P Y888888P  Y888P  YP  YP  YP YP   YP      VP   V8P  `Y88P'     YP    Y88888P """)
            f.write('\n------------------------------------------\n')
            f.write('\nSAVED MACHINE STATE\n')
            f.write('\n Rotor Settings: \n')
            f.writelines(rotor_i_save.upper())
            f.write(',')
            f.writelines(rotor_ii_save.upper())
            f.write(',')
            f.writelines(rotor_iii_save.upper())
            f.write('\n Ring Settings: \n')
            f.writelines(ring_setting_save.upper())
            f.write('\n Ring Position: \n')
            f.writelines(ring_position_save.upper())

    if event == 'Copy Result':
        clipboard.copy(cleanedciphertext)
    if event == 'Save Settings':
        saveStuff()
        time.sleep(0.5)
        sg.popup('Machine state saved successfully')
    if event == 'Send as Email':
        getEmail()
    if event == 'Help':
        sg.Popup("""
Setting the rotors: use any combination of the following roman numerals: i,ii,iii \n
Ring Settings and positions: use any combination of 3 latin characters for each \n
Input: The machine is only capable of handling latin alphabetical characters, a-z. Please leave out any punctuation or numbers
""")
        
    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
        break
        
window.close()
