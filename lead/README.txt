This folder contains the project running on the lead node. The Python3 project
is composed of:

- A main application managing the storage and retrieval of files, in all
  transparency for the user
- A RESTful API implemented with Flask, for the user to have a web interface
- An RPC server for receiving commands from the storage nodes
- A strategy module, for the different implementations of file storage
