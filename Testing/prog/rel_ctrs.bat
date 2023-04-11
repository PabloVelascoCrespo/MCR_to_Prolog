rem set WNDB=C:\WordNet3.0
set WNDB=C:\fernan\docs\publicaciones\journals\PREPARA\2023_WordNet\prog\wn_ek
REM set WNDB=C:\fernan\docs\publicaciones\journals\PREPARA\2023_WordNet\prog\wn_mcr
set cwd %cd%
:begin
cls
call swipl.exe --traditional rel_ctrs.pl
rem pause
cd %cwd%
goto begin
