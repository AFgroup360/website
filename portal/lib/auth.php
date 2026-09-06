<?php
/**
 * Sessions, sign in, and the cross site request check. Replaces the hosted
 * auth service the previous build used, so the portal runs on the hosting
 * the site is already paying for.
 */

declare(strict_types=1);

require_once __DIR__ . '/db.php';

function boot_session(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    $https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
          || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    session_set_cookie_params([
        'lifetime' => 0,
        'path'     => '/',
        'httponly' => true,
        'secure'   => $https,
        'samesite' => 'Lax',
    ]);
    session_name('afportal');
    session_start();
}

function current_user(): ?array
{
    boot_session();
    if (empty($_SESSION['uid'])) {
        return null;
    }
    static $user = null;
    if ($user === null) {
        $stmt = db()->prepare('SELECT * FROM portal_users WHERE id = ?');
        $stmt->execute([$_SESSION['uid']]);
        $user = $stmt->fetch() ?: false;
        if ($user === false) {           // Account removed while signed in.
            sign_out();
            return null;
        }
    }
    return $user ?: null;
}

function require_user(): array
{
    $u = current_user();
    if (!$u) {
        header('Location: index.php');
        exit;
    }
    return $u;
}

function require_admin(): array
{
    $u = require_user();
    if ($u['role'] !== 'admin') {
        http_response_code(403);
        exit('Not your area.');
    }
    return $u;
}

function attempt_sign_in(string $email, string $password): bool
{
    boot_session();
    $stmt = db()->prepare('SELECT * FROM portal_users WHERE email = ?');
    $stmt->execute([strtolower(trim($email))]);
    $user = $stmt->fetch();

    // Always run a hash comparison so a wrong email and a wrong password take
    // the same time to fail.
    $hash = $user['password_hash'] ?? '$2y$12$invalidinvalidinvalidinvalidinvalidinvalidinvalidinva';
    if (!password_verify($password, $hash) || !$user) {
        return false;
    }
    session_regenerate_id(true);
    $_SESSION['uid'] = (int) $user['id'];
    return true;
}

function sign_out(): void
{
    boot_session();
    $_SESSION = [];
    if (ini_get('session.use_cookies')) {
        $p = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000, $p['path'], $p['domain'], $p['secure'], $p['httponly']);
    }
    session_destroy();
}

function csrf_token(): string
{
    boot_session();
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="_csrf" value="' . htmlspecialchars(csrf_token(), ENT_QUOTES) . '">';
}

function check_csrf(): void
{
    boot_session();
    $sent = $_POST['_csrf'] ?? '';
    if (!is_string($sent) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $sent)) {
        http_response_code(400);
        exit('That form expired. Go back, reload the page and try again.');
    }
}

function e(?string $v): string
{
    return htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');
}
