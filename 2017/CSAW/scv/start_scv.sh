#!/bin/bash          
socat -d -d TCP-LISTEN:3764,reuseaddr,fork SYSTEM:"./scv",pty,raw,echo=0