CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `password` password,
  `nomor_induk` varchar(255),
  `nama_lengkap` varchar(255),
  `tanggal_lahir` int,
  `nomor_telpon` varchar(255),
  `nomor_telpon_ortu` varchar(255),
  `alamat` varchar(255),
  `level` enum
);

CREATE TABLE `kelas` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nama` varchar(255)
);

CREATE TABLE `mapel` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nama` varchar(255)
);

CREATE TABLE `kelas_user` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `kelas_id` int,
  `create_time` int
);

CREATE TABLE `mapel_user` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `mapel_id` int,
  `create_time` int
);

CREATE TABLE `absen` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `kelas_user_id` int,
  `mapel_user_id` int,
  `waktu_hadir` int,
  `waktu_jadwal` int
);

ALTER TABLE `kelas_user` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `kelas_user` ADD FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`);

ALTER TABLE `mapel_user` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `mapel_user` ADD FOREIGN KEY (`mapel_id`) REFERENCES `mapel` (`id`);

ALTER TABLE `absen` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `absen` ADD FOREIGN KEY (`kelas_user_id`) REFERENCES `kelas_user` (`id`);

ALTER TABLE `absen` ADD FOREIGN KEY (`mapel_user_id`) REFERENCES `mapel_user` (`id`);
