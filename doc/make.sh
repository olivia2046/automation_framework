rm -rf automation_framework/source
sphinx-apidoc -o automation_framework/source .. --separate
make clean
make html
