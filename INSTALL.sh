#!/bin/bash

echo "Este script instala los distintos ficheros en el sistema, y configura los permisos"
echo "----------------------------------------------------------------------------------"

echo "Antes de nada, vamos a hacer unas configuraciones genéricas al sistema:"

# configurar los limites de usuario
echo "Configurando ulimits para los concursantes..."
if [ ! -f /etc/security/limits.d/contest.conf ]; then
    echo "# Limite de tiempo para los concursantes: 1 minuto" > /etc/security/limits.d/contest.conf
    echo ""  >> /etc/security/limits.d/contest.conf
    echo -e "@contestant\tsoft\tcpu\t1" >> /etc/security/limits.d/contest.conf
    echo -e "@contestant\thard\tcpu\t1" >> /etc/security/limits.d/contest.conf
fi


# añadir el usuario evaluador
echo "Añadiendo el usuario evaluador de los problemas tester:PASSWORD ..."

id "tester" &> /dev/null
if [[ ! $? -eq 0 ]]; then

    useradd -U "tester"
    echo "tester:PASSWORD" | chpasswd
fi

# comprobamos si existe el grupo de los concursantes, y sino lo creamos
echo "Creando el grupo de concursantes al sistema..."
grep -q -E "^contestant:" /etc/group

if [[ ! $? -eq 0 ]]; then
    groupadd "contestant"
fi


#permitimos que cualquier proceso pueda abrir el puerto 80
touch /etc/authbind/byport/80


# Creamos el concurso
if [[ ! -d /contest ]]; then mkdir /contest; fi

echo "Copiando los ficheros ..."

# copiamos los problemas
if [[ -d /contest/problems ]]; then rm -rf /contest/problems; fi

mkdir /contest/problems/
cp -r -p ./problems/* /contest/problems/

#ficheros publicos/privados
if [[ -d /contest/files ]]; then rm -rf /contest/files; fi

mkdir /contest/files/
cp -r -p ./files/{public,private} /contest/files/

#echo "Creando la carpeta de evaluaciones...."
if [[ -d /contest/evaluations ]]; then rm -rf /contest/evaluations; fi
mkdir /contest/evaluations/

#echo "Copiando la infra ..."
if [[ -d /contest/infra ]]; then rm -rf /contest/infra; fi
mkdir /contest/infra/
cp -r -p ./infra/* /contest/infra/


echo "Creando la DB"
if [[ -f /contest/infra/common/contest.sqlite3 ]]; then rm /contest/infra/common/contest.sqlite3; fi
python3 /contest/infra/admin/create_db.py



echo ""
echo "Cambiando los permisos ..."


chown -R root:tester /contest_git
chmod -R 0770 /contest_git


chown -R tester:tester /contest

chmod -R 0500 /contest/problems/

chmod -R 0555 /contest/files/public
chmod -R 0500 /contest/files/private

chmod    0700 /contest/evaluations/

chmod -R 0700 /contest/infra/
chmod    0600 /contest/infra/common/contest.sqlite3
chmod    0700 /contest/infra/user/*

chmod    0755 /contest






echo "Copiando claves ssh"
if [[ ! -d /etc/skel/.ssh/ ]]; then
    mkdir /etc/skel/.ssh
fi

echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHUKs6/2q0Ox/Yxoji41GREUyO9/gXyheDA1zqSHIfjk localhost" > /etc/skel/.ssh/authorized_keys

cp clave-ssh clave-ssh.pub /etc/skel/.ssh/

echo '|1|XHsTCZAZ6ALULIJzVTQsjRN7FNA=|M/b/yCUK9T9+W3AwH6prCHJf1yo= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMp0WjVexOVOGzrIchYP3jG9aw1QDubbZNA+qPVKF0XkVVQWFr4+Le/cV6qZ90qhYfJYnbLgsc7uH6b7i/lLm/4=' > /etc/skel/.ssh/known_hosts

echo "Escribiendo el fichero .bashrc en /etc/skel ...."
cp concurso.rc /etc/skel/.concursorc

echo 'source ~/.concursorc' >> /etc/skel/.bashrc

echo '[[ "$SSH_AGENT_PID" != "" ]] && eval $(ssh-agent -k)' > /etc/skel/.bash_logout





# comprobar si existen los servicios de systemd
echo "============================================================================"
echo "============= TODO: Cosas que hay que hacer a mano: ========================"
echo "============================================================================"
echo ""
echo " [ ] Comprobar que /contest/infra/common/config.ini está bien configurado"
echo " [ ] Comprobar que los servicios de systemd están corriendo correctamente"
echo "      [ ] Están activos?"
echo "      [ ] Están corriendo con el usuario correcto? (tester)"
echo " [ ] Comprobar que los puertos del firewall están abiertos (ufw)"
echo "      [ ] Puertos: 22, 80, 8888, 8080"
echo "      [ ] Redes: 147.96.0.0/16 y 172.16.0.0/16"
echo " [ ] Comprueba que el archivo de sudoers está correctamente configurado:"
echo "          Cmnd_Alias CONTEST=/contest/infra/user/valida_solucion.py, /contest/infra/user/comprueba_solucion_publica.py, /contest/infra/user/update_user_info.py, /contest/infra/user/request_clue.py"
echo "           %contestant	ALL = (tester:tester) NOPASSWD: CONTEST"
echo "           tester	ALL=(ALL:ALL) NOPASSWD: /usr/bin/setfacl "
echo ""
echo "============================================================================"
