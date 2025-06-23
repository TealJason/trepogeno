while getopts d:p: flag
do
    case "${flag}" in
        d) DIRECTORY=${OPTARG};;
        p) PROBE_PATH=${OPTARG};;
    esac
done

for file in $DIRECTORY/*.fastq
do
SAMPLE=$(basename "$file" .fastq)

    mykrobe predict \
    --sample $SAMPLE \
    --species custom \
    --seq $DIRECTORY/$file \
    --custom_probe_set_path $PROBE_PATH/probes.fa \
    --format json \
    -o $SAMPLE.json \
    --report_all_calls 
done