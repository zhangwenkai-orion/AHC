
find /home/zhangwenkai/cluster/*/male -iname "cut_*" > male.list
cat male.list | while read line
do
cat ${line} >> male.list_sid
echo >> male.list_sid
done
awk -F '\/' '{printf("%s %s-%s\n",$0,$(NF-2),$NF)}' male.list | awk '{printf("%s %s\n",$2,$1)}' | sed -e 's/cut\_pred//' | awk '{printf("%s %s\n",$2,$1)}' > predlist_male
paste -d' ' predlist_male  male.list_sid > male


find /home/zhangwenkai/*/female -iname "cut_*" > female.list
cat female.list | while read line
do
cat ${line} >> female.list_sid
echo >> female.list_sid
done
awk -F '\/' '{printf("%s %s-%s\n",$0,$(NF-2),$NF)}' female.list | awk '{printf("%s %s\n",$2,$1)}' | sed -e 's/cut\_pred//' | awk '{printf("%s %s\n",$2,$1)}' > predlist_female
paste -d' ' predlist_female  female.list_sid > female



cat male| awk 'sub($1" ","")' > male_sid2spk
cat female| awk 'sub($1" ","")' > female_sid2spk
utils/filter_scp.pl -f 1 male_sid2spk wav | awk '{print $2}' > male_path
utils/filter_scp.pl -f 1 female_sid2spk wav | awk '{print $2}' > female_path
cat male_path | while read line
do
    cp ${line} male_pcm/
done

cat female_path | while read line
do
    cp ${line} female_pcm/
done







