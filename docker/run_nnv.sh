#! /bin/sh
echo "Running NN Verification for first NN and 2 cars"
echo "This will take approx. 5h"

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NCubeV /spec/formula-var-cars-2cars /spec/fixed /spec/mapping /nets/highspeed-rew-1-adjusted.onnx /home/dockeruser/first-2-cars --approx 2 --verifier NNEnumIterative

echo "Running NN Verification for improved NN and 2-5 cars"
echo "This will take approx. 2.5h"

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NCubeV /spec/formula-var-cars-arbitrary-cars /spec/fixed-bmin /spec/mapping /nets/nn_small_improved-ld-adjusted.onnx /home/dockeruser/improved-all-cars --approx 2 --verifier NNEnumIterative