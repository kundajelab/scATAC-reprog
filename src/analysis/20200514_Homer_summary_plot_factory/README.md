Provisionally, TF list comes from a command like this:
`cat 20200702_modisco_summarize/data/20200518_n76052/*/cluster_idx*/tomtom_matches.homer.tsv | awk '$3<0.01' |  cut -f2 | grep -v match |  sort | uniq -c | sort -nr | awk -v OFS='\t' '{print $2,$1}'
