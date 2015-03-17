#!/bin/sh
VERSION="latest"

(cd doc; make)

rm -rf /tmp/skame-doc/
mkdir -p /tmp/skame-doc/
mv doc/*.html /tmp/skame-doc/

git checkout gh-pages || exit 1

rm -rf ./$VERSION
mv /tmp/skame-doc/ ./$VERSION

git add --all ./$VERSION
git commit -a -m "Update ${VERSION} doc"
