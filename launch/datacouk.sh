#!/bin/bash

server_url="http://localhost:8080"

echo "Téléchargement en cours sur DataCouk"
curl ${server_url}/datacouk/download_all_files

