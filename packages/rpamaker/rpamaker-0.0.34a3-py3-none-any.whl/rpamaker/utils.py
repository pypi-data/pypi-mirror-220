import datetime
import logging
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from distutils.dir_util import copy_tree
from multiprocessing import Process

import requests
from fastapi import HTTPException, status

from rpamaker.orquestador import OrquestadorAPI


def get_base_path():
    file_location = os.getcwd()
    return file_location


def call_command(command, t_id):
    exit_code, stdout = run_suprocess(command)

    orquestador = OrquestadorAPI(t_id)
    if exit_code == 0:
        orquestador.send_status_logs_infra(stdout, "SUCCESS", "Robot ejecutado con exito")
    else:
        orquestador.send_status_logs_infra(stdout, "FAILURE", "Error al ejecutar el robot")
    return exit_code, stdout


def call_deployment(zip_url, headers, deployment_id, path):
    orquestador = OrquestadorAPI()
    root_path = get_base_path()
    b_path = path.split(".")
    other_path = b_path[:-1]
    base_path = os.path.join(root_path, *other_path)

    result = requests.get(zip_url, headers=headers, timeout=15)
    if result.status_code != 200:
        logging.error("Error in downloading the zip file")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in downloading the zip file")

    now = datetime.now().strftime("%Y%m%d%H%M%S%f")
    extract_dir = os.path.join(tempfile.gettempdir(), now)
    archive_file = os.path.join(extract_dir, f"build_{deployment_id}.zip")
    os.makedirs(extract_dir)

    with open(archive_file, "wb") as file_pointer:
        file_pointer.write(result.content)
        logging.info("extracting zip file '%s' to '%s'", archive_file, extract_dir)
    shutil.unpack_archive(archive_file, extract_dir, "zip")
    os.remove(archive_file)
    from_dir = os.path.join(os.path.join(extract_dir, os.listdir(extract_dir)[0]), "base")

    if not os.path.isdir(extract_dir):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in structure robot")

    # # deep comparison req for pip install -r requirements.txt
    # f1=f"{from_dir}\\requirements.txt"
    # f2=f"{base_path}\\requirements.txt"
    # result = filecmp.cmp(f1, f2, shallow=False)
    # if result == False:
    #     logging.info("Installing requirements.txt")

    logging.info("Updating folders from '%s' to '%s'", from_dir, base_path)
    copy_tree(from_dir, base_path)
    response = orquestador.deploy(deployment_id=deployment_id, status="SUCCESS", message="Deployed successfully")
    if response.status_code != 200:
        logging.error(response.text)


def call_robot(keyword, variables, t_id):
    root_path = get_base_path()
    b_path = keyword.split(".")
    task_path = b_path[-1]
    other_path = b_path[:-1]

    base_path = os.path.join(root_path, *other_path)
    env_path = os.path.join(root_path, f"{b_path[0]}")

    logging.info("call_robot: %s %s %s", keyword, variables, base_path)

    output_path = os.path.join(base_path, "output/")
    robot_path = os.path.join(base_path, f"{task_path}.robot")

    now = datetime.strftime(datetime.now(), "%y%m%d%H%M%S%f")
    output_file = "output-" + now + ".xml"
    log_file = "log-" + now + ".html"
    report_file = "report-" + now + ".html"

    if platform.system() == "Windows":
        python_path = (os.path.join(env_path, "venv/Scripts/python.exe"),)
    else:
        #python_path = os.path.join(env_path, "venv/bin/python")
        #Path contendor
        python_path = "/usr/local/bin/python"

    command = [
        python_path,
        "-m",
        "robot",
        "--pythonpath",
        base_path,
        "--listener",
        "rpamaker.listener.Listener",
        *variables,
        "--log",
        os.path.join(output_path, log_file),
        "--output",
        os.path.join(output_path, output_file),
        "--report",
        os.path.join(output_path, report_file),
        robot_path,
    ]

    print(command)
    if platform.system() != "Windows":
        command = " ".join(command)

    exit_code, stdout = run_suprocess(command)

    orquestador = OrquestadorAPI(t_id)
    if exit_code == 0:
        orquestador.send_logs_infra(stdout)
    else:
        orquestador.send_status_logs_infra(stdout, "FAILURE", "Error al ejecutar el robot")


def run_suprocess(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = ""

    while True:
        nextline = process.stdout.readline()
        if nextline == b"" and process.poll() is not None:
            break

        stdout = stdout + nextline.decode("latin1")
        sys.stdout.write(nextline.decode("latin1"))
        sys.stdout.flush()

    exit_code = process.returncode

    return exit_code, stdout


def start_process(keyword, variables, t_id):
    process = Process(target=call_robot, args=(keyword, variables, t_id))
    process.start()
    logging.info("Process %s started", process)


def start_command(command, t_id):
    process = Process(target=call_command, args=(command, t_id))
    process.start()
    logging.info("Process %s started", process)


def start_deploy(_zip_url, _headers, _deployment_id, _path):
    p = Process(
        name=f"Deployment_{_deployment_id}", target=call_deployment, args=(_zip_url, _headers, _deployment_id, _path)
    )
    p.start()
    logging.info(f"Deployment {p} started")
