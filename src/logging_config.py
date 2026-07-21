import logging
import os
import multiprocessing
import socket
from pathlib import Path

def setup_logger():
    # Create a logs directory
    Path("log_files").mkdir(exist_ok=True)

    # Defining SLURM environment variables
    job_id = os.getenv("SLURM_JOB_ID", "local")
    array_task = os.getenv("SLURM_ARRAY_TASK_ID", "0")

    # Multiprocessing worker name
    process_name = multiprocessing.current_process().name

    # Naming log file (produces one for each job/item in the array)
    log_file = Path("log_files") / f"convert_{job_id}_{array_task}_{process_name}.log"

    # Get machine information
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "Unknown"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | "
                "%(processName)s | "
                "%(levelname)s | "
                "%(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()],
    )

    logger = logging.getLogger(__name__)

    # Write startup information
    logger.info("=" * 80)
    logger.info("Starting PDF conversion")
    logger.info("Hostname: %s", hostname)
    logger.info("IP Address: %s", ip_address)
    logger.info("SLURM Job ID: %s", job_id)
    logger.info("SLURM Array Task ID: %s", array_task)
    logger.info("Process: %s", process_name)
    logger.info("=" * 80)

    return logger


