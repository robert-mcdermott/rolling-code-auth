# Rolling Code Security System

## Overview
This repository contains an example implementation of a rolling code security system, similar to those used in modern garage door openers and Remote Keyless Entry (RKE) car key fobs. This is an implementation of a rolling code system to use as a client-server authentication system, offering a secure alternative to traditional passwords and API keys.

This is a reference implementation, I doesn't do anything beyond authentication, you'll have to integrated into your application as need.


### What is a Rolling Code?
A rolling code is a security technology used in remote keyless entry systems where each use of the remote control generates a new code. This code changes with every use, based on a shared secret, algorithm and a counter, enhancing security by preventing replay attacks. It's essentially a One Time Password (OTP) system. In this implemenation, 

## Components
1. **Client (Remote Control)**: Simulates a remote device sending a unique code to the server for authentication.

2. **Server (Garage Door Opener)**: Represents the server that receives and validates the code sent by the client.

## How It Works
1. **Code Generation**: The client and server start with a shared secret seed and a counter. The client generates a code (SHA-256 cryptographic hash) using the shared secret seed and counter for each authentication attempt.

2. **Code Transmission**: The client sends the code (SHA-256 cryptographic hash) to the server.

3. **Code Validation and Tolerance**: The server validates the received code. If the server's counter is slightly out of sync with the client (within a specified tolerance), it still accepts the code and resynchronizes its counter with the client's counter.

4. **Counter value persistance**: Both client and server store the current counter value in an SQLite database to continue from the last state after restarts.

## Handling Counter Desynchronization
- **Tolerance for Desynchronization**: The system allows a tolerance for the counters to be slightly out of sync. This is crucial for scenarios where the client might use the remote out of the server's range, causing the client's counter to increment without the server's knowledge.

- **Resynchronization**: When a code is received within this tolerance range, the server adjusts its counter to match the client's, effectively resynchronizing them. This mechanism ensures that occasional desynchronization doesn't disrupt the system's functionality. If the client's counter gets farther ahead of the server's counter than the tolerance allows (failed auth attempts, due to network interruptions, etc.), automatic resynchronization will no longer be possible and will require manual intervention (zeroing the counters by deleting the databases for both the client and server)

## Security Features
- **Shared Secret**: The shared secret is not transmitted over the network.
- **Rolling Codes**: Resilient against replay attacks.

## Implementation Details
- **Python**: Implemented in Python, with FastAPI for the server.
- **SQLite Database**: Stores the state of the counters.

## Setup and Usage

**Install requirements:**

with Poetry:
```
poetry install
```
with Pip:
```
pip install -r requirements.txt
```

Copy example.env to .env and edit it and update the 'SECRET_KEY' to something secure.

### Server
- Run `python server.py` to start the server.

### Client
- Run `python client.py` to send an authentication request to the server.

## Potential Applications
Suitable for various applications requiring secure client-server authentication, as an alternative to password or API key methods.

## Disclaimer
This implementation is for demonstration and educational purposes. Additional security measures such as putting behind an HTTPS/TLS proxy to encrypt communication between the client and server, logging and additional features may be required for production use.
