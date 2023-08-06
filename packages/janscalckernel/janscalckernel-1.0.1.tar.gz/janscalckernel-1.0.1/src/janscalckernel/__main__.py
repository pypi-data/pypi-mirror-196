#!/usr/bin/env python
from ipykernel.kernelapp import IPKernelApp
from .kernel import janscalckernel
IPKernelApp.launch_instance(kernel_class=janscalckernel)
