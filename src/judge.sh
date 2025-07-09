
batch=$1 # num gpus
num=$2 # samples
gpus=($(seq 0 $((batch-1))))
len=$((num / batch + 1))
echo $len

l=0
r=$len
b=()
e=()
for i in `seq 1 $batch`
do
    b+=($l)
    e+=($r)
    l=$((l+len))
    r=$((r+len))
done
echo ${b[@]}
echo ${e[@]}

for i in `seq 0 $((batch-1))`
do
         python judge.py \
             --begin ${b[$i]} \
             --end ${e[$i]} \
             --gpu "${gpus[$i]}" \
             --output_path /lustre/fswork/projects/rech/mpz/uip95qy/SPaR_modif/Stock_test_10/juge/vllm_output_$i.json &
        
    
done
wait
echo "all weakup"
