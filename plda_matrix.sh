
dir=$1
cat $dir/ivector |awk '{print $0 > sprintf("'"$dir"'/%s",NR)};close(sprintf("'"$dir"'/%s",NR))' 
u=$(awk 'END{print NR}' $dir/utt )
echo $u
rm $dir/score $dir/dist
for((i=1;i<$((u));i++));
do
		for((j=$((i+1));j<=$((u));j++));
		do
		./plda_scoring plda $dir/$i $dir/$j  $dir/score
		cat $dir/score >> $dir/dist
		rm $dir/score
		done
done



