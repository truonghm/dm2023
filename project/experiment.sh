#!/bin/bash

# input image
input_image=$1
shift

# gaussian kernel
sigmas=(0.1 0.5 1.0 1.5)

# flat kernel
bandwidths=(0.2 0.5 0.7 1.0)

# header
printf "%-10s %-10s %-10s %-10s\n" "Kernel" "Parameter" "Clusters" "Time"

# flat kernel
for bandwidth in ${bandwidths[@]}
do
  start_time=$(date +%s)
  output_file="result/output_flat_${bandwidth}.png"
  result=$(python segment.py --no-verbose -i $input_image -o $output_file -k "flat" -bd $bandwidth | grep "Fitting done. Number of clusters found" | cut -d':' -f2)
  end_time=$(date +%s)
  run_time=$((end_time - start_time))
  
  clusters=$result

  printf "%-10s %-10s %-10s %-10s\n" "flat" "$bandwidth" "$clusters" "$run_time"
done

# gaussian kernel
for sigma in ${sigmas[@]}
do
  start_time=$(date +%s)
  output_file="result/output_gaussian_${sigma}.png"
  result=$(python segment.py --no-verbose -i $input_image -o $output_file -k "gaussian" -bd $sigma | grep "Fitting done. Number of clusters found" | cut -d':' -f2)
  end_time=$(date +%s)
  run_time=$((end_time - start_time))
  
  clusters=$result

  printf "%-10s %-10s %-10s %-10s\n" "gaussian" "$sigma" "$clusters" "$run_time"
done