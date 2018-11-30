# Distribute

A distributed storage project for Aarhus University. Experimentations with replication and erasure codes.

# Architecture

- One Raspbery Pi 3 as a lead node running the REST API (Flask) and holding the
  files ledger
- 4 slave Raspbery Pi 2's as storage nodes
