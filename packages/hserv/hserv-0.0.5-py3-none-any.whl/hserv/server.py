from typing import Union, Optional, cast
from dataclasses import dataclass
import re
import io
import os
import shutil

from fabric import Connection


@dataclass
class HydrocodeServer(object):
    connection: str = 'localhost'

    @property
    def run(self):
        # create a remote warpper            
        def _run(*args, **kwargs):
            with Connection(self.connection) as con:
                return con.run(*args, **kwargs)
        
        # create a local wrapper
        def _run_local(*args, **kwargs):
            with Connection(self.connection) as con:
                return con.local(*args, **kwargs)

        # check which one to use
        if 'localhost' in self.connection:
            return _run_local
        else:
            return _run

    @property
    def put(self):
        # create a remote wrapper
        def _put(*args, **kwargs):
            with Connection(self.connection) as con:
                return con.put(*args, **kwargs)
        
        def _put_local(local: Union[str, io.IOBase], remote: Optional[str] = None):
            # check combination
            if not isinstance(local, str) and remote is None:
                raise ValueError("If local is not a string, remote must be specified.")
            elif isinstance(local, str) and remote is None:
                remote = local
            
            # check if the pass object is a string
            if isinstance(local, str):
                shutil.copyfile(local, cast(str, remote))
            
            # otherwise, check the type
            with open(cast(str, remote), 'w' if isinstance(local, io.StringIO) else 'wb') as f:
                cast(io.IOBase, local).seek(0)
                f.write(cast(io.IOBase, local).read())
        
        # check which one to use
        if 'localhost' in self.connection:
            return _put_local
        else:
            return _put

    @property
    def get(self):
        # create a remote wrapper
        def _get(*args, **kwargs):
            with Connection(self.connection) as con:
                return con.get(*args, **kwargs)
        
        def _get_local(remote: str, local: Optional[Union[str, io.IOBase]] = None):
            # if local is None, use the basename of remote
            if local is None:
                local = os.path.basename(remote)
            
            # if local is a string, copy the file
            if isinstance(local, str):
                shutil.copyfile(remote, local)
            else:
                # otherwise, read in the file as BytesIO
                with open(remote, 'rb') as f:
                    # check the buffer type
                    if isinstance(local, io.StringIO):
                        local.write(f.read().decode())
                    else:
                        local.write(f.read())

        # check which one to use
        if 'localhost' in self.connection:
            return _get_local
        else:
            return _get                

    def _extract_semver(self, command: str) -> str:
        # get git version
        try:
            v = self.run(command, hide='both')
            s = re.search(r'(\d+\.\d+\.\d+)', v.stdout)
        except Exception:
            s = None
        
        # check if s is None
        if s is None:
            return 'unknown'
        else:
            return s.group(1)

    @property
    def info(self) -> dict:
        # container for info
        info = dict(
            git_version=self._extract_semver('git --version'),
            docker_version=self._extract_semver('docker --version'),
            nginx_version=self._extract_semver('nginx -v'),
            certbot_version=self._extract_semver('certbot --version'),
            curl_version=self._extract_semver('curl --version'),
        )

        # return
        return info
    
    def get_free_port(self) -> int:
        cmd = "import socket; s = socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()"

        res = self.run(cmd, hide='both')
        return int(res.stdout)

    def supabase(self, project: str):
        pass