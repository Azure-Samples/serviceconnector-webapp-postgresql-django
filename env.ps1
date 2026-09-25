if ([string]::IsNullOrEmpty($Env:DBPASS)) {
    throw 'Set DBPASS securely before running env.ps1.'
}

$Env:DBHOST = "localhost"
$Env:DBUSER = "manager"
$Env:DBNAME = "pollsdb"
