print("""
d88888b d8b   db d888888b  d888b  .88b  d88.  .d8b.       d8b   db  .d88b.  d888888b d88888b 
88'     888o  88   `88'   88' Y8b 88'YbdP`88 d8' `8b      888o  88 .8P  Y8. `~~88~~' 88'     
88ooooo 88V8o 88    88    88      88  88  88 88ooo88      88V8o 88 88    88    88    88ooooo 
88~~~~~ 88 V8o88    88    88  ooo 88  88  88 88~~~88      88 V8o88 88    88    88    88~~~~~ 
88.     88  V888   .88.   88. ~8~ 88  88  88 88   88      88  V888 `8b  d8'    88    88.     
Y88888P VP   V8P Y888888P  Y888P  YP  YP  YP YP   YP      VP   V8P  `Y88P'     YP    Y88888P 
""")
print("")
print("##################################################################################################")
print("")
print("Remember to keep your settings in a safe place if you want to be able to decrypt your notes")
print("Press ENTER to begin")
input()
print("##################################################################################################")
# Manual settings input by user
rotori = input("Rotor 1 setting? (Enter a roman numeral from I to V): ")
rotorii = input("Rotor 2 setting? (Enter a roman numeral from I to V): ")
rotoriii = input("Rotor 3 setting? (Enter a roman numeral from I to V): ")
# ----------------- Settings ------------------------
rotors = (rotori,rotorii,rotoriii)
reflector = "UKW-B" # Choose between UKW-B and UKW-C
ringSettings ="ABC" #Choose any three letters
ringPositions = "DEF" # Choose any three letters
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
  rotorANotch = False
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


# in front of the curtain...
plaintext = input("Enter text to encode or decode:\n")
ciphertext = encode(plaintext)

print("\nEncoded text: \n " + ciphertext)
print("")
print("Press ENTER to close program")
input()