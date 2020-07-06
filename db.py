import sqlite3 as SQL
import hashlib

class DB :
	def __init__(self, fn="absensi.db"):
		self.sql = SQL.connect(fn, check_same_thread=False)
		self.sql.row_factory = self.row

	def cursor(self):
		return self.sql.cursor()

	def row(self, *args, **kwargs):
		return dict(SQL.Row(*args, **kwargs))

class Table():

	def __init__(self, db):
		self.db = db

	@property
	def table_name(self):
		return type(self).__name__.lower().replace("table", "")


	def getAll(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM {};".format(self.table_name))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def createPassword(self, txt):
		txt = txt.encode("ascii")
		md5 = hashlib.md5(txt)
		return md5.hexdigest()

class UsersTable(Table):
	def getByUser(self, user):
		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM {} WHERE username=?;".format(self.table_name), (user,))
		ret = cursor.fetchall()
		cursor.close()

		if len(ret) != 1:
			return

		return ret[0]

	def getLevel(self, id):
		cursor = self.db.cursor()
		cursor.execute("SELECT level FROM {} WHERE id=?;".format(self.table_name), (id,))
		ret = cursor.fetchall()
		cursor.close()

		if len(ret) != 1:
			return

		ret = ret[0]["level"]

		return ret

	def getByLevel(self, level, id=None):
		cursor = self.db.cursor()
		i = "AND id = ?"
		v = (level, id)
		if not id:
			i = ""
			v = (level,)

		if(level == 1):
			cursor.execute("SELECT id, nomor_induk, nama_lengkap, username, tanggal_lahir, nomor_telpon, alamat FROM {} WHERE level=? {};".format(self.table_name, i), v)
		else:
			cursor.execute("SELECT id, nomor_induk, nama_lengkap, username, tanggal_lahir, nomor_telpon, nomor_telpon_ortu, alamat FROM {} WHERE level=? {};".format(self.table_name, i), v)
		ret = cursor.fetchall()
		cursor.close()

		if id:
			if len(ret) == 1:
				ret = ret[0]
			else:
				ret = None

		return ret

	def getGuru(self, id=None):
		return self.getByLevel(1, id)

	def getSiswa(self, id=None):
		return self.getByLevel(2, id)

	def create(self, level, username, password, nomor_induk, nama_lengkap, tanggal_lahir=None, nomor_telpon=None, nomor_telpon_ortu=None, alamat=None):
		try:
			cursor = self.db.cursor()
			password = self.createPassword(password)
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (level, username, password, nomor_induk, nama_lengkap, tanggal_lahir, nomor_telpon, nomor_telpon_ortu, alamat) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);".format(self.table_name), (level, username, password, nomor_induk, nama_lengkap, tanggal_lahir, nomor_telpon, nomor_telpon_ortu, alamat))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

	def createGuru(self, username, password, nomor_induk, nama_lengkap, tanggal_lahir, nomor_telpon, alamat):
		level = 1
		return self.create(level, username, password, nomor_induk, nama_lengkap, tanggal_lahir=tanggal_lahir, nomor_telpon=nomor_telpon, nomor_telpon_ortu=None, alamat=alamat)

	def createSiswa(self, username, password, nomor_induk, nama_lengkap, tanggal_lahir, nomor_telpon, nomor_telpon_ortu, alamat):
		level = 2
		return self.create(level, username, password, nomor_induk, nama_lengkap, tanggal_lahir=tanggal_lahir, nomor_telpon=nomor_telpon, nomor_telpon_ortu=nomor_telpon_ortu, alamat=alamat)

class KelasTable(Table):
	def getAll(self, id=None):
		if not id:
			return Table.getAll(self)

		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM {} WHERE id = ?;".format(self.table_name), (id,))
		ret = cursor.fetchall()
		cursor.close()

		if len(ret) == 1:
			ret = ret[0]
		else:
			ret = None

		return ret

	def create(self, nama):
		try:
			cursor = self.db.cursor()
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (nama) VALUES(?);".format(self.table_name), (nama,))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

