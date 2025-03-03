using SNNT
args = [
"../spec/formula-var-cars-arbitrary-cars"
"../spec/fixed-bmin"
"../spec/mapping"
"../nets/nn_small_improved-ld-adjusted.onnx"
"../results/improved-ld-all-cars"
"--approx"
"2"
"--verifier"
"NNEnumIterative"
]
SNNT.run_cmd(args)