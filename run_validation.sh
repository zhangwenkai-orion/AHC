cat dev | while read line
do 
./pick_dev_validation.sh ${line}
done
