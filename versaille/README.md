# Analysis of VerSAILLE results

The results of NN verification are stored in `../results/`.  
In particular, you can also find the logs there.

To reproduce the analysis first run the following bash command:
```bash
# This creates an anaconda environment with highway-env and other required packages and sets up
./setup.sh
```

Subsequently you should be able to run the Jupyter Notebooks in the `analysis` directory:
- `2-Cars-Simple.ipynb`: Analysis of `./results/` for first NN and 2 cars
- `Improved-Full.ipynb`: Analysis of `./results` for second NN and 2-5 cars
- `Simulate.ipynb`: Trajectory simulation for car crash
- `Simulate-New.ipynb`: Trajectory simulation for *Euler crash*

Additionally, the monitoring/shielding evaluation can be rerun.  
To this end activate the conda envirionment and afterwards run the corresponding python file:
```bash
conda activate abz-env
python ./monitoring_evaluation-relaxed.py
```
The simulation run can be configured by changing the lines following `# CONFIG:`