class MapelTable(Table):
	def getAll(self, id=None):
		if not id:
			return Table.getAll(self)

		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM {} WHERE id = ?;".format(self.table_name), (id,))
		ret = cursor.fetchall()
		cursor.close()

		if len(ret) == 1:
			ret = ret[0]
		else:
			ret = None

		return ret

	def create(self, nama):
		try:
			cursor = self.db.cursor()
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (nama) VALUES(?);".format(self.table_name), (nama,))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

class Kelas_UserTable(Table):
	def getAll(self, id=None, kelas_id=None, user_id=None, level=None):
		i = ""
		v = tuple()
		if id:
			i = " AND kelas_user.id = ?"
			v = (id,)
		if kelas_id:
			i = " AND kelas.id = ?"
			v = (kelas_id,)
		if user_id:
			i = " AND users.id = ?"
			v = (user_id,)

		if level:
			i += " AND users.level = ?"
			v += (level,)

		cursor = self.db.cursor()
		cursor.execute("SELECT kelas_user.id, kelas_user.user_id, kelas_user.kelas_id, users.nama_lengkap, users.level, kelas.nama FROM kelas_user JOIN kelas JOIN users WHERE users.id = kelas_user.user_id AND kelas.id = kelas_user.kelas_id %s;" % i, v)
		ret = cursor.fetchall()
		cursor.close()

		return ret

	def getByLevel(self, level):
		cursor = self.db.cursor()
		cursor.execute("SELECT kelas_user.id, kelas_user.user_id, kelas_user.kelas_id, users.nama_lengkap, kelas.nama FROM kelas_user JOIN kelas JOIN users WHERE users.id = kelas_user.user_id AND kelas.id = kelas_user.kelas_id AND users.level = ?;", (level,))
		ret = cursor.fetchall()
		cursor.close()

		return ret

	def getGuru(self):
		return self.getByLevel(1)

	def getSiswa(self):
		return self.getByLevel(2)

	def create(self, kelas_id, user_id):
		try:
			cursor = self.db.cursor()
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (kelas_id, user_id) VALUES(?, ?);".format(self.table_name), (kelas_id, user_id))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

class Mapel_UserTable(Table):
	def getAll(self, id=None, mapel_id=None, user_id=None, level=None):
		i = ""
		v = tuple()
		if id:
			i = " AND mapel_user.id = ?"
			v = (id,)
		if mapel_id:
			i = " AND mapel.id = ?"
			v = (mapel_id,)
		if user_id:
			i = " AND users.id = ?"
			v = (user_id,)

		if level:
			i += " AND users.level = ?"
			v += (level,)

		cursor = self.db.cursor()
		cursor.execute("SELECT mapel_user.id, mapel_user.user_id, mapel_user.mapel_id, users.nama_lengkap, mapel.nama FROM mapel_user JOIN mapel JOIN users WHERE users.id = mapel_user.user_id AND mapel.id = mapel_user.mapel_id %s;" % i, v)
		ret = cursor.fetchall()
		cursor.close()

		return ret

	def getByLevel(self, level):
		cursor = self.db.cursor()
		cursor.execute("SELECT mapel_user.id, mapel_user.user_id, mapel_user.mapel_id, users.nama_lengkap, mapel.nama FROM mapel_user JOIN mapel JOIN users WHERE users.id = mapel_user.user_id AND mapel.id = mapel_user.mapel_id AND users.level = ?;", (level,))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getGuru(self):
		return self.getByLevel(1)

	def getSiswa(self):
		return self.getByLevel(2)

	def create(self, mapel_id, user_id):
		try:
			cursor = self.db.cursor()
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (mapel_id, user_id) VALUES(?, ?);".format(self.table_name), (mapel_id, user_id))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

