#!/bin/sh

set -eu

MY_DIR="$(dirname "$(readlink -f "$0")")"

if [ ! -d "$MY_DIR/server_content" ]; then
    mkdir -p "$MY_DIR/server_content"

    # SEE: https://titlekeys.ovh
    curl -fsSL http://vault.titlekeys.ovh/vault.tar.gz | tar xzC "$MY_DIR/server_content" --strip-components 1
fi

exec python3 -m http.server -d "$MY_DIR/server_content"
