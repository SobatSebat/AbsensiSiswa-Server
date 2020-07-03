BEGIN TRANSACTION;
DROP TABLE IF EXISTS "absen";
CREATE TABLE IF NOT EXISTS "absen" (
	"id"	integer PRIMARY KEY AUTOINCREMENT,
	"kelas_mapel_user_id"	INTEGER,
	"waktu_hadir"	integer
);
DROP TABLE IF EXISTS "kelas_mapel_user";
CREATE TABLE IF NOT EXISTS "kelas_mapel_user" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"user_id"	INTEGER,
	"kelas_id"	INTEGER,
	"mapel_id"	INTEGER,
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("kelas_id") REFERENCES "kelas"("id"),
	FOREIGN KEY("mapel_id") REFERENCES "mapel"("id")
);
DROP TABLE IF EXISTS "mapel";
CREATE TABLE IF NOT EXISTS "mapel" (
	"id"	integer PRIMARY KEY AUTOINCREMENT,
	"nama"	varchar(255)
);
DROP TABLE IF EXISTS "kelas";
CREATE TABLE IF NOT EXISTS "kelas" (
	"id"	integer PRIMARY KEY AUTOINCREMENT,
	"nama"	varchar(255)
);
DROP TABLE IF EXISTS "users";
CREATE TABLE IF NOT EXISTS "users" (
	"id"	integer PRIMARY KEY AUTOINCREMENT,
	"username"	varchar(255),
	"password"	varchar(255),
	"nomor_induk"	varchar(255),
	"nama_lengkap"	varchar(255),
	"tanggal_lahir"	integer,
	"nomor_telpon"	varchar(255),
	"nomor_telpon_ortu"	varchar(255),
	"alamat"	varchar(255),
	"level"	enum
);
INSERT INTO "users" ("id","username","password","nomor_induk","nama_lengkap","tanggal_lahir","nomor_telpon","nomor_telpon_ortu","alamat","level") VALUES (1,'admin','5f4dcc3b5aa765d61d8327deb882cf99',NULL,NULL,NULL,NULL,NULL,NULL,0);
COMMIT;
