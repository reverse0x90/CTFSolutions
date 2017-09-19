#!/bin/bash          
socat -d -d TCP-LISTEN:8464,reuseaddr,fork SYSTEM:"./pilot",pty,raw,echo=0