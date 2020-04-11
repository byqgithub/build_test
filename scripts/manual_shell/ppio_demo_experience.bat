@echo off

set script_path="%~dp0"

cd %script_path%

set /a counter=0
set max=10

:loop
set /a counter=%counter%+1
set start_time="%date%   %time%"
echo "execute times :"%counter%
::.\poss_win.exe put-object --bucket=ppio-demo --key=/test/test_%counter%.txt --body=%script_path%\1G --chiprice=200 --copies=5 --expires=2019-12-12 --rpcport=18060
.\poss_win.exe get-object --bucket=ppio-demo --key=ppio_demo_upload_1G_office_2 --chiprice=200 --rpcport=18060 --outfile=D:\download\ppio_demo\PPIO-demo\resources\extraResources\outfile_%counter%

set end_time="%date%   %time%"
echo start time: %start_time%
echo end time:   %end_time%
echo execute times :%counter%               start time: %start_time%                 end time: %end_time% >> ./record.txt

if not %counter%==%max% goto loop

.\poss_win.exe sync-objects --rpcport=18060
.\poss_win.exe list-objects --bucket=ppio-demo --rpcport=18060 > ./list_objects.txt
.\poss_win.exe list-tasks --rpcport=18060 > ./list_tasks.txt

pause