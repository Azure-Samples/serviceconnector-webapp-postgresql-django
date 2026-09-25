@echo off
if not defined DBPASS (
    echo Set DBPASS securely before running env.bat. 1>&2
    exit /b 1
)
if not defined ResourceConnector_demo_Key (
    echo Set ResourceConnector_demo_Key securely before running env.bat. 1>&2
    exit /b 1
)

set DBHOST=resourceconnector-postgres.postgres.database.azure.com
set DBUSER=pollsdb
set DBNAME=resourceconnector@resourceconnector-postgres
set DJANGO_ENV=production

set ResourceConnector_demo_TargetServiceEndpoint=resourceconnector-postgres.postgres.database.azure.com
set ResourceConnector_demo_SubResourceName=pollsdb
set ResourceConnector_demo_Name=resourceconnector@resourceconnector-postgres
set DJANGO_ENV=production
exit /b 0