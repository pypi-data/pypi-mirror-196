import sys
sys.path.append("../src")
from zbrowser.chrome import Chrome


chrome = Chrome()
chrome.go('http://19lou.com')
print(chrome.html)