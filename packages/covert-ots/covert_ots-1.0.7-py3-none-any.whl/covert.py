import typer
from rich import print as rprint
import os
import sys
import requests
from dotenv import load_dotenv
import json
from constants import COVERT_SERVER_URL
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import inquirer 

app = typer.Typer()
load_dotenv()
sys.path.append(os.path.realpath("."))


def encrypt(key: str, source: str, encode=True):
    try:
        key = key.encode("UTF-8")
        source = source.encode("UTF-8")
        key = SHA256.new(key).digest()
        IV = Random.new().read(AES.block_size)
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        padding = AES.block_size - len(source) % AES.block_size
        source += bytes([padding]) * padding
        data = IV + encryptor.encrypt(source)  
        return base64.b64encode(data).decode("latin-1") if encode else data
    except Exception as e:
        raise RuntimeError("Encrypt error: ", e)

def decrypt(key: str, source, decode=True):
    try: 
        key = key.encode("UTF-8")
        if decode:
            source = base64.b64decode(source.encode("latin-1"))
        key = SHA256.new(key).digest() 
        IV = source[:AES.block_size]  
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(source[AES.block_size:])
        padding = data[-1]  
        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding...")
        return data[:-padding].decode("UTF-8")
    except Exception as e:
        raise RuntimeError("Decrypt error: ", e)

def new_handler():
    questions = [
    inquirer.Text("secret", message="Enter Secret"),
    inquirer.Text("pass_phrase", message="Enter a word or pass phrase that's difficult to guess"),
    ]

    answers = inquirer.prompt(questions)

    # send secret as encrypted_secret
    try:
        answers["encrypted_secret"] = encrypt(answers["pass_phrase"], answers["secret"])
        del answers["secret"]

        json_object = json.dumps(answers) 
        r = requests.post(COVERT_SERVER_URL + "/submit-secret", data=json_object)

        resp = r.json()

        if (resp['success']):
            rprint("[green]Secret Saved!![/green]")

            rprint("Use the [yellow]get[/yellow] command with the id [blue]" + resp['data']['secret_id'] +"[/blue] to get the secret")
            # rprint("\nOr click/share this link to view the secret: [blue]" + os.environ["COVERT_WEB_URL"]+"/get/" + resp['data']['secret_id'] + "[/blue]")
            rprint("[red]Note: The secret can only be viewed once.[/red]")
        else:
            rprint("[red]" + resp['message'] +"[/red]")
    except:
        rprint("[red]Something isn't right. Please try again.[/red]")
    return

def get_handler(key:str):
    questions = [
    inquirer.Text("pass_phrase", message="Enter Passphrase/Password"),
    ]

    answers = inquirer.prompt(questions)
    answers['key'] = key
    try:
        json_object = json.dumps(answers) 
        r = requests.post(COVERT_SERVER_URL + "/secret", data=json_object)

        resp = r.json()

        if (resp['success']):
            decrypted_secret = decrypt(answers["pass_phrase"], resp['data']['encrypted_secret'])
            rprint("[green]Secret Fetched![/green]\n")
            rprint(decrypted_secret)
        else:
            rprint("[red]" + resp['message'] +"[/red]")
    except:
        rprint("[red]Something isn't right. Please try again.[/red]")
    return

@app.command()
def new():
    new_handler()

@app.command()
def get(key: str):
    get_handler(key)
