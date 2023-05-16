import psutil

# Get the current network usage by application
net_io_counters = psutil.net_io_counters(pernic=False, nowrap=True)

# Create a dictionary to store the network usage by application
app_net_usage = {}

# Loop through all processes and add up the network usage by application
for proc in psutil.process_iter(['pid', 'name']):
    
    try:
        proc_io_counters = proc.io_counters()
        
        if proc_io_counters:
            app_name = proc.info['name']
            
            if app_name not in app_net_usage:
                app_net_usage[app_name] = {
                    'bytes_sent': 0,
                    'bytes_recv': 0
                }
            app_net_usage[app_name]['bytes_sent'] += proc_io_counters[0]
            
            app_net_usage[app_name]['bytes_recv'] += proc_io_counters[1]
    
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

# Print the network usage by application
for app_name, data in app_net_usage.items():
    
    #print the application name
    print(f"Application: {app_name}")
    
    #print the upload
    print(f"Bytes sent: {data['bytes_sent']}")
    
    #print the download
    print(f"Bytes received: {data['bytes_recv']}")