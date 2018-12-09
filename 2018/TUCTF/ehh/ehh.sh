#!/bin/bash          
socat -d -d TCP-LISTEN:12345,reuseaddr,fork SYSTEM:"./ehh",pty,raw,echo=0
