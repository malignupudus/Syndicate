#!/usr/bin/env bash

rm conf/*.db 2> /dev/null
rm conf/pass 2> /dev/null
rm databases/credentials/*.db 2> /dev/null
rm databases/credentials/admins/*.db 2> /dev/null
rm databases/credentials/rooks/*.db 2> /dev/null
rm databases/profile/* --dir --force --recursive 2> /dev/null
rm databases/preserved/*.db 2> /dev/null
rm databases/tmp/*.db 2> /dev/null
rm logs/*.log 2> /dev/null
rm public/* --dir --force --recursive 2> /dev/null
rm share/* --dir --force --recursive 2> /dev/null
rm defend/logs/*.log 2> /dev/null
