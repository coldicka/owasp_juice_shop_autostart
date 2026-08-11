import os
import sys
import subprocess

JUICE_SHOP_DIR = "/home/kali/Projects/juice-shop"


def install_service():
    """Erstellt den Systemd-Service einmalig."""
    # Check whether the script is running with root privileges
    if os.geteuid() != 0:
        print("Error: This script must be run with 'sudo' to complete \n"
              "the setup!")
        sys.exit(1)

    # Define the content for the systemd service file
    service_content = f"""[Unit]
    Description=OWASP Juice Shop Autostart
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory={JUICE_SHOP_DIR}
    ExecStart=/usr/bin/npm start
    Restart=always
    User=root

    [Install]
    WantedBy=multi-user.target
    """

    # Save the configuration file for Systemd
    service_file = "/etc/systemd/system/juice_shop.service"

    try:
        # Write the .service file to /etc/systemd/system/
        with open(service_file, "w") as f:
            f.write(service_content)

        # Notify systemd that a new service file exists
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "juice_shop.service"], check=True)
        subprocess.run(["systemctl", "start", "juice_shop.service"], check=True)

        print("Successfully set up and launched!")
    except Exception as e:
        print(f"Error during setup: {e}")


if __name__ == "__main__":
    install_service()
