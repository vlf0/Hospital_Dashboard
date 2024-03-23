#!/bin/sh
daphne backend.asgi:application -b 0.0.0.0 -p 8000
