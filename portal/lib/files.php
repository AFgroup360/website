<?php
/**
 * Uploads. Files are written under a random name so nothing about them can be
 * guessed from a URL, and the original name is kept only in the database.
 */

declare(strict_types=1);

require_once __DIR__ . '/db.php';

const ALLOWED_UPLOAD_TYPES = [
    'pdf'  => 'application/pdf',
    'csv'  => 'text/csv',
    'xls'  => 'application/vnd.ms-excel',
    'xlsx' => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'doc'  => 'application/msword',
    'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'jpg'  => 'image/jpeg',
    'jpeg' => 'image/jpeg',
    'png'  => 'image/png',
    'heic' => 'image/heic',
];

function storage_dir(): string
{
    $dir = config()['storage'];
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    return rtrim($dir, '/');
}

/**
 * @return array{ok:bool, error?:string, stored?:string, original?:string, mime?:string, size?:int}
 */
function store_upload(array $file): array
{
    if (($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
        $why = [
            UPLOAD_ERR_INI_SIZE   => 'That file is larger than the server allows.',
            UPLOAD_ERR_FORM_SIZE  => 'That file is too large.',
            UPLOAD_ERR_PARTIAL    => 'The upload did not finish. Please try again.',
            UPLOAD_ERR_NO_FILE    => 'No file was chosen.',
            UPLOAD_ERR_NO_TMP_DIR => 'The server has nowhere to put the file.',
            UPLOAD_ERR_CANT_WRITE => 'The server could not write the file.',
        ];
        return ['ok' => false, 'error' => $why[$file['error']] ?? 'Upload failed. Please try again.'];
    }
    if (!is_uploaded_file($file['tmp_name'])) {
        return ['ok' => false, 'error' => 'Upload failed. Please try again.'];
    }

    $maxBytes = ((int) (config()['max_upload_mb'] ?? 25)) * 1024 * 1024;
    if ($file['size'] > $maxBytes) {
        return ['ok' => false, 'error' => 'That file is larger than '
            . (int) (config()['max_upload_mb'] ?? 25) . 'MB.'];
    }

    $original = (string) $file['name'];
    $ext = strtolower(pathinfo($original, PATHINFO_EXTENSION));
    if (!isset(ALLOWED_UPLOAD_TYPES[$ext])) {
        return ['ok' => false, 'error' => 'That file type is not accepted. '
            . 'PDF is preferred; images, spreadsheets and Word documents also work.'];
    }

    // Trust the file's contents, not its name.
    $mime = 'application/octet-stream';
    if (function_exists('finfo_open') && ($fi = finfo_open(FILEINFO_MIME_TYPE))) {
        $mime = (string) finfo_file($fi, $file['tmp_name']);
        finfo_close($fi);
    }

    $stored = bin2hex(random_bytes(20)) . '.' . $ext;
    $target = storage_dir() . '/' . $stored;
    if (!move_uploaded_file($file['tmp_name'], $target)) {
        return ['ok' => false, 'error' => 'The file could not be saved. Please try again.'];
    }
    @chmod($target, 0600);

    return [
        'ok'       => true,
        'stored'   => $stored,
        'original' => mb_substr($original, 0, 255),
        'mime'     => $mime,
        'size'     => (int) $file['size'],
    ];
}

function human_size(int $bytes): string
{
    if ($bytes < 1024) {
        return $bytes . ' B';
    }
    $units = ['KB', 'MB', 'GB'];
    $i = -1;
    do {
        $bytes /= 1024;
        $i++;
    } while ($bytes >= 1024 && $i < 2);
    return round($bytes, $bytes >= 10 ? 0 : 1) . ' ' . $units[$i];
}
