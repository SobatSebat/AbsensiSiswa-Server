import sqlite3 as SQL

class DB :
	def __init__(self, fn="absensi.db"):
		self.sql = SQL.connect(fn, check_same_thread=False)

	def cursor(self):
		return self.sql.cursor()

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

		ret = ret[0][0]

		return ret

	def getByLevel(self, level):
		cursor = self.db.cursor()
		if(level == 1):
			cursor.execute("SELECT id, nomor_induk, nama_lengkap, username, tanggal_lahir, nomor_telpon, alamat FROM {} WHERE level=?;".format(self.table_name), (level,))
		else:
			cursor.execute("SELECT id, nomor_induk, nama_lengkap, username, tanggal_lahir, nomor_telpon, nomor_telpon_ortu, alamat FROM {} WHERE level=?;".format(self.table_name), (level,))
		ret = cursor.fetchall()
		cursor.close()

		return ret

	def getGuru(self):
		return self.getByLevel(1)

	def getSiswa(self):
		return self.getByLevel(2)


class KelasTable(Table):
	pass

class MapelTable(Table):
	pass

class Kelas_UserTable(Table):
	def getAll(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT kelas_user.id, kelas_user.user_id, kelas_user.kelas_id, users.nama_lengkap, kelas.nama FROM kelas_user JOIN kelas JOIN users WHERE users.id = kelas_user.user_id AND kelas.id = kelas_user.kelas_id;")
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

class Mapel_UserTable(Table):
	def getAll(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT mapel_user.id, mapel_user.user_id, mapel_user.mapel_id, users.nama_lengkap, mapel.nama FROM mapel_user JOIN mapel JOIN users WHERE users.id = mapel_user.user_id AND mapel.id = mapel_user.mapel_id;")
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
