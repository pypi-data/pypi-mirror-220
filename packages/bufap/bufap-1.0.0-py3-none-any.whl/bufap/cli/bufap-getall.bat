@ECHO OFF

SET HOST=192.168.17.101
SET USER=admin
SET PASS=password

cd /d %~dp0

mkdir output

bufap-cli.exe --exec --command "show config all" --outfile "output\%HOST%-config.txt" --host %HOST% --username %USER% --password %PASS%
bufap-cli.exe --exec --command "show status all" --outfile "output\%HOST%-status.txt" --host %HOST% --username %USER% --password %PASS%
bufap-cli.exe --exec --command "show syslog facility all" --outfile "output\%HOST%-syslog.txt" --host %HOST% --username %USER% --password %PASS%
bufap-cli.exe --client-monitor --outfile "output\%HOST%-client.csv" --format csv --host %HOST% --username %USER% --password %PASS%
bufap-cli.exe --wireless-monitor --outfile "output\%HOST%-wireless.csv" --format csv --host %HOST% --username %USER% --password %PASS%
