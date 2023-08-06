import random
__version__="1.1"
text="bonjour"
carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","'","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
def generate_key():
    carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","'","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
    random.shuffle(carac)
    key=carac
    return key
def generate_in(key):
    incode={}
    for i in range(len(key)):
        incode.update({carac[i]:key[i]})
    return incode
def generate_un(key):
    uncode={}
    for i in range(len(key)):
        uncode.update({key[i]:carac[i]})
    return uncode
def code(text,incode):
    newtext=""
    for i in range(len(text)):
        newtext=newtext+incode[text[i]]
    return newtext
def decode(test,uncode):
    newtext=""
    for i in range(len(test)):
        newtext=newtext+uncode[test[i]]
    return newtext
if __name__=="__main__":
    keya=generate_key()
    print(keya)
    incodea=generate_in(keya)
    print(incodea)
    uncodedea=generate_un(keya)
    print(uncodedea)
    icode=code(text,incodea)
    print(icode)
    decod=decode(icode,uncodedea)
    print(decod)