.PHONY: build test check clean
build:
	mkdir -p build
	go build -trimpath -o build/forgepanel ./cmd/forgepanel
test:
	go test ./...
	php apps/panel/tests/run.php
check:
	bash scripts/check.sh
clean:
	rm -rf build
