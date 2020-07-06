from flask import Flask, request as Request
import json
import os
import time, datetime
import hashlib
from db import *
import session

app = Flask(__name__)

DB_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "absensi.db"))

db = DB(DB_PATH)
users = UsersTable(db)
kelas = KelasTable(db)
mapel = MapelTable(db)
kelas_mapel_user = Kelas_Mapel_UserTable(db)
absen = AbsenTable(db)

LEVEL = [
	"Admin",
	"Guru",
	"Siswa",
]

_route = app.route

def _new_route(*args, **kwargs):
	print(kwargs["methods"], args[0])
	return _route(*args, **kwargs)

app.route = _new_route

@app.route("/api/login", methods=["POST"])
def _index_():
	username = Request.form.get("username", "")
	password = Request.form.get("password", "")
	tb = users.getByUser(username)
	if tb:
		passwd = hashlib.md5(password.encode("ascii"))
		if passwd.hexdigest() == tb["password"]:
			session.CreateToken(tb["id"], username, passwd.hexdigest())
			return json.dumps({"success": True, "token": session.GetToken(tb["id"]), "id": int(tb["id"])})

	return json.dumps({"success": False})

# get

@app.route("/api/<token>/guru", methods=["GET"])
def _get_guru(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": users.getGuru()})

@app.route("/api/<token>/id", methods=["GET"])
def _get_id(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})
	return json.dumps({"success": True, "id": int(id)})

@app.route("/api/<token>/check", methods=["GET"])
def _check_token(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})
	return json.dumps({"success": True})

@app.route("/api/<token>/label", methods=["GET"])
def _get_level(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": LEVEL[int(users.getLevel(id))]})

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

@app.route("/api/<token>/guru/<id>", methods=["GET"])
def _get_guru_id(token, id):
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": users.getGuru(id)})

@app.route("/api/<token>/siswa/<id>", methods=["GET"])
def _get_siswa_id(token, id):
	id = int(id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": users.getSiswa(id)})

@app.route("/api/<token>/kelas/<id>", methods=["GET"])
def _get_kelas_id(token, id):
	id = int(id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas.getAll(id)})

@app.route("/api/<token>/mapel/<id>", methods=["GET"])
def _get_mapel_id(token, id):
	id = int(id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": mapel.getAll(id)})

@app.route("/api/<token>/kmu/kelas/<user_id>", methods=["GET"])
def _get_kmu_kelas_by_user_id(token, user_id):
	user_id = int(user_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getKelasByUser(user_id)})

@app.route("/api/<token>/kmu/mapel/<kelas_id>", methods=["GET"])
def _get_kmu_mapel_by_kelas_id(token, kelas_id):
	kelas_id = int(kelas_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getMapelByKelas(kelas_id)})

@app.route("/api/<token>/kmu/mapel/<user_id>/<kelas_id>", methods=["GET"])
def _get_kmu_mapel_by_user_id_and_kelas_id(token, user_id, kelas_id):
	user_id = int(user_id)
	kelas_id = int(kelas_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getMapelByUserKelas(user_id, kelas_id)})

@app.route("/api/<token>/kmu/guru_siswa/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_kmu_guru_siswa_by_kelas_id_and_mapel_id(token, kelas_id, mapel_id):
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getUserByKelasMapel(kelas_id, mapel_id)})

@app.route("/api/<token>/kmu/guru/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_kmu_guru_by_kelas_id_and_mapel_id(token, kelas_id, mapel_id):
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getUserByKelasMapelLevel(kelas_id, mapel_id, 1)})

@app.route("/api/<token>/kmu/siswa/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_kmu_siswa_by_kelas_id_and_mapel_id(token, kelas_id, mapel_id):
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getUserByKelasMapelLevel(kelas_id, mapel_id, 2)})

@app.route("/api/<token>/kmu/guru_siswa/noton/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_kmu_guru_siswa_by_noton_kelas_id_and_mapel_id(token, kelas_id, mapel_id):
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getUserByBukanKelasMapel(kelas_id, mapel_id)})

@app.route("/api/<token>/kmu/guru/noton/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_kmu_guru_by_noton_kelas_id_and_mapel_id(token, kelas_id, mapel_id):
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getUserByBukanKelasMapelLevel(kelas_id, mapel_id, 1)})

@app.route("/api/<token>/kmu/siswa/noton/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_kmu_siswa_by_noton_kelas_id_and_mapel_id(token, kelas_id, mapel_id):
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getUserByBukanKelasMapelLevel(kelas_id, mapel_id, 2)})

@app.route("/api/<token>/kmu/all/guru", methods=["GET"])
def _get_kmu_all_guru(token):
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getAllByLevel(1)})

@app.route("/api/<token>/kmu/all/siswa", methods=["GET"])
def _get_kmu_all_siswa(token):
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getAllByLevel(2)})

@app.route("/api/<token>/kmu/all/guru/<user_id>", methods=["GET"])
def _get_kmu_all_guru_by_user_id(token, user_id):
	user_id = int(user_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getAllByUserLevel(user_id, 1)})

