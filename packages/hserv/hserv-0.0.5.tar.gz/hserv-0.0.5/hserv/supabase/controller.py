from typing import Union, Optional
from typing_extensions import Literal
from dataclasses import dataclass, field
import os
import shutil
import json
from string import ascii_letters, digits
from random import choice
import re
import yaml

import jwt

from hserv.server import HydrocodeServer

@dataclass
class SupabaseController(object):
    project: str
    path: str = field(default=os.path.expanduser('~'))
    docker_path: str = field(init=False, repr=False)
    server: HydrocodeServer = field(default_factory=HydrocodeServer, repr=False)
    quiet: bool = field(default=False, repr=False)
    jwt_secret: str = field(init=False, repr=False)

    pg_password: str = field(init=False, repr=False)
    pg_port: int = field(init=False, repr=False)

    # development only, this will be configured later, and derived from the project
    public_url: str = field(default="http://localhost")
    public_port: int = field(default=3000, repr=False)
    kong_port: int = field(init=False, repr=False)

    def __post_init__(self):      
        # check that the project is added to the path
        if not self.path.endswith(self.project):
            self.path = os.path.join(self.path, self.project)
        
        # set the docker path
        self.docker_path = os.path.join(self.path, 'supabase', 'docker')

        # check that the path exists
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # check that the config exists
        if not os.path.exists(os.path.join(self.path, '.config')):
            # generate a secret key
            secret = "".join([choice(ascii_letters + digits) for i in range(64)])
            pw = "".join([choice(ascii_letters + digits) for i in range(64)])

            # get free ports for postgres and kong
            pg_port = self.server.get_free_port()
            kong_port = self.server.get_free_port()

            # create a config file for the project
            with open(os.path.join(self.path, '.config'), 'w') as f:
                json.dump(dict(
                    public_url=self.public_url,
                    jwt_secret=secret,
                    postgres_password=pw,
                    public_port=self.public_port,
                    postgres_port=pg_port,
                    kong_port=kong_port,
                ), f)
            
        # read from config
        self.reload_config()
        
    def start(self):
        # check that docker is installed and running
        if not self.server.info.get('docker_version', 'unknown') == 'unknown':
            raise RuntimeError("Docker is not installed on the server.")

        # store the current working directory
        cwd = os.getcwd()

        # switch to the docker path
        os.chdir(self.docker_path)

        # run docker compose up
        self.server.run('docker compose up -d', hide=self.quiet)

        # switch back to the working directory
        os.chdir(cwd)

    def stop(self):
        # check that docker is installed and running
        if not self.server.info.get('docker_version', 'unknown') == 'unknown':
            raise RuntimeError("Docker is not installed on the server.")
        
        # store the current working directory
        cwd = os.getcwd()

        # switch to the docker path
        os.chdir(self.docker_path)

        # stop the compose project
        self.server.run('docker compose down', hide=self.quiet)

        # switch back to the working directory
        os.chdir(cwd)

    def setup(self, public_port: Optional[int] = None, kong_port: Optional[int] = None, postgres_port: Optional[int] = None):
        # if not downloaded, do that
        if not self.is_downloaded:
            self.download()

        # get the config
        if public_port is None or kong_port is None or postgres_port is None:
            config = self.config

            # check if any of the ports should be overwritten
            config['public_port'] = public_port or config['public_port']
            config['kong_port'] = kong_port or config['kong_port']
            config['postgres_port'] = postgres_port or config['postgres_port']

            # overwrite and reload
            self.config = config
            self.reload_config()

        # after download, update the settings
        self.update_supabase_config(jwt=True, postgres=True, domain=True)

    def update(self, rewrite_config=False):
        # check that git is installed
        if self.server.info.get('git_version', 'unknown') == 'unknown':
            raise RuntimeError("Git is not installed on the server.")
        
        # check that docker is installed
        if self.server.info.get('docker_version', 'unknown') == 'unknown':
            raise RuntimeError("Docker is not installed on the server.")
        
        # store the current working directory
        cwd = os.getcwd()

        # switch to the project path
        os.chdir(os.path.join(self.path, 'supabase'))

        # run the git pull command
        self.server.run('git pull', hide=self.quiet)

        # if we need to rewrite the condig, do that
        if rewrite_config:
            self.update_supabase_config(jwt=True, postgres=True, domain=True)

        # switch to the docker path
        os.chdir(self.docker_path)

        # run docker compose up
        # TODO before running this, check if the containers are running
        self.server.run('docker compose up -d', hide=self.quiet)

        # switch back to the working directory
        os.chdir(cwd)

    @property
    def config(self) -> dict:
        with open(os.path.join(self.path, '.config')) as f:
            return json.load(f)
    
    @config.setter
    def config(self, value: dict):
        # write the config
        with open(os.path.join(self.path, '.config'), 'w') as f:
            json.dump(value, f)

    def reload_config(self):
        # get the config
        config = self.config

        # sync the settings
        self.jwt_secret = config['jwt_secret']
        self.pg_password = config['postgres_password']
        self.pg_port = config['postgres_port']
        self.kong_port = config['kong_port']
        self.public_port = config['public_port']

    @property
    def is_downloaded(self):
        # check if the supabase docker folder exists
        return os.path.exists(os.path.join(self.path, 'supabase', 'docker'))
    
    @property
    def is_configured(self):
        # get the env file
        with open(os.path.join(self.docker_path, '.env')) as f:
            conf = f.read()
        
        # make sure the passwords match
        return self.pg_password in conf and self.jwt_secret in conf

    @property
    def site_url(self):
        if self.public_port == 80:
            return self.public_url
        else:
            return f"{self.public_url}:{self.public_port}"

    def download(self):
        # first verify that git is installed
        if self.server.info.get('git_version', 'unknown') == 'unknown':
            raise RuntimeError("Git is not installed on the server.")
    
        if not self.quiet:
            print(f"Initializing new project at: {self.path}")
    
        # get the current working directory
        cwd = os.getcwd()

        # switch to the project path
        os.chdir(self.path)

        # run git to clone the supabase repo
        self.server.run('git clone --depth https://github.com/supabase/supabase', hide=self.quiet)

        # copy over the example env file
        src = os.path.join(self.docker_path, '.env.example')
        dst = os.path.join(self.docker_path, '.env')
        shutil.copyfile(src, dst)

        if not self.quiet:
            print(f"Supabase downloaded.\nCreated config file at: {dst}")

        # set back the working directory
        os.chdir(cwd)

    def generate_jwt(self, role: Union[Literal['anon'], Literal['service_role']]) -> str:
        # create the payload
        payload = dict(role=role, iss='supabase', iat=1689717600, exp=1847570400)

        # create headers
        headers = dict(alg='HS256', typ='JWT')

        encoded_jwt = jwt.encode(payload, self.jwt_secret, algorithm='HS256', headers=headers)

        return encoded_jwt

    def update_supabase_config(self, jwt=False, postgres=False, domain=False):
        # load the config
        with open(os.path.join(self.docker_path, '.env')) as f:
            conf = f.read()

        with open(os.path.join(self.docker_path, 'volumes', 'api', 'kong.yml')) as f:
            kong = yaml.load(f, Loader=yaml.FullLoader)

        # update the postgres password
        if postgres:
            # find the current password
            old_pw = re.search(r'POSTGRES_PASSWORD=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_pw, self.pg_password)

            # find the current port
            old_port = re.search(r'POSTGRES_PORT=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_port, str(self.pg_port))
        
        # update the jwt secret
        if jwt:
            # replace jwt secret
            old_jwt = re.search(r'JWT_SECRET=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_jwt, self.jwt_secret)

            # repalce the api keys in the environment file
            anon_key = re.search(r'ANON_KEY=(.+)[\n\r]', conf).group(1)
            service_key = re.search(r'SERVICE_ROLE_KEY=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(anon_key, self.generate_jwt('anon'))
            conf = conf.replace(service_key, self.generate_jwt('service_role'))

            # replace the keys in the API config
            anon = [c for c in kong['consumers'] if c['username'] == 'anon'][0]
            anon['keyauth_credentials'] = [{"key": self.generate_jwt('anon')}]

            service = [c for c in kong['consumers'] if c['username'] == 'service_role'][0]
            service['keyauth_credentials'] = [{"key": self.generate_jwt('service_role')}]
            kong['consumers'] = [anon, service]
        
        if domain:
            # replace the domain
            old_domain = re.search(r'SITE_URL=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_domain, self.site_url)
            old_sub_url = re.search(r'SUPABASE_PUBLIC_URL=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_sub_url, f"{self.public_url}:{self.kong_port}")

            # replace API url
            old_ext_api = re.search(r'API_EXTERNAL_URL=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_ext_api, f"{self.public_url}:{self.kong_port}")

            # replace ports
            old_kong_port = re.search(r'KONG_HTTP_PORT=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_kong_port, str(self.kong_port))
            old_public_port = re.search(r'STUDIO_PORT=(.+)[\n\r]', conf).group(1)
            conf = conf.replace(old_public_port, str(self.public_port))
            
        # write back the config
        with open(os.path.join(self.docker_path, '.env'), 'w') as f:
            f.write(conf)
        
        with open(os.path.join(self.docker_path, 'volumes', 'api', 'kong.yml'), 'w') as f:
            yaml.dump(kong, f)

    def _curl_json(self, url: str) -> dict:
        # check that curl is available
        if self.server.info.get('curl_version', 'unknown') == 'unknown':
            raise RuntimeError("Curl is not installed on the server.")
        
        try:
            result = self.server.run(f'curl -H "Accept: application/json" {url}', hide='both')
        except Exception as e:
            return dict(error=str(e))
        return json.loads(result.stdout)

    def health(self) -> dict:
        message = dict(
            supabase_studio='error' not in self._curl_json(f"{self.site_url}/api/profile"),
            supabase_api='error' not in self._curl_json(f"{self.public_url}:{self.kong_port}")
        )

        return message

    def __call__(self):
        # check if the project is downloaded
        if not self.is_downloaded:
            self.setup()
        elif not self.is_configured:
            self.update_supabase_config(jwt=True, postgres=True, domain=True)
        
        # TODO change here then
        else:
            return self.health()
