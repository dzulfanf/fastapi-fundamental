# AWS EC2 Deployment Guide

This guide documents the deployment of FastAPI Fundamental to an Ubuntu
EC2 instance, managed by `systemd` and exposed through Nginx.

AWS console labels, prices, and account eligibility can change. Replace
placeholders with the current values in your AWS console.

## Architecture

``` text
Client / Browser
       |
       | HTTP :80
       v
AWS Security Group
       |
       v
Nginx (EC2, port 80)
       |
       | proxy_pass to 127.0.0.1:8000
       v
Uvicorn / FastAPI (systemd service)
```

Uvicorn listens only on `127.0.0.1:8000`. Nginx receives public HTTP
traffic on port `80` and forwards it to the application. Do not expose
port `8000` to the internet.

## 1. Create an EC2 instance

In AWS Console:

1.  Open **EC2** and choose the intended Region. This walkthrough used
    Singapore (`ap-southeast-1`).
2.  Choose **Launch instance** and name it, for example,
    `fastapi-fundamental`.
3.  Select **Ubuntu Server 24.04 LTS**.
4.  Choose an instance type appropriate for a learning workload, such as
    `t3.micro` if available and suitable for your account.
5.  Create or select an SSH key pair and download the private key as a
    `.pem` file.
6.  Configure a security group with these inbound rules:
    -   SSH / TCP `22` from **My IP**.
    -   HTTP / TCP `80` from `0.0.0.0/0`.
    -   Do not add port `8000`.
    -   Add HTTPS / TCP `443` when HTTPS is configured.
7.  Select an EBS root volume appropriate for the exercise. The instance
    in this walkthrough used an 8 GiB `gp3` volume.
8.  Launch the instance and wait for it to be running with passing
    status checks.
9.  Copy its **Public IPv4 address**.

### Cost considerations

Check current AWS pricing and your account's Free Tier or credit
eligibility. Charges may apply to EC2 compute, EBS storage, public IPv4
addresses, data transfer, and other resources. Eligibility and
allowances vary. Consider setting a billing budget or alert. Stopping an
instance does not necessarily stop all charges.

## 2. Connect from Windows using SSH

Store the downloaded private key securely and outside the repository.
The example path used in this walkthrough was:

``` text
D:\Development\aws\fastapi-fundamental-key.pem
```

Replace the path if yours differs.

### Fix private-key permissions

If SSH reports that permissions are too open, run these commands in
PowerShell:

``` powershell
icacls "D:\Development\aws\fastapi-fundamental-key.pem" /inheritance:r
icacls "D:\Development\aws\fastapi-fundamental-key.pem" /remove "NT AUTHORITY\Authenticated Users"
icacls "D:\Development\aws\fastapi-fundamental-key.pem" /remove "BUILTIN\Users"
icacls "D:\Development\aws\fastapi-fundamental-key.pem" /remove "Everyone"
icacls "D:\Development\aws\fastapi-fundamental-key.pem" /grant:r "$($env:USERDOMAIN)\$($env:USERNAME):(R)"
```

If a group is not present, `icacls` may report that it could not find
the mapping. Inspect the resulting permissions and ensure only the
intended account can read the key.

### Connect to EC2

Replace `YOUR_EC2_PUBLIC_IP` with the current public IPv4 address:

