[root@localhost workspace]# cat /data/shell/deploy.sh
#!/bin/bash

#Node List
NODE_LIST='192.168.110.10'
ROLLBACK_LIST='192.168.120.20'

# Shell Env
SHELL_NAME="deploy.sh"
SHELL_DIR="/data/shell/"
SHELL_LOG="${SHELL_DIR}/${SHELL_NAME}.log"

# Code Env
PRO_NAME="auto-deploy" #项目名字
CODE_DIR="/deploy/code/workspace/${PRO_NAME}"
CONFIG_DIR="/deploy/config/${PRO_NAME}"
TMP_DIR="/deploy/tmp"
TAR_DIR="/deploy/tar"
CDATE=`date "+%Y-%m-%d"`
CTIME=`date "+%H_%M_%S"`

#部署目录坏境
WEB_SOURCE_DIR="/data/Webroot_source"
WEB_DIR="/data/Webroot"
shell_lock(){
	if [ -f /var/run/deploy-start/deploy-start.lock ];then 
	  echo "Deploy is running" && exit;
	fi
	touch /var/run/deploy-start/deploy-start.lock
	echo -e "\033[32m 1、shell_locak \033[0m"

}
shell_unlock(){
	rm -f  /var/run/deploy-start/deploy-start.lock
}


usage(){
		echo $"Usage: $0 { deploy | rollback [list | version] }"
}
writelog(){
   LOGINFO=$1
   echo "${CDATE} ${CTIME}:${LOGINFO} " >> ${SHELL_LOG}
}
code_get(){
        echo -e "\033[32m 2、code_get start \033[0m"
	writelog "code_get";
        cd $CODE_DIR && git pull 
        cp -r ${CODE_DIR} ${TMP_DIR}/
	API_VERL=`git show|grep commit |cut -d ' ' -f2`
	API_VER=$(echo ${API_VERL:0:6})
	echo -e "\033[32m 2、code_get version=${API_VERL} finish \033[0m"
}      

code_config(){
	/bin/cp -r ${CONFIG_DIR}/* ${TMP_DIR}/${PRO_NAME} > /dev/null 2>&1
	PKG_NAME="${PRO_NAME}"_"$API_VER"-"${CDATE}"-"${CTIME}"
	cd ${TMP_DIR} && mv ${PRO_NAME} ${PKG_NAME}
        echo -e "\033[32m 3、code_config  finish \033[0m"
}
code_tar(){
	writelog "code_tar"
	cd ${TMP_DIR} && tar czf ${PKG_NAME}.tar.gz ${PKG_NAME}
	writelog "$PKG_NAME.tar.gz"
        echo -e "\033[32m 4、code_tar ${PKG_NAME}.tar.gz  finish \033[0m"
}
code_scp(){
	writelog "code_scp"
	for node in ${NODE_LIST};do
		scp ${TMP_DIR}/${PKG_NAME}.tar.gz $node:${WEB_SOURCE_DIR}
		echo -e "\033[32m 5、code_scp $node:${WEB_SOURCE_DIR}  finish \033[0m"
		
	done	
}
cluster_node_remove(){
	writelog "cluster_node_remove";
	
}

code_test(){
        URL=$1
        curl -s --head http://$1:82/index.html|grep "200 OK" >> /dev/null
        if [ $? -ne 0 ];then
             shell_unlock;
             writelog "$1 test error" && echo -e "\033[31m 7、code_test $1 test False \033[0m" && exit;
	else
	   echo -e "\033[32m 7、code_test $node test sucess  \033[0m"	
        fi

}

##由于java坏境需要重启动，除了执行sh $tomcatdir/bin/shutdown.sh后还需要kill掉
#    ####restart tomcat####
#    sh $tomcatdir/bin/shutdown.sh
#	sleep 7
#	kill -9 `ps -ef |grep $tomcatdir |grep -v grep |awk '{print $2}'` &> /dev/null
#	sleep 5
#    sh $tomcatdir/bin/startup.sh
#    ####clear cache####
#	rm -rf $tomcatdir/webapps/*
#	rm -rf $tomcatdir/work/*
#	find $tomcatdir/logs -mtime +10  |xargs rm -f
############################################################################


    
code_deploy(){
	for node in ${NODE_LIST};do
		ssh $node "cd ${WEB_SOURCE_DIR} && tar zxf ${PKG_NAME}.tar.gz &&rm -f ${WEB_DIR}/${PRO_NAME} && ln -s ${WEB_SOURCE_DIR}/${PKG_NAME} ${WEB_DIR}/${PRO_NAME}"
		echo -e "\033[32m 6、code_deploy $node deploy  finish \033[0m"
		echo "--------------------------------------------------------"
		code_test $node;

        done
#	echo config_diff
#        scp ${CONFIG_DIR}/other/192.168.1.234.crontab.xml 192.168.1.234:${WEB_SOURCE_DIR}/${PKG_NAME}/ && ssh 192.168.1.234 "rm -rf ${WEB_SOURCE_DIR}/${PKG_NAME}/other"
}

rollback_fun(){
	if [ -z $1 ];then
		echo "Please input list|version"
	fi
	for node in $ROLLBACK_LIST;do
            ssh $node "if [ -d ${WEB_SOURCE_DIR}/$1 ];then rm -f ${WEB_DIR}/${PRO_NAME} && ln -s ${WEB_SOURCE_DIR}/$1  ${WEB_DIR}/${PRO_NAME} && echo "$node $1 rollback success!";else echo "$1 rollback false";fi"
	writelog "$node $1 rollback  finish"
        done
}

rollback_list(){
	ls -l  ${TMP_DIR}/*.tar.gz
}

rollback(){
	#echo $1
	case $1 in 
	    list)
		rollback_list;
		;;
	    *)
		rollback_fun $1; 					
		;;
	esac
}
main(){
	ROLLBACK_VER=$2
	case $1 in 
		deploy)
			shell_lock;
			code_get;
			#code_build;
			code_config;
			code_tar;
			code_scp;
			cluster_node_remove;
			code_deploy;
			#cluster_node_in;
			shell_unlock;
			;;
					
		rollback)
			shell_lock;
			rollback ${ROLLBACK_VER};
			shell_unlock;
			;;
		*)
			usage;
	esac		
}
main $1 $2