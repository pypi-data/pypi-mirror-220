# MicroService Encryption Lib SGX

## Overview

MSE lib SGX bootstraps the execution of an encrypted ASGI/WSGI Python web application for [Gramine](https://gramine.readthedocs.io/).

The library is responsible for:

- Configuring the SSL certificates with either:
  - *RA-TLS*, a self-signed certificate including the Intel SGX quote in an X.509 v3 extension
  - *Custom*, the private key and full keychain is provided by the application owner
  - *No SSL*, the secure channel may be managed elsewhere by an SSL proxy
- Decrypting Python modules encrypted with XSala20-Poly1305 AEAD
- Running the ASGI/WSGI Python web application with [hypercorn](https://pgjones.gitlab.io/hypercorn/)

## Technical details

The flow to run an encrypted Python web application is the following:

1. A first self-signed HTTPS server using RA-TLS is launched waiting to receive a JSON payload with:
   - UUID, a unique application identifier provided to `mse-bootstrap` as an argument
   - the decryption key of the code
   - Optionally the private key corresponding to the certificate provided to `mse-bootstrap` (for *Custom* certificate)
2. If the UUID and decryption key are the expected one, the configuration server is stopped, the code is decrypted and finally run as a new server


## Installation 

```console
$ pip install mse-lib-sgx
```

## Usage

```console
$ mse-bootstrap --help
usage: mse-bootstrap [-h] --host HOST --port PORT --app-dir APP_DIR --uuid
                     UUID [--version] [--debug]
                     (--self-signed EXPIRATION_DATE | --no-ssl | --certificate CERTIFICATE_PATH)
                     application

Bootstrap ASGI/WSGI Python web application for Gramine

positional arguments:
  application           ASGI application path (as module:app)

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           hostname of the configuration server, also the
                        hostname of the app server if `--self-signed`
  --port PORT           port of the server
  --app-dir APP_DIR     path of the python web application
  --uuid UUID           unique application UUID
  --version             show program's version number and exit
  --debug               debug mode with more logging
  --self-signed EXPIRATION_DATE
                        generate a self-signed certificate for the web app
                        with a specific expiration date (Unix time)
  --no-ssl              use HTTP without SSL
  --certificate CERTIFICATE_PATH
                        custom certificate used for the SSL connection,
                        private key must be sent through the configuration
                        server

```
