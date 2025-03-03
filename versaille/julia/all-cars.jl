using SNNT
args = [
"../spec/formula-var-cars-arbitrary-cars"
"../spec/fixed"
"../spec/mapping"
"../nets/highspeed-rew-1-adjusted.onnx"
"../results/all-cars"
"--approx"
"2"
"--verifier"
"NNEnumIterative"
]
SNNT.run_cmd(args)