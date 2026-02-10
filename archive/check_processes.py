import psutil

print("Top 10 CPU-consuming processes:\n")
print(f"{'Process Name':<30} {'CPU %':<10} {'Memory %':<10}")
print("=" * 50)

# Get all processes
processes = []
for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# Sort by CPU usage
processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

# Print top 10
for proc in processes[:10]:
    print(f"{proc['name']:<30} {proc['cpu_percent']:<10.1f} {proc['memory_percent']:<10.1f}")

print(f"\n\nTotal CPU: {psutil.cpu_percent()}%")
print(f"Total RAM: {psutil.virtual_memory().percent}%")
