#!/bin/bash

usage() { echo "Usage: $0 [-c <config_file>] [-d <data_dir>]" 1>&2; exit 1; }

while getopts ":c:d:" o; do
    case "${o}" in
        c)
            c=${OPTARG}
            ;;
        d)
            d=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${c}" ] || [ -z "${d}" ]; then
    usage
fi

litenchat=`which litenchat.py`
echo "litenchat = ${litenchat} config_file = ${c} data_dir = ${d}"

panel serve ${litenchat} --autoreload --show --args ${c} ${d}

