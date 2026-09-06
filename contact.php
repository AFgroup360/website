<?php
/**
 * Contact form handler for AmeriFinancial.
 *
 * GoDaddy shared hosting runs PHP, so the form can post here and be emailed
 * without a third party service. Drop this file in public_html alongside
 * index.html. Nothing else is required.
 *
 * If the site is ever moved to hosting without PHP, delete this file and set
 * CONTACT_ENDPOINT in js/main.js to a Formspree or Web3Forms URL instead. The
 * form falls back to showing the email address and phone number either way.
 */

declare(strict_types=1);

const TO_ADDRESS  = 'hello@ameri-group.ca';
const FROM_DOMAIN = 'ameri-group.ca';
const SUBJECT     = 'Website enquiry';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function fail(int $code, string $message): void {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $message]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fail(405, 'Method not allowed.');
}

// The form posts JSON. Fall back to a normal form post if JavaScript is off.
$raw   = file_get_contents('php://input') ?: '';
$data  = json_decode($raw, true);
if (!is_array($data)) {
    $data = $_POST;
}

$clean = static function (?string $v, int $max): string {
    $v = trim((string) $v);
    // Strip anything that could be used to inject an extra mail header.
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);
    return mb_substr($v, 0, $max);
};

// A field a person never sees and never fills in. Bots do.
if ($clean($data['website'] ?? '', 100) !== '') {
    echo json_encode(['ok' => true]);   // Look successful, send nothing.
    exit;
}

$name    = $clean($data['name'] ?? '', 120);
$email   = $clean($data['email'] ?? '', 190);
$company = $clean($data['company'] ?? '', 160);
$message = trim((string) ($data['message'] ?? ''));
$message = mb_substr($message, 0, 5000);

if ($name === '' || $email === '' || $message === '') {
    fail(422, 'Please complete your name, email and message.');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fail(422, 'That email address does not look right.');
}

$body = "New enquiry from the AmeriFinancial website.\n\n"
      . "Name:    {$name}\n"
      . "Email:   {$email}\n"
      . "Company: " . ($company !== '' ? $company : 'not given') . "\n"
      . "Sent:    " . gmdate('Y-m-d H:i') . " UTC\n"
      . "IP:      " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n\n"
      . "Where is the pressure right now?\n"
      . "-------------------------------\n"
      . $message . "\n";

// Send from the domain itself so the host's mail server accepts it, and put
// the enquirer in Reply-To so hitting reply goes to them.
$headers = implode("\r\n", [
    'From: AmeriFinancial website <no-reply@' . FROM_DOMAIN . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'Content-Type: text/plain; charset=utf-8',
    'MIME-Version: 1.0',
    'X-Mailer: PHP/' . phpversion(),
]);

$sent = @mail(TO_ADDRESS, SUBJECT . ' from ' . $name, $body, $headers,
              '-f no-reply@' . FROM_DOMAIN);

if (!$sent) {
    fail(500, 'The message could not be sent.');
}

echo json_encode(['ok' => true]);
