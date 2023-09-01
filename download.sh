#!/bin/sh

set -eux

MY_DIR="$(dirname "$(readlink -f "$0")")"

for TITLE in "$@"; do
    poetry run python "$MY_DIR/FunKiiU.py" --titles "$TITLE" --keysite http://127.0.0.1:8000 --online-tickets \
    || poetry run python "$MY_DIR/FunKiiU.py" --titles "$TITLE" --keysite http://127.0.0.1:8000 --online-keys
done

# rsync -av --checksum install/ /media/nuno/TIRA/install/
