# V Edición del concurso de BASH (segundo semestre 2025/2026)

Comprueba la carpeta de /utils !!!

Ahí hay scripts para:
- Crear la estructura de carpetas de un problema nuevo (create_problem.sh)
- Ver un problema de forma amigable (compose_problem.sh <num>)
- Comprobar todas las soluciones propuestas de un problema (test_solutions.sh <num>)


# Cosas que comprobar antes de que inicie el concurso:
- [ ] Hay un problema que juega con los permisos de los ficheros. Comprobar que
      la solución propuesta es correcta y ajustar los permisos de forma adecuada
- [ ] De igual forma, hay un ejercicio que juega con la fecha de modificación
      (el de backup). Comprobar las fechas y ajustarlas para que la solución sea
      correcta
- [ ] Comprobar si /etc/motd está con la fecha adecuada
- [ ] Comprobar que en el /etc/skel/.bashrc no haya más de una copia de la misma
      línea al final. El script de INSTALL.sh añade al final cosas, pero no
      comprueba si ya está añadido o no ...
- [ ] Comprobar que el agente ssh está corriendo con un usuario (debería de
      hacerlo automáticamente el .bashrc generado por el script INSTALL.sh).
  - [ ] Comprobar además que la clave ssh está añadida al agente para que el
      	problema de ssh no dé ninǵun problema (ssh-add -l).
- [ ] Comprobar que al hacer logout finaliza el agente ssh (igual que antes,
      debería de hacerlo automáticamente).
- [ ] Comprobar que /contest/infra/common/config.ini está bien configurado
- [ ] Comprobar que los servicios de systemd están corriendo correctamente
  - [ ] ¿Están activos?
  - [ ] ¿Están corriendo con el usuario correcto? (tester)
- [ ] Comprobar que los puertos del firewall están abiertos (ufw)
  - [ ] Puertos: 22, 80, 8888, 8080
  - [ ] Redes: 147.96.0.0/16 y 172.16.0.0/16
- [ ] Comprueba que el archivo de sudoers está correctamente configurado:
          Cmnd_Alias CONTEST=/contest/infra/user/valida_solucion.py, /contest/infra/user/comprueba_solucion_publica.py, /contest/infra/user/update_user_info.py, /contest/infra/user/request_clue.py
          %contestant	ALL = (tester:tester) NOPASSWD: CONTEST
          tester	ALL=(ALL:ALL) NOPASSWD: /usr/bin/setfacl
      

# TODO things:

- [ ] Cheatsheet en formato txt en las home?
- [ ] Diff con la solución pública ....
