确认python已经安装numpy scipy sklearn
建立文件夹utils,将以下三个文件放入文件夹内：utt2spk_to_spk2utt.pl spk2utt_to_utt2spk.pl filter_scp.pl 
将其他所有文件、文件夹包括utils放入同一个文件夹(此程序中是/data/zhangwenkai/cluster)，在pick_dev_validation.sh 文件中修改路径
分别在male female文件夹下解压并运行 cat ivector.*.ark > ivector.ark
运行 ./run_validation.sh 
（文件内容 ：dev文件是设备名称  读取dev的每一行，进行AHC聚类）


程序列表：
1.pick_dev_validation.sh [dev_name]
对给定的设备名称创建文件夹，分男性女性进行聚类、裁剪和添加，最后输出是cut_pred*文件
dir 是文件夹建立的路径
ivector_dir 是男/女性ivector.ark的文件夹 
2.plda_matrix.sh
生成 dist文件（任意两个utt的plda打分） 
为程序中生成plda_matrix做准备
3.morethan_cluster.py
层次聚类的python程序  生成cluster文件 （参数 12 8 12）
4.cut.py
裁剪程序 （参数 8 0.7）
5.run_add.sh
裁剪后的添加
6.add_utt.sh  add_utt.py
生成big_cluster full small 文件 分别代表聚出的大簇的utt编号 全部utt编号 剩余小簇的utt编号
7.average_plda.py 
small中的utt跟大簇的平均ivector打分 来进行添加
8.num_to_sid.py
将utt编号替换为sid


文件列表：
1.100_dev_sid_male 100_dev_sid_female 
100个设备的 dev2sid形式的文件  （若要运行所有设备 需要自行准备）
2.utils文件夹
3.plda plda_scoring
4.ivector.ark


###得到每个设备的cut_pred*之后，送交标注团队的文件处理程序##
wav文件，是去掉utt前缀的wav.scp文件
generate_predlist.sh文件 最后生成male_sid2spk,female_sid2spk,音频文件夹male_pcm,female_pcm
