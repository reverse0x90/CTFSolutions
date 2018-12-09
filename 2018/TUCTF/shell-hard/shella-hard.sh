#!/bin/bash          
socat -d -d TCP-LISTEN:12345,reuseaddr,fork SYSTEM:"./shella-hard",pty,raw,echo=0
