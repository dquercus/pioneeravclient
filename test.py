from pioneeravclient import *

a = PioneerAvClient.factory('VSX-528', '192.168.2.12')

#print a.isOn()
#a.setInput(a.INPUTS['BD'])
print a.getVolPer()
#a.switchOn()
#a.switchOff()
#print a.getInput()

