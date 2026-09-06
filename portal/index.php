<?php
/**
 * The client side of the portal: sign in, then one checklist of what we still
 * need and what has already arrived.
 */

declare(strict_types=1);

require_once __DIR__ . '/lib/auth.php';
require_once __DIR__ . '/lib/files.php';
require_once __DIR__ . '/lib/layout.php';

$user  = current_user();
$error = null;

/* ---------------------------------------------------------------- sign in */
if (!$user && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    check_csrf();
    if (attempt_sign_in((string) ($_POST['email'] ?? ''), (string) ($_POST['password'] ?? ''))) {
        header('Location: index.php');
        exit;
    }
    $error = 'That email and password do not match an account.';
}

if (!$user) {
    portal_head('Client portal');
    ?>
    <section class="portal-signin">
      <div class="container portal-signin__inner">
        <div>
          <span class="overline">Client portal</span>
          <h1>Sign in to your portal.</h1>
          <p class="lede">A private, orderly way to get us what we need. One
            checklist, real time status, and nothing shared with anyone else.</p>
          <ul class="portal-points" role="list">
            <li><strong>A single checklist</strong> Everything outstanding in one place, so nothing gets chased twice.</li>
            <li><strong>Real time status</strong> Drop a file and the item flips to received the moment it lands with us.</li>
            <li><strong>Discreet by design</strong> Only AmeriFinancial and you ever see your documents. No third parties.</li>
          </ul>
        </div>
        <div class="portal-card">
          <?php if ($error): ?>
            <p class="portal-note portal-note--err"><?= e($error) ?></p>
          <?php endif; ?>
          <form method="post" novalidate>
            <?= csrf_field() ?>
            <div class="field">
              <label for="email">Email</label>
              <input type="email" id="email" name="email" autocomplete="username" required
                     value="<?= e((string) ($_POST['email'] ?? '')) ?>">
            </div>
            <div class="field">
              <label for="password">Password</label>
              <input type="password" id="password" name="password" autocomplete="current-password" required>
            </div>
            <button class="btn btn--primary" type="submit">Sign in</button>
          </form>
          <p class="portal-help">No sign in yet, or lost your password? Email
            <a href="mailto:hello@ameri-group.ca">hello@ameri-group.ca</a> and we
            will sort it out.</p>
        </div>
      </div>
    </section>
    <?php
    portal_foot();
    exit;
}

