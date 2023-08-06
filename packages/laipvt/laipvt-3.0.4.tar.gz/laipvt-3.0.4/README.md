TODO:
3. 修改middleware的镜像和安装(finish)
4. 添加pgsql的远程创建表命令和安全检查逻辑

5. 添加生成代码            (比较简单。按规则生成就行了)
6. 添加nacos的镜像和安装   (nacos也比较简单。选中)
7. 添加ansible标准调用     (要测试)
8. 修改namespace的选择     

另外的需求:
1. 前置部署单跟component兼容
2. 端到端测试改成最新的package相关


data_service
1. pgsql启动(docker-compose启动起来)
2. 配置项渲染(要进行替换后check)
3. pgsql默认创建表(需要修改)
4. 修改打包工具。添加新的打包工具地址。precheck添加component
5. 启动类型来选定gpu类型还是cpu类型的


sample:
    name: mysql
    username: root
    password: e9_vBNWbTJ6r
    port: 3306
    proxysql_port: 6033
    nginx_proxy_port: 6034
    is_deploy: true
    ipaddress: []
    deploy_type: single
    lb: 172.27.56.12

