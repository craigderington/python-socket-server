##### Python3 Socket Server and Client + Data Model


1. Socket server listens for incoming connections on port 9060.
2. Client tests server with sample encoded radio data.
3. Data stream is broken in to 1024 byte chunks
4. The socket server decodes the data stream
5. Valid radio transmission detected, radio tx database tx_header records are created.
6. The decoded radio data transmission data readings are decoded from the data stream and are stored in the related table tx_readings.
7. Socket server terminates the connection on close.