/* --------------------------------------------------------------- upload */
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && ($_POST['action'] ?? '') === 'upload') {
    check_csrf();
    $requestId = (int) ($_POST['request_id'] ?? 0);

    $stmt = db()->prepare('SELECT * FROM portal_requests WHERE id = ? AND client_id = ?');
    $stmt->execute([$requestId, $user['id']]);
    $request = $stmt->fetch();

    if (!$request) {
        flash('err', 'That item is not on your checklist.');
    } else {
        $result = store_upload($_FILES['document'] ?? []);
        if (!$result['ok']) {
            flash('err', $result['error']);
        } else {
            $ins = db()->prepare('INSERT INTO portal_files
                (request_id, client_id, stored_name, original_name, mime, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?)');
            $ins->execute([$requestId, $user['id'], $result['stored'],
                           $result['original'], $result['mime'], $result['size']]);
            db()->prepare('UPDATE portal_requests SET status = ? WHERE id = ?')
                ->execute(['received', $requestId]);
            flash('ok', 'Received. Thank you.');
        }
    }
    header('Location: index.php');
    exit;
}

/* ------------------------------------------------------------- checklist */
$stmt = db()->prepare('SELECT * FROM portal_requests WHERE client_id = ? ORDER BY id');
$stmt->execute([$user['id']]);
$requests = $stmt->fetchAll();

$stmt = db()->prepare('SELECT * FROM portal_files WHERE client_id = ? ORDER BY id DESC');
$stmt->execute([$user['id']]);
$filesByRequest = [];
foreach ($stmt->fetchAll() as $f) {
    $filesByRequest[$f['request_id']][] = $f;
}

$pending  = array_values(array_filter($requests, fn($r) => $r['status'] !== 'received'));
$received = array_values(array_filter($requests, fn($r) => $r['status'] === 'received'));
$firstName = trim(explode(' ', trim((string) $user['name']))[0] ?? '');

portal_head('Your document checklist', $user);
?>
<section class="section">
  <div class="container">
    <div class="page-title">
      <span class="overline">Client portal</span>
      <h1><?= $firstName !== '' ? 'Welcome back, ' . e($firstName) . '.' : 'Welcome back.' ?></h1>
      <p class="lede">Your document checklist. Everything we still need, and
        everything already with us.</p>
    </div>
    <?php show_flashes(); ?>

    <?php if (!$requests): ?>
      <div class="portal-empty">
        <h2>Nothing on your plate yet</h2>
        <p>Your portal is being set up. As soon as we need something from you it
          will appear here, and you will hear from us.</p>
      </div>
    <?php else: ?>

      <?php if ($pending): ?>
        <h2 class="portal-h">Needed from you (<?= count($pending) ?>)</h2>
        <ul class="portal-list" role="list">
          <?php foreach ($pending as $r): ?>
            <li class="portal-item">
              <div class="portal-item__head">
                <span class="portal-status portal-status--pending">Awaiting upload</span>
                <h3><?= e($r['title']) ?></h3>
                <?php if (!empty($r['description'])): ?>
                  <p><?= e($r['description']) ?></p>
                <?php endif; ?>
              </div>
              <form class="portal-drop" method="post" enctype="multipart/form-data">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="upload">
                <input type="hidden" name="request_id" value="<?= (int) $r['id'] ?>">
                <label class="portal-drop__label" for="file-<?= (int) $r['id'] ?>">
                  Drop file here <span>or click to browse</span>
                </label>
                <input class="portal-drop__input" id="file-<?= (int) $r['id'] ?>" type="file"
                       name="document" required
                       accept=".pdf,.csv,.xls,.xlsx,.doc,.docx,.jpg,.jpeg,.png,.heic">
                <button class="btn btn--navy" type="submit">Upload</button>
              </form>
            </li>
          <?php endforeach; ?>
        </ul>
      <?php else: ?>
        <div class="portal-empty">
          <h2>All caught up</h2>
          <p>Your finance team has everything they need for now.</p>
        </div>
      <?php endif; ?>

      <?php if ($received): ?>
        <h2 class="portal-h">Received (<?= count($received) ?>)</h2>
        <ul class="portal-list" role="list">
          <?php foreach ($received as $r): ?>
            <li class="portal-item portal-item--done">
              <div class="portal-item__head">
                <span class="portal-status portal-status--done">Document received</span>
                <h3><?= e($r['title']) ?></h3>
                <?php foreach ($filesByRequest[$r['id']] ?? [] as $i => $f): ?>
                  <p class="portal-file">
                    <a href="download.php?id=<?= (int) $f['id'] ?>"><?= e($f['original_name']) ?></a>
                    <span><?= e(human_size((int) $f['size_bytes'])) ?><?= $i > 0 ? ' (earlier version)' : '' ?></span>
                  </p>
                <?php endforeach; ?>
              </div>
              <form class="portal-drop portal-drop--replace" method="post" enctype="multipart/form-data">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="upload">
                <input type="hidden" name="request_id" value="<?= (int) $r['id'] ?>">
                <label class="portal-drop__label" for="replace-<?= (int) $r['id'] ?>">
                  Sent the wrong file? <span>Replace it</span>
                </label>
                <input class="portal-drop__input" id="replace-<?= (int) $r['id'] ?>" type="file"
                       name="document" required
                       accept=".pdf,.csv,.xls,.xlsx,.doc,.docx,.jpg,.jpeg,.png,.heic">
                <button class="btn btn--outline" type="submit">Replace</button>
              </form>
            </li>
          <?php endforeach; ?>
        </ul>
      <?php endif; ?>

    <?php endif; ?>
  </div>
</section>
<?php
portal_foot();
