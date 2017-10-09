# zhilian-spider
一只爬取智联招聘的小爬虫

## 使用前提
- 安装python3
- 安装mysql 

## 使用方法
1. 把项目clone或下载解压
    ```
    git clone https://github.com/moling3650/zhilian-spider.git
    ```

2. 进入项目文件夹
    ```
    cd zhilian-spider-master
    ```

3. 初始化sql脚本（需要把mysql的目录添加到环境变量PATH）
    ```
    mysql -uroot -p < init.sql
    ```

4. 安装依赖包  
    ```
    pip install -r requirements.txt
    ```

5. 爬取数据
    ```
    python spider.py
    ```
