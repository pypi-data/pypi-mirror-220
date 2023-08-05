REM hatch version fix
hatch clean
hatch build

hatch publish -r main
