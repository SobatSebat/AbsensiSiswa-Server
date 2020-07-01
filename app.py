from flask import Flask, request as Request
import json
import os
import hashlib
from db import *
import session

app = Flask(__name__)

DB_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "absensi.db"))

db = DB(DB_PATH)
users = UsersTable(db)
kelas = KelasTable(db)
mapel = MapelTable(db)
kelas_user = Kelas_UserTable(db)
mapel_user = Mapel_UserTable(db)

@app.route("/api/login", methods=["POST"])
def _index_():
	username = Request.form.get("username", "")
	password = Request.form.get("password", "")
	tb = users.getByUser(username)
	if tb:
		passwd = hashlib.md5(password.encode("ascii"))
		if passwd.hexdigest() == tb[2]:
			session.CreateToken(tb[0], username, passwd.hexdigest())
			return json.dumps({"success": True, "token": session.GetToken(tb[0])})

	return json.dumps({"success": False})


@app.route("/api/<token>/guru", methods=["GET"])
def _get_guru(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": users.getGuru()})

@app.route("/api/<token>/siswa", methods=["GET"])
def _get_siswa(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": users.getSiswa()})

@app.route("/api/<token>/kelas", methods=["GET"])
def _get_kelas(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas.getAll()})

@app.route("/api/<token>/mapel", methods=["GET"])
def _get_mapel(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": mapel.getAll()})

@app.route("/api/<token>/kelas_user", methods=["GET"])
def _get_kelas_user(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_user.getAll()})

@app.route("/api/<token>/kelas_user/guru", methods=["GET"])
def _get_kelas_user_guru(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_user.getGuru()})

@app.route("/api/<token>/kelas_user/siswa", methods=["GET"])
def _get_kelas_user_siswa(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_user.getSiswa()})

@app.route("/api/<token>/mapel_user", methods=["GET"])
def _get_mapel_user(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": mapel_user.getAll()})

@app.route("/api/<token>/mapel_user/guru", methods=["GET"])
def _get_mapel_user_guru(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": mapel_user.getGuru()})

@app.route("/api/<token>/mapel_user/siswa", methods=["GET"])
def _get_mapel_user_siswa(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": mapel_user.getSiswa()})

app.run(host="0.0.0.0", port=8080, debug=True)
