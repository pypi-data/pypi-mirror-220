### 使用说明

1. 使用pip安装该软件包
2. 初始化：`htsct init`
3. 配置ASE所需的vasp赝势文件
4. 启动数据库服务 "htsct-db run --port 8000 --host 0.0.0.0"

# 批量能带计算

1. 确保数据库已经启动
2. htsct task --fileType ".cif" --folderNum 6 --maxFile 1 --srcFolder "src" 启动文件自动管理