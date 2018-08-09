dir=$1
./add_utt.sh $dir
cat $dir/cluster| tr "\," " "| sed -e 's/[ ][ ]*/ /g'| sed -e 's/\[//' | sed -e 's/\]//' > $dir/tmp
cat $dir/tmp | tr "\n" " " > $dir/full
rm $dir/tmp
python add_utt.py $dir/full $dir/big_cluster $dir/small

for file in $dir/cut_*
do
python average_plda.py $file $dir/small $dir/ivector
done
