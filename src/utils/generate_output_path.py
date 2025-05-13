import os
from datetime import datetime

def generate_output_path(base_dir: str = "output", prefix: str = "result") -> str:
    now = datetime.now()
    date_str = now.strftime("%m_%d")
    datetime_str = now.strftime("%m%d_%H%M")

    output_dir = os.path.join(base_dir, f"output_{date_str}")
    os.makedirs(output_dir, exist_ok=True)  

    output_filename = f"{prefix}_{datetime_str}.csv"
    output_path = os.path.join(output_dir, output_filename)
    
    return output_path