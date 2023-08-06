import datetime
import logging
from datetime import datetime
from urllib.parse import urlparse

import dotenv
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from rpamaker.utils import start_command, start_deploy, start_process

dotenv.load_dotenv(".env")

logging.basicConfig(level=logging.INFO)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


app = FastAPI()


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    api_keys = [config("RPAMAKER_TOKEN")]  # This is encrypted in the database
    if api_key not in api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")


@app.post("/deploy/", dependencies=[Depends(api_key_auth)])
async def deploy(request: Request):
    json_body = {}
    try:
        json_body = await request.json()
    except Exception as err:
        logging.error(err)

    _url = json_body["url"]
    _branch = json_body["branch"]
    _path = json_body["path"]
    _deployment_id = json_body["deployment_id"]
    _, owner, repo = urlparse(_url).path.split("/")

    if "Token" in request.headers.get("X-GitHub-Token"):
        _git_token = request.headers.get("X-GitHub-Token").split()[1]
        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_git_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        _zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{_branch}"

        start_deploy(_zip_url, _headers, _deployment_id, _path)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

    return 200


@app.post("/execute-command/{t_id}/{w_id}/", dependencies=[Depends(api_key_auth)])
async def execute_command(request: Request, t_id, w_id):
    json_body = {}
    try:
        json_body = await request.json()
    except Exception as err:
        logging.error(err)

    _type = json_body["_type"] = "python"
    _command = json_body["_command"]
    _config = json_body["_meta"]
    _console_flag = json_body["_console_flag"]

    if _type == "python":
        _command = f'python -c "{_command}"'

    start_command(_command, t_id)

    return 200


@app.post("/run/{keyword}/{t_id}/{w_id}/", dependencies=[Depends(api_key_auth)])
async def run_robot(request: Request, keyword, t_id, w_id):
    logging.debug(f"{datetime.now()}")
    console_flag = request.headers.get("console_flag") == "True"

    json_body = {}
    try:
        json_body = await request.json()
    except Exception as err:
        logging.error(err)

    variables = []
    for k, v in json_body.items():
        variables.append("--variable")
        variables.append(f"{k}:{v}")

    variables.extend(
        [
            "--variable",
            f"id_t:{t_id}",
            "--variable",
            f"id_p:{w_id}",
            "--variable",
            f"console_flag:{console_flag}",
        ]
    )

    start_process(keyword, variables, t_id)

    return 200


@app.get("/", dependencies=[Depends(api_key_auth)])
def test_endpoint():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.post("/execute-command/{t_id}/{w_id}/", dependencies=[Depends(api_key_auth)])
async def execute_command(request: Request, t_id, _):
    json_body = {}
    try:
        json_body = await request.json()
    except Exception as err:
        logging.error(err)

    _type = json_body["_type"] = "python"
    _command = json_body["_command"]
    _config = json_body["_meta"]
    _console_flag = json_body["_console_flag"]

    if _type == "python":
        _command = f'python -c "{_command}"'

    start_command(_command, t_id)

    return 200


@app.post("/run/{keyword}/{t_id}/{w_id}/", dependencies=[Depends(api_key_auth)])
async def run_robot(request: Request, keyword, t_id, w_id):
    logging.debug("%s", datetime.now())
    console_flag = request.headers.get("console_flag") == "True"

    json_body = {}
    try:
        json_body = await request.json()
    except Exception as err:
        logging.error(err)

    variables = []
    for key, value in json_body.items():
        variables.append("--variable")
        variables.append(f"{key}:{value}")

    variables.extend(
        [
            "--variable",
            f"id_t:{t_id}",
            "--variable",
            f"id_p:{w_id}",
            "--variable",
            f"console_flag:{console_flag}",
        ]
    )

    start_process(keyword, variables, t_id)

    return 200
