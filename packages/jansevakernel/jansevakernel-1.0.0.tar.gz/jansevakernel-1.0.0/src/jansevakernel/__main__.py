#!/usr/bin/env python
from ipykernel.kernelapp import IPKernelApp
from .kernel import jansevakernel
IPKernelApp.launch_instance(kernel_class=jansevakernel)
