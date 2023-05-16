import psutil
import time

# The name of the application you want to monitor
app_name = "chrome.exe"

while True:
    # Get the current network usage by application
    net_io_counters = psutil.net_io_counters(pernic=False, nowrap=True)

    # Create a dictionary to store the network usage by application
    app_net_usage = {}

    # Loop through all processes and add up the network usage for the specific application
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_io_counters = proc.io_counters()
            if proc_io_counters and proc.info['name'] == app_name:
                if app_name not in app_net_usage:
                    app_net_usage[app_name] = {
                        'bytes_sent': 0,
                        'bytes_recv': 0
                    }
                app_net_usage[app_name]['bytes_sent'] += proc_io_counters[0]
                app_net_usage[app_name]['bytes_recv'] += proc_io_counters[1]
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    # Print the network usage for the specific application in megabytes
    if app_name in app_net_usage:
        
        #print the application name
        print(f"Application: {app_name}")
        
        #print the upload speed
        print(f"Bytes sent: {app_net_usage[app_name]['bytes_sent'] / 1024 / 1024:.2f} MB")
        
        #print the download speed
        print(f"Bytes received: {app_net_usage[app_name]['bytes_recv'] / 1024 / 1024:.2f} MB")

    # Wait for 1 second before checking the network usage again
time.sleep(1)