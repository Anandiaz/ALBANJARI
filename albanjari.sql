-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 23 Nov 2024 pada 12.37
-- Versi server: 10.6.19-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `albanjari`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `albanjari_category`
--

CREATE TABLE `albanjari_category` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data untuk tabel `albanjari_category`
--

INSERT INTO `albanjari_category` (`category_id`, `category_name`) VALUES
(1, 'Country choose girl red. We investment black go meet. Thank suggest front moment else.'),
(2, 'Pay sign condition reason. Response true theory movie. Process involve quite matter.'),
(3, 'Pull paper according always star. Affect guy over nearly sense. Structure although difference.'),
(4, 'Hair sign believe meet its radio information. Help story our nothing strong pull buy.'),
(5, 'Wrong there week well time both too. Society run effort blue candidate my carry.'),
(6, 'Wife lose lead push offer goal career. Business back perform far.'),
(7, 'Make let decision stop value need. Film face total leader century Mrs sure.'),
(8, 'Reason learn skin cell defense. Civil fast gun that account stuff apply.'),
(9, 'Gas subject set difficult song increase television claim. Seem star then old tough nor.'),
(10, 'Effect item require beyond. Authority by once reach around.');

-- --------------------------------------------------------

--
-- Struktur dari tabel `albanjari_payment`
--

