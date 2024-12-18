from tqdm import tqdm
import time

def show_progress(iterable, description="Processing"):
    for _ in tqdm(iterable, desc=description):
        time.sleep(0.01)  # Simulation légère pour chaque étape
