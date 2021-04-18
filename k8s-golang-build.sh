#!/usr/bin/env bash
set -e

project=$1
codepath=$2

dir=${PWD}


cd ${dir}
binfile=${dir}/${project}


cd ${codepath}
go build -o ${binfile} main.go


