#!/bin/bash


SQLITE_WEB_PASSWORD="PASSWORD" sqlite_web -p 8080 -H 0.0.0.0 -P -x /contest/infra/common/contest.sqlite3
