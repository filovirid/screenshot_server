#!/bin/bash
kill `ps aux | grep  -E '[s]{1}c_api\.py' | sed -n --regexp-extended 's/([a-z]{1,})\s{1,}([0-9]{1,}).*/\2/p'`;
sleep 2;
cd /home/scrapi/screenshot_api && nohup python3 sc_api.py &
