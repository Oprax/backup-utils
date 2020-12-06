#!/bin/bash

set -e

if [ -z $AUTH ]
then
    echo "Missing 'AUTH' variable"
    exit 1
fi


if [ -z $FILE_BIN ] && [ -f $FILE_BIN ] && [ -r $FILE_BIN ]
then
    echo "Missing 'FILE_BIN' variable"
    exit 1
fi

VERSION=$(poetry version --short --no-ansi)

if [ -z $VERSION ]
then
    echo "variable 'VERSION' is empty"
    exit 1
fi

RESOLVE_FILE_BIN=$(realpath $FILE_BIN)

FILE_PATH="backup-utils/$VERSION/backup_utils.pyz"
curl --user "$AUTH" -X POST -F filepath="$FILE_PATH" -F filebin="@$RESOLVE_FILE_BIN" https://download.oprax.fr/v1/upload/

FILE_PATH_LATEST="backup-utils/latest/backup_utils.pyz"
curl --user "$AUTH" -X POST -F "filepath=$FILE_PATH_LATEST" -F "filebin=@$RESOLVE_FILE_BIN" https://download.oprax.fr/v1/upload/
