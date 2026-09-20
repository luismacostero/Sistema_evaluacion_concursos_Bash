#!/bin/bash

echo "Este script actualiza los ficheros del concurso, pero intenta no romper nada (por ejemplo, la bd)"

echo ""
echo ""
echo ""

echo "Actualizando git"
cd /contest/git
git pull


echo "Copiando los ficheros ..."


#ficheros publicos/privados
cp -r -p ./files/{public,private} /contest/files/

#echo "Copiando la infra ..."
cp /contest/infra/common/contest.sqlite3 /tmp/contest.sqlite3
#echo "Copiando la infra ..."
cp -r -p ./infra/* /contest/infra
mv /tmp/contest.sqlite3 /contest/infra/common/contest.sqlite3



echo ""
echo "Cambiando los permisos ..."

chmod -R 0555 /contest/files/public
chmod -R 0500 /contest/files/private

chmod 0500 /contest/evaluations/

chmod -R 0500 /contest/infra/
chmod 0700 /contest/infra/user/*

chmod 0755 /contest
chmod -R 0700 /git_2025_v1

cp concurso.rc /etc/skel/.concursorc
