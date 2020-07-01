import json
import os
import hashlib
import time

_SESSION_FILE_NAME = os.path.realpath(os.path.join(os.path.dirname(__file__), "session.json"))
if not os.path.isfile(_SESSION_FILE_NAME):
	open(_SESSION_FILE_NAME, "w+").close()
	
_SESSION_FILE = open(_SESSION_FILE_NAME, "r+")
if _SESSION_FILE.read() == "":
	_SESSION_FILE.write("{}")
	_SESSION_FILE.close()

class _MyDict(dict):
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		_SESSION_FILE = open(_SESSION_FILE_NAME, "r+")
		data = json.load(_SESSION_FILE)
		_SESSION_FILE.close()
		dict.update(self, data)

	def __setitem__(self, a, b):
		dict.__setitem__(self, a, b)
		_SESSION_FILE = open(_SESSION_FILE_NAME, "w+")
		_SESSION_FILE.write(json.dumps(dict(self.items())))
		_SESSION_FILE.close()

	def __delitem__(self, a):
		dict.__delitem__(self, a)
		_SESSION_FILE = open(_SESSION_FILE_NAME, "w+")
		_SESSION_FILE.write(json.dumps(dict(self.items())))
		_SESSION_FILE.close()

	def update(self, a):
		dict.update(self, a)
		_SESSION_FILE = open(_SESSION_FILE_NAME, "w+")
		_SESSION_FILE.write(json.dumps(dict(self.items())))
		_SESSION_FILE.close()

	def copy(self):
		data = dict.copy(self)
		return _MyDict(data)

_SESSION = _MyDict()

def Add(id, token):
	global _SESSION
	old_token = _SESSION.get(id, None)
	_SESSION[id] = token
	_SESSION[token] = id

	if old_token:
		if _SESSION[old_token] == id:
			del _SESSION[old_token]

def GetID(token):
	return _SESSION.get(token, None)

def GetId(token):
	return GetID(token)

def GetToken(id):
	return _SESSION.get(id, None)

def Set(id, token):
	Add(id, token)

def CreateToken(id, user, passwd):
	sec = int(time.time())
	key = "%d\0%d\0%s\0%s" % (id, sec, user, passwd)
	md5 = hashlib.md5(key.encode("ascii"))
	token = md5.hexdigest()
	Set(id, token)

def Auth(token):
	return not (not session.GetID(token))