CREATE TABLE `albanjari_payment` (
  `payment_id` int(11) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `payment_date` datetime(6) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `transaction_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `albanjari_product`
--

CREATE TABLE `albanjari_product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `albanjari_topuppackage`
--

CREATE TABLE `albanjari_topuppackage` (
  `package_id` int(11) NOT NULL,
  `package_name` varchar(100) NOT NULL,
  `amount` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `product_id` int(11) NOT NULL,
  `agent_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `albanjari_transaction`
--

CREATE TABLE `albanjari_transaction` (
  `transaction_id` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `transaction_date` datetime(6) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `package_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `transaction_proof` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `albanjari_userprofile`
--

CREATE TABLE `albanjari_userprofile` (
  `id` bigint(20) NOT NULL,
  `role` varchar(10) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data untuk tabel `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add category', 7, 'add_category'),
(26, 'Can change category', 7, 'change_category'),
(27, 'Can delete category', 7, 'delete_category'),
(28, 'Can view category', 7, 'view_category'),
(29, 'Can add product', 8, 'add_product'),
(30, 'Can change product', 8, 'change_product'),
(31, 'Can delete product', 8, 'delete_product'),
(32, 'Can view product', 8, 'view_product'),
(33, 'Can add top up package', 9, 'add_topuppackage'),
(34, 'Can change top up package', 9, 'change_topuppackage'),
(35, 'Can delete top up package', 9, 'delete_topuppackage'),
(36, 'Can view top up package', 9, 'view_topuppackage'),
(37, 'Can add transaction', 10, 'add_transaction'),
(38, 'Can change transaction', 10, 'change_transaction'),
(39, 'Can delete transaction', 10, 'delete_transaction'),
(40, 'Can view transaction', 10, 'view_transaction'),
(41, 'Can add payment', 11, 'add_payment'),
(42, 'Can change payment', 11, 'change_payment'),
(43, 'Can delete payment', 11, 'delete_payment'),
(44, 'Can view payment', 11, 'view_payment'),
(45, 'Can add user profile', 12, 'add_userprofile'),
(46, 'Can change user profile', 12, 'change_userprofile'),
(47, 'Can delete user profile', 12, 'delete_userprofile'),
(48, 'Can view user profile', 12, 'view_userprofile');

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data untuk tabel `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$VimYAaWbH9fdekP3vJTyQb$3dtBN88IsiVdR4/lhShSDrO7XuPIxvc0SRphGwyPs7g=', '2024-11-22 22:54:25.779761', 1, 'albanjari', '', '', 'albanjari@example.com', 1, 1, '2024-11-22 22:53:30.092418');

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data untuk tabel `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(7, 'albanjari', 'category'),
(11, 'albanjari', 'payment'),
(8, 'albanjari', 'product'),
(9, 'albanjari', 'topuppackage'),
(10, 'albanjari', 'transaction'),
(12, 'albanjari', 'userprofile'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data untuk tabel `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-11-22 22:42:45.137140'),
(2, 'auth', '0001_initial', '2024-11-22 22:42:45.355279'),
(3, 'admin', '0001_initial', '2024-11-22 22:42:45.422105'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-11-22 22:42:45.422105'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-22 22:42:45.443665'),
(6, 'albanjari', '0001_initial', '2024-11-22 22:42:45.592011'),
(7, 'contenttypes', '0002_remove_content_type_name', '2024-11-22 22:42:45.671850'),
(8, 'auth', '0002_alter_permission_name_max_length', '2024-11-22 22:42:45.738639'),
(9, 'auth', '0003_alter_user_email_max_length', '2024-11-22 22:42:45.773988'),
(10, 'auth', '0004_alter_user_username_opts', '2024-11-22 22:42:45.794182'),
(11, 'auth', '0005_alter_user_last_login_null', '2024-11-22 22:42:45.827532'),
(12, 'auth', '0006_require_contenttypes_0002', '2024-11-22 22:42:45.827532'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2024-11-22 22:42:45.847450'),
(14, 'auth', '0008_alter_user_username_max_length', '2024-11-22 22:42:45.872194'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2024-11-22 22:42:45.885733'),
(16, 'auth', '0010_alter_group_name_max_length', '2024-11-22 22:42:45.928216'),
(17, 'auth', '0011_update_proxy_permissions', '2024-11-22 22:42:45.937790'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2024-11-22 22:42:45.970377'),
(19, 'sessions', '0001_initial', '2024-11-22 22:42:45.988785'),
(20, 'albanjari', '0002_topuppackage_agent_price_and_more', '2024-11-22 22:44:06.809107');

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data untuk tabel `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9s79c6vcswnar7zrfivlit9lw9hsv65v', '.eJxVjMEOwiAQRP-FsyELgoBH7_0GsrCLVA1NSnsy_rtt0oNe5jDvzbxFxHWpce08x5HEVShx-u0S5ie3HdAD232SeWrLPCa5K_KgXQ4T8et2uH8HFXvd1sZlVy4eXEGyTjtnFasSEm0RgjcWiYs56wI-q-BtAJMAwSLrlBWD-HwB2Lg3sQ:1tEcXh:hXohwT_uTlgsj5cLZ97MkQqnRoRDuscPTQ40g91-lv4', '2024-12-06 22:54:25.779761');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `albanjari_category`
--
ALTER TABLE `albanjari_category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indeks untuk tabel `albanjari_payment`
--
ALTER TABLE `albanjari_payment`
  ADD PRIMARY KEY (`payment_id`),
  ADD UNIQUE KEY `transaction_id` (`transaction_id`);

--
-- Indeks untuk tabel `albanjari_product`
--
ALTER TABLE `albanjari_product`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `albanjari_product_category_id_048adf11_fk_albanjari` (`category_id`);

--
-- Indeks untuk tabel `albanjari_topuppackage`
--
ALTER TABLE `albanjari_topuppackage`
  ADD PRIMARY KEY (`package_id`),
  ADD KEY `albanjari_topuppacka_product_id_251db150_fk_albanjari` (`product_id`);

--
-- Indeks untuk tabel `albanjari_transaction`
--
ALTER TABLE `albanjari_transaction`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `albanjari_transactio_package_id_7d3bf357_fk_albanjari` (`package_id`),
  ADD KEY `albanjari_transaction_user_id_eba9e1eb_fk_auth_user_id` (`user_id`);

--
-- Indeks untuk tabel `albanjari_userprofile`
--
ALTER TABLE `albanjari_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indeks untuk tabel `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indeks untuk tabel `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indeks untuk tabel `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indeks untuk tabel `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indeks untuk tabel `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indeks untuk tabel `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indeks untuk tabel `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `albanjari_category`
--
ALTER TABLE `albanjari_category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `albanjari_payment`
--
ALTER TABLE `albanjari_payment`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `albanjari_product`
--
ALTER TABLE `albanjari_product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `albanjari_topuppackage`
--
ALTER TABLE `albanjari_topuppackage`
  MODIFY `package_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `albanjari_transaction`
--
ALTER TABLE `albanjari_transaction`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `albanjari_userprofile`
--
ALTER TABLE `albanjari_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT untuk tabel `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `albanjari_payment`
--
ALTER TABLE `albanjari_payment`
  ADD CONSTRAINT `albanjari_payment_transaction_id_95817727_fk_albanjari` FOREIGN KEY (`transaction_id`) REFERENCES `albanjari_transaction` (`transaction_id`);

--
-- Ketidakleluasaan untuk tabel `albanjari_product`
--
ALTER TABLE `albanjari_product`
  ADD CONSTRAINT `albanjari_product_category_id_048adf11_fk_albanjari` FOREIGN KEY (`category_id`) REFERENCES `albanjari_category` (`category_id`);

--
-- Ketidakleluasaan untuk tabel `albanjari_topuppackage`
--
ALTER TABLE `albanjari_topuppackage`
  ADD CONSTRAINT `albanjari_topuppacka_product_id_251db150_fk_albanjari` FOREIGN KEY (`product_id`) REFERENCES `albanjari_product` (`product_id`);

--
-- Ketidakleluasaan untuk tabel `albanjari_transaction`
--
ALTER TABLE `albanjari_transaction`
  ADD CONSTRAINT `albanjari_transactio_package_id_7d3bf357_fk_albanjari` FOREIGN KEY (`package_id`) REFERENCES `albanjari_topuppackage` (`package_id`),
  ADD CONSTRAINT `albanjari_transaction_user_id_eba9e1eb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ketidakleluasaan untuk tabel `albanjari_userprofile`
--
ALTER TABLE `albanjari_userprofile`
  ADD CONSTRAINT `albanjari_userprofile_user_id_db46815a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ketidakleluasaan untuk tabel `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
