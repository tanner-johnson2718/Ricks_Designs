import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 65432

n = len(sys.argv)
if not n==2:
    print("ERROR takes single argument, GCODE file to send")
    exit()

file = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    def send(string):
        s.sendall(string.encode('ascii'))
        print(string)

    with open(str(file), encoding="utf-8") as my_file_handle:
        send("subR 0\n")
        send("cmdG M110 N0\n")
        send("cmdG M28 " + file + "\n")

        line = 1

        for chunk in my_file_handle:

            if not (chunk.find("G") == 0 or chunk.find("M") == 0):
                continue

            # Add line number and strip trailing new line
            chunk = "N" + str(line) + " " + chunk.rstrip()
            line += 1

            # strip comments
            off = chunk.find(";")
            if off > -1:
                chunk = chunk[0:off]

            # Calc checksum
            sum = 0
            for c in chunk:
                sum ^= ord(c)
            chunk = chunk + '*' + str(sum)
            send("cmdG " + chunk + "\n")
        send("cmdG M29\n")

        print("Done sending file, sleeping to keep socket open")
        time.sleep(5)