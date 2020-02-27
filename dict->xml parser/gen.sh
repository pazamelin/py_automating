#!/bin/bash
# Usage: bash scripts/gen.sh

sort -u 1k.txt -o 1k.txt
cp 1k.txt out_alpha.txt
grep -v '[[:out_alpha:]]*' out_alpha.txt
python3 scripts/main.py 1k.txt > test_1k_out.xml
rm *.zip
find . -type f -name "test_1k_out*" -maxdepth 1 -execdir zip '{}.zip' '{}' \;