``` powershell
ssh -i "D:\Development\aws\fastapi-fundamental-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

The default username for Ubuntu EC2 images is usually `ubuntu`.

Verify the environment:

``` bash
whoami
cat /etc/os-release
python3 --version
git --version
```

The walkthrough used Ubuntu Server 24.04 LTS, Python `3.12.3`, and Git
`2.43.0`; your versions may differ.

## 3. Update Ubuntu and install prerequisites

Run in the EC2 SSH session:

``` bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git
```

Verify:

``` bash
python3 --version
git --version
```

## 4. Clone the repository

``` bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/dzulfanf/fastapi-fundamental.git
cd fastapi-fundamental
ls -la
```

Confirm that `requirements.txt` and the `src` directory exist. If the
repository is private, configure Git authentication securely; never
commit or share access tokens.

## 5. Create a virtual environment and install dependencies

From `~/apps/fastapi-fundamental`:

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The shell prompt usually shows `(.venv)` while the environment is
active. If installation fails, inspect the first package-specific error.
Requirements generated on another operating system can include
platform-specific packages; fix the requirements instead of ignoring the
error.

## 6. Run FastAPI locally on EC2

With the virtual environment active and the current directory set to the
repository root:

``` bash
python -m uvicorn app.main:app \
  --app-dir src \
  --host 127.0.0.1 \
  --port 8000
```

Expected output indicates Uvicorn is running at `http://127.0.0.1:8000`.

Keep that terminal running. Open a second SSH session and test:

``` bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/docs
```

Expected: - `/` returns `{"message":"Hello, FastAPI!"}`. - `/health`
returns `{"status":"ok"}`. - `/docs` returns HTML for Swagger UI.

Stop the manually started server with `Ctrl+C` before configuring
`systemd`.

**Security:** Keep Uvicorn bound to `127.0.0.1`. Do not expose port
`8000` in the security group.

## 7. Configure systemd

Create the service file:

``` bash
sudo nano /etc/systemd/system/fastapi-fundamental.service
```

Paste this complete configuration:

``` ini
[Unit]
Description=FastAPI Fundamental Application
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/apps/fastapi-fundamental
ExecStart=/home/ubuntu/apps/fastapi-fundamental/.venv/bin/python -m uvicorn app.main:app --app-dir src --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Save with `Ctrl+O`, press `Enter`, and exit with `Ctrl+X`.

Reload systemd and start the service:

``` bash
sudo systemctl daemon-reload
sudo systemctl enable --now fastapi-fundamental
```

Check the service:

``` bash
sudo systemctl status fastapi-fundamental
curl http://127.0.0.1:8000/health
```

The expected service status is `Active: active (running)`.

Useful commands:

``` bash
sudo systemctl start fastapi-fundamental
sudo systemctl stop fastapi-fundamental
sudo systemctl restart fastapi-fundamental
sudo systemctl status fastapi-fundamental
sudo journalctl -u fastapi-fundamental -n 50 --no-pager
sudo journalctl -u fastapi-fundamental -f
```

Press `Ctrl+C` to stop following live logs.

## 8. Install Nginx

``` bash
sudo apt install -y nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

Confirm Nginx is `active (running)`.

## 9. Configure Nginx as a reverse proxy

Create the site configuration:

``` bash
sudo nano /etc/nginx/sites-available/fastapi-fundamental
```

Paste the complete configuration:

``` nginx
server {
    listen 80;
    listen [::]:80;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Save and exit Nano. Enable the site:

``` bash
sudo ln -s /etc/nginx/sites-available/fastapi-fundamental /etc/nginx/sites-enabled/fastapi-fundamental
```

If the symbolic link already exists, inspect it rather than creating a
duplicate. Disable the default site to avoid its default server block
taking precedence:

``` bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Validate before reloading:

``` bash
sudo nginx -t
```

Proceed only if the output reports `syntax is ok` and
`test is successful`. Then reload:

``` bash
sudo systemctl reload nginx
sudo systemctl status nginx
```

## 10. Verify security group rules

In AWS Console:

1.  Open **EC2 → Instances** and select the instance.
2.  Open **Security** and click the attached security group.
3.  Choose **Edit inbound rules**.
4.  Confirm the intended rules:

  Type    Protocol     Port Source
  ------- ---------- ------ ----------------------------------
  SSH     TCP            22 Your current public IP (`My IP`)
  HTTP    TCP            80 `0.0.0.0/0`
  HTTPS   TCP           443 Add when HTTPS is configured

