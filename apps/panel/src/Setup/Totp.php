<?php
declare(strict_types=1);
namespace ForgePanel\Setup;
/** Narrow RFC 6238 implementation, SHA-1, 30-second step.
 * It is enrollment-only: a future login verifier must persist replay counters too.
 * Standard-library HMAC is used; RFC test vectors are included in tests/run.php. */
final class Totp {
    private const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    public function newSecret(): string { return self::encode(random_bytes(20)); }
    public function code(string $secret, int $timestamp, int $digits=6): string {
        if ($timestamp < 0 || !in_array($digits, [6, 8], true)) { throw new \InvalidArgumentException('Invalid TOTP parameters.'); }
        $counter = intdiv($timestamp, 30);
        $binary = pack('N2', intdiv($counter, 4294967296), $counter % 4294967296);
        $mac = hash_hmac('sha1', $binary, self::decode($secret), true);
        $offset = ord($mac[19]) & 15;
        $number = unpack('N', substr($mac, $offset, 4))[1] & 0x7fffffff;
        return str_pad((string) ($number % (10 ** $digits)), $digits, '0', STR_PAD_LEFT);
    }
    public function match(string $secret, string $code, int $timestamp): ?int {
        if (!preg_match('/\A[0-9]{6}\z/D', $code)) { return null; }
        foreach ([0, -1, 1] as $offset) {
            $at = $timestamp + $offset * 30;
            if ($at >= 0 && hash_equals($this->code($secret, $at), $code)) { return intdiv($at, 30); }
        }
        return null;
    }
    public static function encode(string $raw): string {
        $buffer=0; $bits=0; $out='';
        for ($i=0; $i<strlen($raw); $i++) {
            $buffer=($buffer<<8)|ord($raw[$i]); $bits+=8;
            while ($bits>=5) { $bits-=5; $out.=self::ALPHABET[($buffer>>$bits)&31]; }
            $buffer &= (1<<$bits)-1;
        }
        if ($bits>0) { $out.=self::ALPHABET[($buffer<<(5-$bits))&31]; }
        return $out;
    }
    public static function decode(string $encoded): string {
        if (!preg_match('/\A[A-Z2-7]+\z/D', $encoded)) { throw new \InvalidArgumentException('Invalid base32 secret.'); }
        $buffer=0; $bits=0; $out='';
        foreach (str_split($encoded) as $char) {
            $buffer=($buffer<<5)|strpos(self::ALPHABET, $char); $bits+=5;
            if ($bits>=8) { $bits-=8; $out.=chr(($buffer>>$bits)&255); }
            $buffer &= (1<<$bits)-1;
        }
        if ($buffer!==0) { throw new \InvalidArgumentException('Noncanonical base32.'); }
        return $out;
    }
}
