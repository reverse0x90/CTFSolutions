#!/bin/bash          
socat -d -d TCP-LISTEN:1111,reuseaddr,fork SYSTEM:"./vuln",pty,raw,echo=0
