#!/usr/bin/expect

spawn python3 test_p.py
expect "please input:" 
send "a\n"
expect "ab:"
send "a\n"
expect "b:"
send "b\n"

