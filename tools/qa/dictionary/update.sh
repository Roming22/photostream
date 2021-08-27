#!/bin/bash
echo "Update dictionary"
set -e
set -o pipefail
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

set -x
parse_args(){
    DICT="${SCRIPT_DIR}/words.txt"
    while [[ "$#" -gt "0" ]]; do
        case $1 in
            --check)
                ACTION="check"
                ;;
        esac
        shift
    done
    ACTION="${ACTION:-generate}"
}

generate(){
    { "${SCRIPT_DIR}/../lint.sh" --pylint || true; } \
        | grep ": C0402: " \
        | sed "s/.*Wrong spelling of a word '\(.*\)' in a docstring:/\1/" \
        | sort -u > "${DICT}" || true
}

check(){
    CURRENT="${DICT}.bak"
    NEW="${DICT}.new"
    mv "${DICT}" "${CURRENT}"
    generate
    mv "${DICT}" "${NEW}" 
    mv "${CURRENT}" "${DICT}"
    diff "${DICT}" "${NEW}"
    rm -f "${NEW}"
}

parse_args "$@"
$ACTION
echo "[OK]"