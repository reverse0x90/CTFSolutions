#!/bin/bash          
socat -d -d TCP-LISTEN:12345,reuseaddr,fork SYSTEM:"./canary",pty,raw,echo=0
