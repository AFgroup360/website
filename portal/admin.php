<?php
/**
 * The AmeriFinancial side. Add clients, request documents from them, watch
 * items flip to received, and download what arrives.
 */

declare(strict_types=1);

require_once __DIR__ . '/lib/auth.php';
require_once __DIR__ . '/lib/files.php';
require_once __DIR__ . '/lib/layout.php';

$user = require_admin();

function random_password(): string
{
    $words = ['harbour','ledger','granite','compass','meridian','anchor','quarry','beacon'];
    return $words[random_int(0, count($words) - 1)] . '-'
         . $words[random_int(0, count($words) - 1)] . '-'
         . random_int(1000, 9999);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    check_csrf();
    $action = (string) ($_POST['action'] ?? '');

    if ($action === 'add_client') {
        $email = strtolower(trim((string) ($_POST['email'] ?? '')));
        $business = trim((string) ($_POST['business'] ?? ''));
        if (!filter_var($email, FILTER_VALIDATE_EMAIL) || $business === '') {
            flash('err', 'A business name and a valid login email are both needed.');
        } else {
            $exists = db()->prepare('SELECT id FROM portal_users WHERE email = ?');
            $exists->execute([$email]);
            if ($exists->fetch()) {
                flash('err', 'There is already an account with that email.');
            } else {
                $pass = random_password();
                db()->prepare('INSERT INTO portal_users (email, name, password_hash, role, business, notes)
                               VALUES (?, ?, ?, ?, ?, ?)')
                    ->execute([$email, trim((string) ($_POST['contact'] ?? '')),
                               password_hash($pass, PASSWORD_DEFAULT), 'client',
                               $business, trim((string) ($_POST['notes'] ?? ''))]);
                flash('ok', 'Client added. Their first password is ' . $pass
                          . ' — send it to them and ask them to tell you once they are in.');
            }
        }
    }

    if ($action === 'add_admin') {
        $email = strtolower(trim((string) ($_POST['email'] ?? '')));
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            flash('err', 'That does not look like an email address.');
        } else {
            $exists = db()->prepare('SELECT id FROM portal_users WHERE email = ?');
            $exists->execute([$email]);
            if ($exists->fetch()) {
                flash('err', 'There is already an account with that email.');
            } else {
                $pass = random_password();
                db()->prepare('INSERT INTO portal_users (email, name, password_hash, role)
                               VALUES (?, ?, ?, ?)')
                    ->execute([$email, trim((string) ($_POST['name'] ?? '')),
                               password_hash($pass, PASSWORD_DEFAULT), 'admin']);
                flash('ok', 'Admin added, with full access to every client checklist. '
                          . 'Their first password is ' . $pass);
            }
        }
    }

    if ($action === 'request_doc') {
        $clientId = (int) ($_POST['client_id'] ?? 0);
        $title = trim((string) ($_POST['title'] ?? ''));
        $check = db()->prepare("SELECT id FROM portal_users WHERE id = ? AND role = 'client'");
        $check->execute([$clientId]);
        if (!$check->fetch() || $title === '') {
            flash('err', 'Pick a client and give the document a title.');
        } else {
            db()->prepare('INSERT INTO portal_requests (client_id, title, description) VALUES (?, ?, ?)')
                ->execute([$clientId, $title, trim((string) ($_POST['description'] ?? ''))]);
            flash('ok', 'Added to their checklist.');
        }
    }

    if ($action === 'set_status') {
        $rid = (int) ($_POST['request_id'] ?? 0);
        $to  = ($_POST['status'] ?? '') === 'received' ? 'received' : 'pending';
        db()->prepare('UPDATE portal_requests SET status = ? WHERE id = ?')->execute([$to, $rid]);
        flash('ok', $to === 'received' ? 'Marked received.' : 'Marked pending.');
    }

    if ($action === 'delete_request') {
        $rid = (int) ($_POST['request_id'] ?? 0);
        $files = db()->prepare('SELECT stored_name FROM portal_files WHERE request_id = ?');
        $files->execute([$rid]);
        foreach ($files->fetchAll() as $f) {
            @unlink(storage_dir() . '/' . basename((string) $f['stored_name']));
        }
        db()->prepare('DELETE FROM portal_files WHERE request_id = ?')->execute([$rid]);
        db()->prepare('DELETE FROM portal_requests WHERE id = ?')->execute([$rid]);
        flash('ok', 'Request removed, along with anything uploaded against it.');
    }

    header('Location: admin.php');
    exit;
}

$clients = db()->query("SELECT * FROM portal_users WHERE role = 'client' ORDER BY business")->fetchAll();
$admins  = db()->query("SELECT * FROM portal_users WHERE role = 'admin' ORDER BY email")->fetchAll();

$requests = [];
foreach (db()->query('SELECT * FROM portal_requests ORDER BY id')->fetchAll() as $r) {
    $requests[$r['client_id']][] = $r;
}
$files = [];
foreach (db()->query('SELECT * FROM portal_files ORDER BY id DESC')->fetchAll() as $f) {
    $files[$f['request_id']][] = $f;
}
$recent = db()->query('SELECT f.*, u.business FROM portal_files f
                       JOIN portal_users u ON u.id = f.client_id
                       ORDER BY f.id DESC')->fetchAll();
$recent = array_slice($recent, 0, 8);

portal_head('Client portal dashboard', $user);
?>
<section class="section">
  <div class="container">
    <div class="page-title">
      <span class="overline">Client portal</span>
      <h1>Dashboard.</h1>
    </div>
    <?php show_flashes(); ?>

    <h2 class="portal-h">Clients (<?= count($clients) ?>)</h2>
    <?php if (!$clients): ?>
      <div class="portal-empty">
        <h2>No clients yet</h2>
        <p>Add your first one to get started.</p>
      </div>
    <?php endif; ?>

    <?php foreach ($clients as $c): ?>
      <?php
        $rs = $requests[$c['id']] ?? [];
        $done = count(array_filter($rs, fn($r) => $r['status'] === 'received'));
      ?>
      <article class="portal-client">
        <div class="portal-client__head">
          <div>
            <h3><?= e($c['business']) ?></h3>
            <p class="portal-client__meta">
              <?= e($c['name'] ?: 'No contact name') ?> &middot; <?= e($c['email']) ?>
              <?php if (!empty($c['notes'])): ?><br><?= e($c['notes']) ?><?php endif; ?>
            </p>
          </div>
          <span class="portal-status <?= $rs && $done === count($rs) ? 'portal-status--done' : 'portal-status--pending' ?>">
            <?= $rs ? $done . ' of ' . count($rs) . ' received' : 'Nothing requested yet' ?>
          </span>
        </div>

        <?php if ($rs): ?>
          <table class="ledger portal-table">
            <thead><tr>
              <th scope="col">Document</th><th scope="col">Status</th><th scope="col">File</th><th scope="col"></th>
            </tr></thead>
            <tbody>
            <?php foreach ($rs as $r): ?>
              <tr>
                <th scope="row"><?= e($r['title']) ?>
                  <?php if (!empty($r['description'])): ?>
                    <span class="portal-table__note"><?= e($r['description']) ?></span>
                  <?php endif; ?>
                </th>
                <td><?= $r['status'] === 'received' ? 'Received' : 'Awaiting upload' ?></td>
                <td>
                  <?php foreach ($files[$r['id']] ?? [] as $i => $f): ?>
                    <a href="download.php?id=<?= (int) $f['id'] ?>"><?= e($f['original_name']) ?></a>
                    <span class="portal-table__note"><?= e(human_size((int) $f['size_bytes'])) ?><?= $i > 0 ? ', earlier version' : '' ?></span><br>
                  <?php endforeach; ?>
                  <?php if (empty($files[$r['id']])): ?><span class="portal-table__note">None yet</span><?php endif; ?>
                </td>
                <td class="portal-table__actions">
                  <form method="post">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="set_status">
                    <input type="hidden" name="request_id" value="<?= (int) $r['id'] ?>">
                    <input type="hidden" name="status" value="<?= $r['status'] === 'received' ? 'pending' : 'received' ?>">
                    <button class="portal-mini" type="submit"><?= $r['status'] === 'received' ? 'Mark pending' : 'Mark received' ?></button>
                  </form>
                  <form method="post" onsubmit="return confirm('Remove this document request?');">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="delete_request">
                    <input type="hidden" name="request_id" value="<?= (int) $r['id'] ?>">
                    <button class="portal-mini portal-mini--warn" type="submit">Remove</button>
                  </form>
                </td>
              </tr>
            <?php endforeach; ?>
            </tbody>
          </table>
        <?php else: ?>
          <p class="portal-table__note">No documents requested yet.</p>
        <?php endif; ?>

        <form class="portal-inline" method="post">
          <?= csrf_field() ?>
          <input type="hidden" name="action" value="request_doc">
          <input type="hidden" name="client_id" value="<?= (int) $c['id'] ?>">
          <div class="field">
            <label for="t<?= (int) $c['id'] ?>">Request a document</label>
            <input type="text" id="t<?= (int) $c['id'] ?>" name="title" required
                   placeholder="March bank statement">
          </div>
          <div class="field">
            <label for="d<?= (int) $c['id'] ?>">Notes (optional)</label>
            <input type="text" id="d<?= (int) $c['id'] ?>" name="description"
                   placeholder="All accounts, PDF preferred.">
          </div>
          <button class="btn btn--navy" type="submit">Add to checklist</button>
        </form>
      </article>
    <?php endforeach; ?>

    <div class="portal-cols">
      <section class="portal-card">
        <h2>Add a client</h2>
        <p class="portal-table__note">The email links this business to their portal sign in.</p>
        <form method="post">
          <?= csrf_field() ?>
          <input type="hidden" name="action" value="add_client">
          <div class="field"><label for="b">Business name</label><input type="text" id="b" name="business" required></div>
          <div class="field"><label for="cn">Contact name</label><input type="text" id="cn" name="contact"></div>
          <div class="field"><label for="ce">Login email</label><input type="email" id="ce" name="email" required></div>
          <div class="field"><label for="cnotes">Notes (optional)</label><input type="text" id="cnotes" name="notes"></div>
          <button class="btn btn--primary" type="submit">Add client</button>
        </form>
      </section>

      <section class="portal-card">
        <h2>Recent uploads</h2>
        <?php if (!$recent): ?>
          <p class="portal-table__note">No documents received yet.</p>
        <?php else: ?>
          <ul class="portal-recent" role="list">
            <?php foreach ($recent as $f): ?>
              <li><a href="download.php?id=<?= (int) $f['id'] ?>"><?= e($f['original_name']) ?></a>
                <span><?= e($f['business']) ?> &middot; <?= e(human_size((int) $f['size_bytes'])) ?></span></li>
            <?php endforeach; ?>
          </ul>
        <?php endif; ?>

        <h2 class="portal-h2-spaced">Admins (<?= count($admins) ?>)</h2>
        <ul class="portal-recent" role="list">
          <?php foreach ($admins as $a): ?>
            <li><?= e($a['name'] ?: $a['email']) ?><span><?= e($a['email']) ?></span></li>
          <?php endforeach; ?>
        </ul>
        <p class="portal-table__note">An admin gets full access to every client's checklist.</p>
        <form method="post">
          <?= csrf_field() ?>
          <input type="hidden" name="action" value="add_admin">
          <div class="field"><label for="an">Name (optional)</label><input type="text" id="an" name="name"></div>
          <div class="field"><label for="ae">Email</label><input type="email" id="ae" name="email" required></div>
          <button class="btn btn--outline" type="submit">Add an admin</button>
        </form>
      </section>
    </div>
  </div>
</section>
<?php
portal_foot();
