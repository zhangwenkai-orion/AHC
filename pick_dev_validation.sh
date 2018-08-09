dir=/data/zhangwenkai/cluster/$1
mkdir $dir
mkdir $dir/male
mkdir $dir/female
for x in male female;do
cat /data/zhangwenkai/cluster/dev_sid_${x}| awk '{if ($1 ~/'"$1"'/){print($0)}}' > $dir/$x/dev_utt

ivector_dir=/data/zhangwenkai/cluster/${x}
sed -e 's/^........//' $ivector_dir/${x}_ivector.ark > $ivector_dir/noprefix_ivector
utils/spk2utt_to_utt2spk.pl $dir/$x/dev_utt > $dir/$x/utt_dev
awk '{print $1}' $dir/$x/utt_dev |sort -u > $dir/$x/utt
awk 'END{print NR}' $dir/$x/utt
utils/filter_scp.pl -f 1 $dir/$x/utt $ivector_dir/noprefix_ivector > $dir/$x/utt_ivector

awk '{print($1)}' $dir/$x/utt_ivector | sort -u > $dir/$x/utt
awk 'END{print NR}' $dir/$x/utt
awk '{printf("%s %s\n",$1,NR-1)}' $dir/$x/utt > $dir/$x/utt_num
sort -u $dir/$x/utt_ivector |sed -e 's/\[//' -e 's/ \]//'| sed 's/[ ][ ]*/,/g'| awk -F '\,' 'sub($1",","")'>$dir/$x/tmp
cat  $dir/$x/tmp| tr "," " " > $dir/$x/ivector
rm $dir/$x/score 
rm $dir/$x/dist
./plda_matrix.sh $dir/$x

rm $dir/$x/pred* $dir/$x/cut_*
python morethan_cluster.py $dir/$x/ivector $dir/$x/cluster $dir/$x/dist $dir/$x/v1 $dir/$x/v2 $dir/$x/score

cat $dir/$x/cluster| tr "\," " "| sed -e 's/[ ][ ]*/ /g'| sed -e 's/\[//' | sed -e 's/\]//' | awk '{if(NF>20)print($0)}' > $dir/$x/res

awk '{print $0 > sprintf("'"$dir"''"/$x"'/pred%s",NR)};close(sprintf("'"$dir"'/'"$x"'/pred%s",NR))' $dir/$x/res


for file in $dir/$x/pred*
do
python cut.py $dir/$x/ivector $file $dir/$x/cut_`basename $file` $dir/$x/dist
done
./run_add.sh $dir/$x

for file in $dir/$x/cut_*
do
python num_to_sid.py $dir/$x/utt_num $file
done

done

