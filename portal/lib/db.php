<?php
/**
 * Database connection and schema. Written against PDO so the same code runs on
 * MySQL (GoDaddy) and SQLite (local testing), and creates its own tables on
 * first run so there is no migration step to remember.
 */

declare(strict_types=1);

function config(): array
{
    static $config = null;
    if ($config === null) {
        $path = __DIR__ . '/config.php';
        if (!is_file($path)) {
            http_response_code(500);
            exit('The portal is not configured yet. Copy portal/lib/config.example.php '
               . 'to portal/lib/config.php and fill in the database details.');
        }
        $config = require $path;
    }
    return $config;
}

function db(): PDO
{
    static $pdo = null;
    if ($pdo !== null) {
        return $pdo;
    }
    $c = config()['db'];
    try {
        $pdo = new PDO($c['dsn'], $c['user'] ?? null, $c['pass'] ?? null, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);
    } catch (PDOException $e) {
        error_log('Portal database connection failed: ' . $e->getMessage());
        http_response_code(500);
        exit('The portal cannot reach its database right now.');
    }
    migrate($pdo);
    return $pdo;
}

function is_sqlite(PDO $pdo): bool
{
    return $pdo->getAttribute(PDO::ATTR_DRIVER_NAME) === 'sqlite';
}

function migrate(PDO $pdo): void
{
    $sqlite = is_sqlite($pdo);
    $id     = $sqlite ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT AUTO_INCREMENT PRIMARY KEY';
    $now    = $sqlite ? "TEXT NOT NULL DEFAULT (datetime('now'))" : 'DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP';
    $engine = $sqlite ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4';

    $pdo->exec("CREATE TABLE IF NOT EXISTS portal_users (
        id            $id,
        email         VARCHAR(190) NOT NULL UNIQUE,
        name          VARCHAR(160) NOT NULL DEFAULT '',
        password_hash VARCHAR(255) NOT NULL,
        role          VARCHAR(10)  NOT NULL DEFAULT 'client',
        business      VARCHAR(190) NOT NULL DEFAULT '',
        notes         TEXT         NULL,
        created_at    $now
    )$engine");

    $pdo->exec("CREATE TABLE IF NOT EXISTS portal_requests (
        id          $id,
        client_id   INTEGER NOT NULL,
        title       VARCHAR(190) NOT NULL,
        description TEXT NULL,
        status      VARCHAR(12) NOT NULL DEFAULT 'pending',
        created_at  $now
    )$engine");

    $pdo->exec("CREATE TABLE IF NOT EXISTS portal_files (
        id            $id,
        request_id    INTEGER NOT NULL,
        client_id     INTEGER NOT NULL,
        stored_name   VARCHAR(120) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        mime          VARCHAR(120) NOT NULL DEFAULT '',
        size_bytes    INTEGER NOT NULL DEFAULT 0,
        uploaded_at   $now
    )$engine");

    // The first administrator, so there is a way in on a fresh install.
    $count = (int) $pdo->query('SELECT COUNT(*) FROM portal_users')->fetchColumn();
    if ($count === 0) {
        $a = config()['bootstrap_admin'];
        $stmt = $pdo->prepare('INSERT INTO portal_users (email, name, password_hash, role)
                               VALUES (?, ?, ?, ?)');
        $stmt->execute([
            strtolower(trim($a['email'])),
            $a['name'],
            password_hash($a['pass'], PASSWORD_DEFAULT),
            'admin',
        ]);
    }
}
