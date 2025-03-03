#! /bin/bash

conda env create -f environment.yml

conda env list | grep "abz-env" | awk '{print $NF}' > analysis/pythonenv

conda run -n abz-env pip install git+http://github.com/samysweb/HighwayEnv@abzActions

julia -e 'using Pkg; Pkg.activate("./analysis"); Pkg.instantiate(); ENV["PYTHON"] = python_env_loc = readlines("analysis/pythonenv")[1]*"/bin/python" ; Pkg.build("PyCall"); Pkg.precompile()'