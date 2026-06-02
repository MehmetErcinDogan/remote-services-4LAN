#!/bin/bash

docker compose down

docker rm remote-touchpad pdf-processor

docker volume rm nginx_access_logs stirling_pdf_configs stirling_pdf_train_data     