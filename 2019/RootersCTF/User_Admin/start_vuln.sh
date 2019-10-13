#!/bin/bash          
socat -d -d TCP-LISTEN:3333,reuseaddr,fork SYSTEM:"./vuln",pty,raw,echo=0
