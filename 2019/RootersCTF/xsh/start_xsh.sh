#!/bin/bash          
socat -d -d TCP-LISTEN:5555,reuseaddr,fork SYSTEM:"./xsh",pty,raw,echo=0