class AbsenTable(Table):
	def create(self, kelas_mapel_user_id, waktu_masuk):
		try:
			cursor = self.db.cursor()
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (kelas_mapel_user_id, waktu_hadir) VALUES(?, ?);".format(self.table_name), (kelas_mapel_user_id, waktu_masuk))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

	def getAbsen(self, level, user_id, kelas_id, mapel_id):
		cursor = self.db.cursor()
		cursor.execute('SELECT absen.id as id, absen.kelas_mapel_user_id as kmu_id, kelas_mapel_user.user_id as user_id, kelas_mapel_user.kelas_id as kelas_id, kelas_mapel_user.mapel_id as mapel_id, users.nama_lengkap as nama_lengkap, kelas.nama as nama_kelas, mapel.nama as nama_mapel, users.level as level, absen.waktu_hadir as waktu_hadir, strftime("%H", datetime(absen.waktu_hadir, "unixepoch", "localtime")) as jam, strftime("%d", datetime(absen.waktu_hadir, "unixepoch", "localtime")) as tanggal, strftime("%m", datetime(absen.waktu_hadir, "unixepoch", "localtime")) as bulan, strftime("%Y", datetime(absen.waktu_hadir, "unixepoch", "localtime")) as tahun FROM absen JOIN kelas_mapel_user JOIN users JOIN kelas JOIN mapel WHERE absen.kelas_mapel_user_id = kelas_mapel_user.id AND kelas_mapel_user.user_id = users.id AND kelas_mapel_user.kelas_id = kelas.id AND kelas_mapel_user.mapel_id = mapel.id AND users.level = ? AND kelas.id = ? AND mapel.id = ? AND users.id = ? GROUP BY absen.id;', (level, kelas_id, mapel_id, user_id))
		ret = cursor.fetchall()
		cursor.close()
		return ret

