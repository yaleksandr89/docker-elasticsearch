#!/bin/bash
set -eu
export LC_ALL=C
label='[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?'
for domain in "${ELASTIC_DOMAIN:?}" "${KIBANA_DOMAIN:?}"; do
    if [[ ${#domain} -gt 253 || ! $domain =~ ^$label(\.$label)*$ ]]; then
        echo 'Expected a DNS hostname for each virtual host.' >&2
        exit 1
    fi
done
shopt -s nocasematch
if [[ $ELASTIC_DOMAIN == "$KIBANA_DOMAIN" || ${ELASTIC_PORT:?} != 9200 || ${KIBANA_PORT:?} != 5601 ]]; then
    echo 'Use distinct domains and the internal ports 9200 and 5601.' >&2
    exit 1
fi
