#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
go test ./...
go test -race ./...
go vet ./...
find apps/panel -type f -name '*.php' -not -path '*/vendor/*' -print0 | xargs -0 -n1 php -l
php -l apps/panel/bin/console
php apps/panel/tests/run.php
make build
./build/forgepanel version
./build/forgepanel install plan --config examples/install.json --json
printf '\nNative tests only. Symfony, PostgreSQL integration, E2E and OS certification are separate gates.\n'