class Kelas_Mapel_UserTable(Table):
	def getMapelByKelas(self, kelas_id):
		cursor = self.db.cursor()
		cursor.execute("SELECT {tn}.mapel_id as id, mapel.nama as nama FROM {tn} JOIN users JOIN kelas JOIN mapel WHERE {tn}.kelas_id = ? AND users.id = {tn}.user_id AND kelas.id = {tn}.kelas_id AND mapel.id = {tn}.mapel_id GROUP BY {tn}.mapel_id;".format(tn=self.table_name), (kelas_id,))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getMapelByUserKelas(self, user_id, kelas_id):
		cursor = self.db.cursor()
		cursor.execute("SELECT {tn}.mapel_id as id, mapel.nama as nama FROM {tn} JOIN users JOIN kelas JOIN mapel WHERE {tn}.user_id = ? AND {tn}.kelas_id = ? AND users.id = {tn}.user_id AND kelas.id = {tn}.kelas_id AND mapel.id = {tn}.mapel_id GROUP BY {tn}.mapel_id;".format(tn=self.table_name), (user_id, kelas_id,))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getKelasByUser(self, user_id):
		cursor = self.db.cursor()
		cursor.execute("SELECT {tn}.kelas_id as id, kelas.nama as nama FROM {tn} JOIN users JOIN kelas JOIN mapel WHERE {tn}.user_id = ? AND users.id = {tn}.user_id AND kelas.id = {tn}.kelas_id AND mapel.id = {tn}.mapel_id GROUP BY {tn}.kelas_id;".format(tn=self.table_name), (user_id,))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getUserByKelasMapel(self, kelas_id, mapel_id):
		cursor = self.db.cursor()
		cursor.execute('SELECT {tn}.id as id, {tn}.user_id as user_id, users.nama_lengkap as nama_lengkap, users.level as level FROM {tn} JOIN users JOIN kelas JOIN mapel WHERE {tn}.kelas_id = ? AND {tn}.mapel_id = ? AND users.id = {tn}.user_id AND kelas.id = {tn}.kelas_id AND mapel.id = {tn}.mapel_id AND NOT EXISTS(SELECT absen.* FROM absen JOIN kelas_mapel_user as kmu JOIN users as u JOIN (SELECT *, strftime("%H:00 %d %m %Y", datetime(waktu_hadir, "unixepoch", "localtime")) as waktu FROM absen) as a where a.waktu_hadir = absen.waktu_hadir AND a.waktu == strftime("%H:00 %d %m %Y", datetime("now", "localtime")) AND absen.kelas_mapel_user_id = kmu.id AND kmu.user_id = u.id AND u.id = users.id GROUP BY absen.id) GROUP BY {tn}.user_id;'.format(tn=self.table_name), (kelas_id, mapel_id))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getUserByKelasMapelLevel(self, kelas_id, mapel_id, level):
		cursor = self.db.cursor()
		cursor.execute('SELECT {tn}.id as id, {tn}.user_id as user_id, users.nama_lengkap as nama_lengkap, users.level as level FROM {tn} JOIN users JOIN kelas JOIN mapel WHERE {tn}.kelas_id = ? AND {tn}.mapel_id = ? AND users.level = ? AND users.id = {tn}.user_id AND kelas.id = {tn}.kelas_id AND mapel.id = {tn}.mapel_id AND NOT EXISTS(SELECT absen.* FROM absen JOIN kelas_mapel_user as kmu JOIN users as u JOIN (SELECT *, strftime("%H:00 %d %m %Y", datetime(waktu_hadir, "unixepoch", "localtime")) as waktu FROM absen) as a where a.waktu_hadir = absen.waktu_hadir AND a.waktu == strftime("%H:00 %d %m %Y", datetime("now", "localtime")) AND absen.kelas_mapel_user_id = kmu.id AND kmu.user_id = u.id AND u.id = users.id GROUP BY absen.id) GROUP BY {tn}.user_id;'.format(tn=self.table_name), (kelas_id, mapel_id, level))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getUserByBukanKelasMapel(self, kelas_id, mapel_id):
		cursor = self.db.cursor()
		cursor.execute("SELECT users.* FROM users WHERE ( users.level = 1 OR users.level = 2 ) AND NOT EXISTS( SELECT * FROM kelas_mapel_user WHERE kelas_mapel_user.user_id = users.id AND kelas_mapel_user.kelas_id = ? AND kelas_mapel_user.mapel_id = ? ) GROUP BY users.id;", (kelas_id, mapel_id))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def getUserByBukanKelasMapelLevel(self, kelas_id, mapel_id, level):
		cursor = self.db.cursor()
		cursor.execute("SELECT users.* FROM users WHERE users.level = ? AND NOT EXISTS( SELECT * FROM kelas_mapel_user WHERE kelas_mapel_user.user_id = users.id AND kelas_mapel_user.kelas_id = ? AND kelas_mapel_user.mapel_id = ? ) GROUP BY users.id;", (level, kelas_id, mapel_id))
		ret = cursor.fetchall()
		cursor.close()
		return ret

	def create(self, user_id, kelas_id, mapel_id):
		try:
			cursor = self.db.cursor()
			cursor.execute("BEGIN TRANSACTION;")
			cursor.execute("INSERT INTO {} (user_id, kelas_id, mapel_id) VALUES(?, ?, ?);".format(self.table_name), (user_id, kelas_id, mapel_id))
			cursor.execute("END TRANSACTION;")
			self.db.sql.commit()
			cursor.close()
			return True
		except Exception as e:
			return False

	def getAllByLevel(self, level):
		cursor = self.db.cursor()
		cursor.execute("SELECT kelas_mapel_user.*, users.nama_lengkap as nama_lengkap, kelas.nama as nama_kelas, mapel.nama as nama_mapel FROM kelas_mapel_user JOIN users JOIN kelas JOIN mapel WHERE users.level = ? AND kelas_mapel_user.user_id = users.id AND kelas_mapel_user.kelas_id = kelas.id AND kelas_mapel_user.mapel_id = mapel.id ORDER BY users.id, kelas.id;", (level,))
		row = cursor.fetchall();
		cursor.close()

		return row

	def getAllByUserLevel(self, user_id, level):
		cursor = self.db.cursor()
		cursor.execute("SELECT kelas_mapel_user.*, users.nama_lengkap as nama_lengkap, kelas.nama as nama_kelas, mapel.nama as nama_mapel FROM kelas_mapel_user JOIN users JOIN kelas JOIN mapel WHERE users.id = ? AND users.level = ? AND kelas_mapel_user.user_id = users.id AND kelas_mapel_user.kelas_id = kelas.id AND kelas_mapel_user.mapel_id = mapel.id ORDER BY users.id, kelas.id;", (user_id, level,))
		row = cursor.fetchall();
		cursor.close()

		return row

	def getAllGuru(self, id=None):
		if id is None:
			return self.getAllByLevel(1)
		else:
			return self.getAllByUserLevel(id, 1)

	def getAllSiswa(self, id=None):
		if id is None:
			return self.getAllByLevel(2)
		else:
			return self.getAllByUserLevel(id, 2)