@app.route("/api/<token>/kmu/all/siswa/<user_id>", methods=["GET"])
def _get_kmu_all_siswa_by_user_id(token, user_id):
	user_id = int(user_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": kelas_mapel_user.getAllByUserLevel(user_id, 2)})

@app.route("/api/<token>/absen/guru/<user_id>/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_absen_guru(token, user_id, kelas_id, mapel_id):
	user_id = int(user_id)
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": absen.getAbsen(1, user_id, kelas_id, mapel_id)})

@app.route("/api/<token>/absen/siswa/<user_id>/<kelas_id>/<mapel_id>", methods=["GET"])
def _get_absen_siswa(token, user_id, kelas_id, mapel_id):
	user_id = int(user_id)
	kelas_id = int(kelas_id)
	mapel_id = int(mapel_id)
	xid = session.GetId(token)
	if not xid:
		return json.dumps({"success": False})

	return json.dumps({"success": True, "data": absen.getAbsen(2, user_id, kelas_id, mapel_id)})

# create

@app.route("/api/<token>/create/guru", methods=["POST"])
def _create_guru(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	if users.getLevel(id) != 0:
		return json.dumps({"success": False})

	username = Request.form.get("username", "", str)
	password = Request.form.get("password", "", str)
	nomor_induk = Request.form.get("nomor_induk", "", str)
	nama_lengkap = Request.form.get("nama_lengkap", "", str)
	tanggal_lahir = Request.form.get("tanggal_lahir", "", int)
	nomor_telpon = Request.form.get("nomor_telpon", "", str)
	alamat = Request.form.get("alamat", "", str)

	if (not username) or (not password) or (not nomor_induk) or (not nama_lengkap):
		return json.dumps({"success": False})

	if users.createGuru(username, password, nomor_induk, nama_lengkap, tanggal_lahir, nomor_telpon, alamat):
		return json.dumps({"success": True})
	else:
		return json.dumps({"success": False})

@app.route("/api/<token>/create/siswa", methods=["POST"])
def _create_siswa(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	if users.getLevel(id) != 0:
		return json.dumps({"success": False})

	username = Request.form.get("username", "", str)
	password = Request.form.get("password", "", str)
	nomor_induk = Request.form.get("nomor_induk", "", str)
	nama_lengkap = Request.form.get("nama_lengkap", "", str)
	tanggal_lahir = Request.form.get("tanggal_lahir", "", int)
	nomor_telpon = Request.form.get("nomor_telpon", "", str)
	nomor_telpon_ortu = Request.form.get("nomor_telpon_ortu", "", str)
	alamat = Request.form.get("alamat", "", str)

	if (not username) or (not password) or (not nomor_induk) or (not nama_lengkap):
		return json.dumps({"success": False})

	if users.createSiswa(username, password, nomor_induk, nama_lengkap, tanggal_lahir, nomor_telpon, nomor_telpon_ortu, alamat):
		return json.dumps({"success": True})
	else:
		return json.dumps({"success": False})

@app.route("/api/<token>/create/kelas", methods=["POST"])
def _create_kelas(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	if users.getLevel(id) != 0:
		return json.dumps({"success": False})

	nama = Request.form.get("nama", "", str)

	if (not nama):
		return json.dumps({"success": False})

	if kelas.create(nama):
		return json.dumps({"success": True})
	else:
		return json.dumps({"success": False})

@app.route("/api/<token>/create/mapel", methods=["POST"])
def _create_mapel(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	if users.getLevel(id) != 0:
		return json.dumps({"success": False})

	nama = Request.form.get("nama", "", str)

	if (not nama):
		return json.dumps({"success": False})

	if mapel.create(nama):
		return json.dumps({"success": True})
	else:
		return json.dumps({"success": False})

@app.route("/api/<token>/create/kmu", methods=["POST"])
def _create_kmu(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	if users.getLevel(id) != 0:
		return json.dumps({"success": False})

	user_id = Request.form.get("user_id", 0, int)
	kelas_id = Request.form.get("kelas_id", 0, int)
	mapel_id = Request.form.get("mapel_id", 0, int)

	if (not user_id) or (not kelas_id) or (not mapel_id):
		return json.dumps({"success": False})

	if kelas_mapel_user.create(user_id, kelas_id, mapel_id):
		return json.dumps({"success": True})
	else:
		return json.dumps({"success": False})

@app.route("/api/<token>/create/absen", methods=["POST"])
def _create_absen(token):
	id = session.GetId(token)
	if not id:
		return json.dumps({"success": False})

	if not (users.getLevel(id) in [0, 1]):
		return json.dumps({"success": False})

	kmu_id = Request.form.get("kmu_id", 0, int)

	if (not kmu_id):
		return json.dumps({"success": False})

	waktu_masuk = time.localtime()
	waktu_masuk = tuple(waktu_masuk)
	waktu_masuk = waktu_masuk[:4]
	waktu_masuk = datetime.datetime(*waktu_masuk)
	waktu_masuk = int(waktu_masuk.timestamp())

	if absen.create(kmu_id, waktu_masuk):
		return json.dumps({"success": True})
	else:
		return json.dumps({"success": False})

app.run(host="0.0.0.0", port=8080, debug=True)