Do not add port `8000`. If IPv6 access is intended, configure the
corresponding IPv6 rules deliberately. Keep SSH restricted to trusted IP
addresses.

## 11. Verify the public API

Use the current **Public IPv4 address** shown in EC2. Replace the
placeholder below:

``` text
http://YOUR_EC2_PUBLIC_IP/
http://YOUR_EC2_PUBLIC_IP/health
http://YOUR_EC2_PUBLIC_IP/docs
```

From a client outside the EC2 instance:

``` bash
curl http://YOUR_EC2_PUBLIC_IP/
curl http://YOUR_EC2_PUBLIC_IP/health
```

The root and health endpoints should return the expected JSON responses,
and `/docs` should show Swagger UI.

Test the CRUD lifecycle through Swagger UI or another HTTP client:

1.  `POST /items` --- create an item.
2.  `GET /items` --- verify it appears.
3.  `GET /items/{item_id}` --- retrieve it.
4.  `PUT /items/{item_id}` --- update it.
5.  `DELETE /items/{item_id}` --- delete it.
6.  `GET /items/{item_id}` --- confirm the deleted item returns `404`.

Use an item ID returned by the API. In-memory data is lost when the
application process restarts.

## 12. Troubleshooting

### Public URL times out

Check that the instance is running and passing status checks, the public
IP is current, and the security group permits inbound TCP `80`. Then
check Nginx and listening ports:

``` bash
sudo systemctl status nginx
sudo ss -lntp
```

### Nginx returns `502 Bad Gateway`

Check the application service, local endpoint, and logs:

``` bash
sudo systemctl status fastapi-fundamental
sudo journalctl -u fastapi-fundamental -n 50 --no-pager
curl http://127.0.0.1:8000/health
sudo tail -n 50 /var/log/nginx/error.log
sudo tail -n 50 /var/log/nginx/access.log
```

Verify the service's `WorkingDirectory`, virtual environment path, and
Uvicorn import path.

### Nginx configuration test fails

``` bash
sudo nginx -t
```

Use the reported file and line number to correct the configuration. Do
not reload Nginx until the test succeeds.

### systemd service fails to start

``` bash
sudo systemctl status fastapi-fundamental
sudo journalctl -u fastapi-fundamental -n 100 --no-pager
```

Common causes include incorrect paths, missing dependencies, an invalid
import path, or a port conflict.

## 13. Operational notes and next steps

-   The enabled systemd service is configured to start at boot.
-   `Restart=always` asks systemd to restart the process if it exits; it
    does not fix application errors automatically.
-   Nginx receives HTTP requests and forwards them to Uvicorn on
    localhost.
-   This deployment currently uses HTTP, not HTTPS. Do not send
    passwords or sensitive data over it. Configure a domain and
    TLS/HTTPS before using the service for sensitive or production
    traffic, and verify certificate renewal.
-   Swagger UI is publicly accessible in this setup. Reassess this if
    the project evolves.
-   In-memory data is not persistent across process restarts and is not
    shared across multiple application processes.
-   Keep the OS and packages updated, protect the SSH private key,
    restrict SSH access, and monitor AWS billing.
-   Automated tests remain a separate roadmap phase.

## Deployment checklist

-   [ ] EC2 instance is running and status checks pass.
-   [ ] SSH works with a protected private key.
-   [ ] Python, venv, pip, and Git are installed.
-   [ ] Repository is cloned and dependencies are installed.
-   [ ] FastAPI responds to local health checks.
-   [ ] The systemd service is enabled and active.
-   [ ] Nginx configuration passes `sudo nginx -t`.
-   [ ] Nginx is enabled and running.
-   [ ] Security group permits only intended inbound ports.
-   [ ] Public root, health, and Swagger endpoints work.
-   [ ] CRUD endpoints have been verified remotely.
-   [ ] AWS resource usage and costs are understood.
