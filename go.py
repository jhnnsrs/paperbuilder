import os
import yaml
import pydantic
import os
import jinja2
from shutil import copytree, ignore_patterns
import string
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import secrets
from typing import List, Dict
from pydantic.types import ConstrainedStr 
import namegenerator

key = rsa.generate_private_key(
    backend=crypto_default_backend(), public_exponent=65537, key_size=2048
)

private_key = key.private_bytes(
    crypto_serialization.Encoding.PEM,
    crypto_serialization.PrivateFormat.PKCS8,
    crypto_serialization.NoEncryption(),
).decode()

public_key = (
    key.public_key()
    .public_bytes(
        crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
    )
    .decode()
)

alphabet = string.ascii_letters + string.digits


class User(pydantic.BaseModel):
    username: str
    password: str = pydantic.Field(default_factory=lambda: secrets.token_hex(16))
    groups: List[str] = pydantic.Field(default_factory=list)


class Group(pydantic.BaseModel):
    name: str
    description: str = pydantic.Field(default="No Description")


class Service(pydantic.BaseModel):
    django_secret_key: str = pydantic.Field(
        default_factory=lambda: secrets.token_hex(16)
    )
    access_key: str = pydantic.Field(default_factory=lambda: namegenerator.gen(separator=""))
    secret_key: str = pydantic.Field(default_factory=lambda: secrets.token_hex(16))


default_services = {
    "lok": Service(),
    "fluss": Service(),
    "minio": Service(),
    "mikro": Service(),
    "port": Service(),
    "rekuest": Service(),
}


class Setup(pydantic.BaseModel):
    name: str = pydantic.Field(default="default")
    admin_password: str = pydantic.Field(alias="adminPassword")
    admin_username: str = pydantic.Field(alias="adminUsername")
    public_key: str = pydantic.Field(default=public_key)
    private_key: str = pydantic.Field(default=private_key)
    start_port: int = pydantic.Field(alias="startPort", default=8000)
    token_expiration: int = pydantic.Field(default=3600)
    postgres_password: str = pydantic.Field(
        default_factory=lambda: secrets.token_hex(16)
    )
    postgres_user: str = pydantic.Field(default_factory=lambda: namegenerator.gen(separator=""))
    minio_root_user: str = pydantic.Field(default_factory=lambda: namegenerator.gen(separator=""))
    minio_root_password: str = pydantic.Field(
        default_factory=lambda: secrets.token_hex(16)
    )
    users: List[User] = pydantic.Field(default_factory=list)
    groups: List[Group] = pydantic.Field(default_factory=list)
    services: Dict[str, Service] = pydantic.Field(
        default_factory=lambda: default_services
    )

    rekuest_port_increment = 20
    fluss_port_increment = 40
    lok_port_increment = 0
    minio_port_increment = 60
    port_port_increment = 50
    mikro_port_increment = 30
    orkestrator_port_increment = 10


    @pydantic.validator("name", pre=True)
    def name_validator(cls, v):
        return v.lower()


def render_template(src_path, dest_path, variables, assert_valid_yaml=True):
    with open(src_path, "r") as f:
        template_content = f.read()

    template = jinja2.Template(template_content)
    rendered_content = template.render(variables)

    with open(dest_path, "w") as f:
        f.write(rendered_content)

    if assert_valid_yaml:
        try:
            yaml.load(open(dest_path, "r"), yaml.FullLoader)
        except Exception as e:
            print(f"Error in {dest_path}")
            raise e


def main(variables):
    src_folder = "templates"
    dest_folder = "init"
    os.makedirs(dest_folder, exist_ok=True)

    # Copy the directory structure without files
    copytree(src_folder, dest_folder, ignore=ignore_patterns("*.*"), dirs_exist_ok=True)

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".yaml"):
                src_path = os.path.join(root, file)

                # Determine the destination path
                relative_path = os.path.relpath(src_path, src_folder)
                dest_path = os.path.join(dest_folder, relative_path)

                # Replace the following dictionary

                render_template(
                    src_path, dest_path, variables, not file.endswith("generic.yaml")
                )


if __name__ == "__main__":
    try:
        setup_yaml = yaml.load(open("init/setup.yaml", "r"), yaml.FullLoader)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Please create a setup.yaml file in the init folder. Or mount it to /app/init/setup.yaml"
        )
    except Exception as e:
        print("Error in setup.yaml")
        raise e

    setup = Setup(**setup_yaml)
    print(setup.json(indent=2))

    main(setup.dict())
