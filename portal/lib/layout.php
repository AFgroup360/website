<?php
declare(strict_types=1);
require_once __DIR__ . '/auth.php';

function portal_head(string $title, ?array $user = null): void
{
    ?><!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?> | AmeriFinancial</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#08162f">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/img/icon-32.png">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/tokens.css">
<link rel="stylesheet" href="../css/base.css">
<link rel="stylesheet" href="../css/main.css">
<link rel="stylesheet" href="../css/portal.css">
</head>
<body class="portal-body">
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="../index.html" aria-label="AmeriFinancial, back to the website">
      <img class="brand__lockup" src="../assets/img/logo-lockup.png" alt="AmeriFinancial"
           width="1182" height="150" decoding="async">
      <img class="brand__markonly" src="../assets/img/logo-mark.png" alt="AmeriFinancial"
           width="271" height="181" loading="lazy" decoding="async">
    </a>
    <div class="portal-bar">
      <?php if ($user): ?>
        <span class="portal-bar__who">Signed in as <strong><?= e($user['name'] ?: $user['email']) ?></strong></span>
        <?php if ($user['role'] === 'admin'): ?>
          <a class="portal-bar__link" href="admin.php">Dashboard</a>
          <a class="portal-bar__link" href="index.php">Checklist view</a>
        <?php endif; ?>
        <a class="portal-bar__link" href="logout.php">Sign out</a>
      <?php endif; ?>
    </div>
  </div>
</header>
<main id="main" class="portal-main">
<?php
}

function portal_foot(): void
{
    ?>
</main>
<script src="portal.js" defer></script>
<footer class="portal-foot">
  <div class="container">
    <span>Only AmeriFinancial and you can see anything uploaded here.</span>
    <span><a href="../index.html">Back to the website</a></span>
  </div>
</footer>
</body>
</html>
<?php
}

function flash(string $kind, string $message): void
{
    boot_session();
    $_SESSION['flash'][] = ['kind' => $kind, 'message' => $message];
}

function show_flashes(): void
{
    boot_session();
    foreach ($_SESSION['flash'] ?? [] as $f) {
        echo '<p class="portal-note portal-note--' . e($f['kind']) . '">' . e($f['message']) . '</p>';
    }
    $_SESSION['flash'] = [];
}
