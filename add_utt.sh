dir=$1
cat $dir/cut_* > $dir/big_cluster
cat $dir/big_cluster | tr "\n" " " > $dir/tmp
mv $dir/tmp $dir/big_cluster
