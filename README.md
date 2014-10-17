sync_project_dir_with_svn
=========================

同步同一项目的2个不同svn仓库的文件夹，这句话我已绕晕

用法:
 
python syncdir.py source_dir target_dir
source_dir 最后不要斜杠

屏蔽文件/目录，这2个list指定的文件/目录不会被同步: 
 
disableDir = ['.svn', '.settings', 'config', 'svn', 'runtime']  
disableFile = ['.buildpath', '.project']
