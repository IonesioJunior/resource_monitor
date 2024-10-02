import os
import json
from datetime import datetime
import psutil  # Ensure that you have psutil installed in your environment
from syftbox.lib import ClientConfig

def main():
    # Load the client configuration
    config_path = os.environ.get("SYFTBOX_CLIENT_CONFIG_PATH", None)
    client_config = ClientConfig.load(config_path)

    # Get the current CPU and memory usage in percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    # Get the current timestamp
    current_timestamp = datetime.now().isoformat()

    # Prepare the data to be written
    usage_data = {
        "timestamp": current_timestamp,
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": memory_usage
    }

    # Prepare output folders
    output_folder = f"{client_config.sync_folder}/{client_config.email}/public/"
    os.makedirs(output_folder, exist_ok=True)

    # Write usage data to output file
    output_file_path = f"{output_folder}system_usage.json"
    with open(output_file_path, "w") as f:
        json.dump(usage_data, f, indent=2)

    # Write _.syftperm file
    syftperm_data = {
        "admin": [client_config.email],
        "read": ["GLOBAL"],
        "write": [client_config.email],
        "filepath": f"{output_folder}_.syftperm",
        "terminal": False
    }
    syftperm_path = f"{output_folder}_.syftperm"
    with open(syftperm_path, "w") as f:
        json.dump(syftperm_data, f, indent=2)

    print(f"System usage data has been written to {output_file_path}")
    print(f"_.syftperm file has been written to {syftperm_path}")

if __name__ == "__main__":
    main()

