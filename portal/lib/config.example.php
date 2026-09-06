<?php
/**
 * Copy this file to config.php and fill in the values, then upload it.
 * config.php is deliberately not in the repository, because it holds the
 * database password.
 *
 * On GoDaddy the database is created in cPanel under "MySQL Databases". The
 * host is almost always localhost.
 */
return [
    'db' => [
        'dsn'  => 'mysql:host=localhost;dbname=YOUR_DATABASE;charset=utf8mb4',
        'user' => 'YOUR_DB_USER',
        'pass' => 'YOUR_DB_PASSWORD',
    ],

    // Where uploaded documents are written. Keep this outside public_html if
    // your hosting allows it. If not, the default below is protected by its
    // own .htaccess and every file is stored under a random name.
    'storage' => __DIR__ . '/../storage',

    // The first administrator. Created automatically on first run, then this
    // block is ignored. Change the password immediately after signing in.
    'bootstrap_admin' => [
        'email' => 'hello@ameri-group.ca',
        'name'  => 'AmeriFinancial',
        'pass'  => 'change-this-on-first-sign-in',
    ],

    'max_upload_mb' => 25,
];
