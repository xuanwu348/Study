#!/usr/bin/expect

exp_internal 1
spawn python3 test_p_01.py
expect "please input:" 
send "a\n"
expect "ab:"
send "a\n"
send "b\n"
interact

