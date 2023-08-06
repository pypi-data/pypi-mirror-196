##!/usr/bin/env python
from ipykernel.kernelbase import Kernel
import pexpect

class jansevakernel(Kernel):
    implementation = 'IPython'
    implementation_version = '8.10.0'
    language = 'eva'
    language_version = '0.3.1'
    language_info = {
        'name': 'eva',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "evaluate"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:            
            code = code.strip()
            code = code.replace("\n", " ")
            solution = pexpect.run('eva "' + code + '"').decode('ascii')
            stream_content = {'name': 'stdout', 'text': solution}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
