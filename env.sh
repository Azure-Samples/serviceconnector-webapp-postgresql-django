if [ -z "${DBPASS:+set}" ]; then
    printf '%s\n' 'Set DBPASS securely before sourcing env.sh.' >&2
    return 1 2>/dev/null || exit 1
fi

export DBHOST="localhost"
export DBUSER="manager"
export DBNAME="pollsdb"
export DBPASS
