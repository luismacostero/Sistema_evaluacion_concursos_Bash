#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from configparser import ConfigParser

from get_ranking import get_ranking

import sys
import os.path as op

sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from User import User


# https://pythonbasics.org/webserver/
hostName = "0.0.0.0"
serverPort = 80




class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)


        self.writeHeader()
        self.wfile.write(bytes("<body>", "utf-8"))

        
        self.wfile.write(bytes("<div>", "utf-8"))
        self.wfile.write(bytes("<h1>BASH Friday - IV Concurso Bash 2025 - fdi </h1>", "utf-8"))

        self.wfile.write(bytes("<div style=\"overflow-x:auto;\">", "utf-8"))
        self.writeTable();

        self.wfile.write(bytes("</div>", "utf-8"))

        self.wfile.write(bytes("<div class=\"nota\">Nota: la página se recarga automáticamente cada 10 segundos</div>", "utf-8"))
        self.wfile.write(bytes("</div>", "utf-8"))
        self.wfile.write(bytes("</html>", "utf-8"))

        
    def writeHeader(self):
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head>", "utf-8"))
        self.wfile.write(bytes("<meta charset=\"utf-8\">", "utf-8"))
        self.wfile.write(bytes("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">", "utf-8"))
        # REFRESH cada 10 segs
        self.wfile.write(bytes("<meta http-equiv=\"refresh\" content=\"10\"; >", "utf-8"))
        self.wfile.write(bytes("<title>IV Concurso Bash 2025</title>", "utf-8"))
        
        self.wfile.write(bytes("<style> .nota {color: #333333; font-size: 0.85em} </style>", "utf-8"))
        self.wfile.write(bytes("<style> .AC {background-color: #bde9ba;}\n .WA {background-color: #f5e187;} </style>", "utf-8"))
        self.wfile.write(bytes("<style> tr:nth-child(even) {background-color: #f2f2f2;} </style>", "utf-8"))
        self.wfile.write(bytes("<style> th {background-color: #333333; color:white;} </style>", "utf-8"))
        self.wfile.write(bytes("<style> td {text-align: center;} </style>", "utf-8"))
        self.wfile.write(bytes("<style> th,td {padding: 10px;} </style>", "utf-8"))

        self.wfile.write(bytes("</head>","utf-8"))




    def writeTable(self):
        
        self.wfile.write(bytes("<table class=\"table\">", "utf-8"))

        # Cabecera
        NUM_PROBLEMS = getattr(self, 'NUM_PROBLEMS', None)
        if NUM_PROBLEMS is None:
            parser = ConfigParser()
            parser.read(op.dirname(op.abspath(__file__)) + "/../common/config.ini")
            NUM_PROBLEMS=int(parser.get('general','num_problems'))
            self.NUM_PROBLEMS = NUM_PROBLEMS
            
        
        self.wfile.write(bytes("<thead>", "utf-8"))
        self.wfile.write(bytes("<tr>", "utf-8"))
        self.wfile.write(bytes("<th>Nombre</th>", "utf-8"))
        self.wfile.write(bytes("<th>Puntuación</th>", "utf-8"))
        for i in range(NUM_PROBLEMS):
            self.wfile.write(bytes("<th>Pr" + str(i) + "</th>", "utf-8"))
        self.wfile.write(bytes("</tr>", "utf-8"))
        self.wfile.write(bytes("</thead>", "utf-8"))

        self.wfile.write(bytes("<tbody>", "utf-8"))

        ranking = get_ranking()

        for contestant in ranking:
            user = User(contestant[0])

            self.wfile.write(bytes("<tr>", "utf-8"))
            self.wfile.write(bytes( "<td> " + contestant[0] + "</td>", "utf-8"))
            self.wfile.write(bytes( "<td> " + str(contestant[1]) + "</td>", "utf-8"))
            
            # ACs
            for i in range(contestant[1]):
                info = user.get_problem_info(i)
                self.wfile.write(bytes( "<td class=\"AC\">", "utf-8"))
                self.wfile.write(bytes(str(info[0]) + " / " + str(info[1]) + " / " + str(info[2]), "utf/8"))
                self.wfile.write(bytes(" </td>", "utf-8"))

            for i in range(NUM_PROBLEMS - contestant[1]):
                info = user.get_problem_info(i+contestant[1])


                if(info[1]==0):
                    self.wfile.write(bytes( "<td>", "utf-8"))
                else:
                    self.wfile.write(bytes( "<td class=\"WA\">", "utf-8"))

                self.wfile.write(bytes("-", "utf-8"))
                self.wfile.write(bytes(" / ", "utf-8"))
                self.wfile.write(bytes(str(info[1]), "utf-8"))
                self.wfile.write(bytes(" / ", "utf-8"))
                self.wfile.write(bytes(str(info[2]), "utf-8"))

                self.wfile.write(bytes( "</td>", "utf-8"))
    
            self.wfile.write(bytes("</tr>", "utf-8"))

        self.wfile.write(bytes("</tbody>", "utf-8"))
        self.wfile.write(bytes("</table>", "utf-8"))
        #self.wfile.write(bytes("</div></div></div>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass


    webServer.server_close()
    print("Server stopped.")
