<?php
declare(strict_types=1);
namespace ForgePanel\Setup;
final class SecretBox {
    private readonly string $key;
    public function __construct(string $keyBase64) {
        $key = base64_decode($keyBase64, true);
        if (!is_string($key) || strlen($key) !== SODIUM_CRYPTO_SECRETBOX_KEYBYTES) {
            throw new \RuntimeException('A dedicated 32-byte FORGE_ENCRYPTION_KEY is required.');
        }
        $this->key = $key;
    }
    public function encrypt(string $plain): string {
        $nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        return 'v1:'.base64_encode($nonce.sodium_crypto_secretbox($plain, $nonce, $this->key));
    }
    public function decrypt(string $sealed): string {
        if (!str_starts_with($sealed, 'v1:')) { throw new \RuntimeException('Unknown secret format.'); }
        $raw = base64_decode(substr($sealed, 3), true);
        if (!is_string($raw) || strlen($raw) < SODIUM_CRYPTO_SECRETBOX_NONCEBYTES + SODIUM_CRYPTO_SECRETBOX_MACBYTES) {
            throw new \RuntimeException('Invalid encrypted secret.');
        }
        $plain = sodium_crypto_secretbox_open(substr($raw, 24), substr($raw, 0, 24), $this->key);
        if ($plain === false) { throw new \RuntimeException('Secret authentication failed.'); }
        return $plain;
    }
}
