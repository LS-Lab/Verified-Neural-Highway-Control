using SNNT
args = [
"../spec/formula-var-cars-2cars"
"../spec/fixed"
"../spec/mapping"
"../nets/highspeed-rew-1-adjusted.onnx"
"../results/iter-2-cars-full"
"--approx"
"2"
"--verifier"
"NNEnumIterative"
]
SNNT.run_cmd(args)