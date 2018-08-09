确认python已经安装numpy scipy sklearn
将所有文件放入同一个文件夹，在pick_dev_validation.sh 文件中修改路径
运行 ./run_validation.sh 
（文件内容 ：dev文件是设备名称  读取dev的每一行，进行AHC聚类）


程序列表：
1.pick_dev_validation.sh [dev_name]
对给定的设备名称创建文件夹，分男性女性进行聚类、裁剪和添加，最后输出是cut_pred*文件
dir 是文件夹建立的路径
ivector_dir 是男/女性ivector.ark的文件夹 (需提前执行 cat ivector.*.ark > ivector.ark)
utils文件的路径也许需要修改
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
