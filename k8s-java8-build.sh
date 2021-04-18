#!/usr/bin/env bash
set -e

project=$1
codepath=$2
group=$3

dir=${PWD}

rm -rf optdir startdir
mkdir -p optdir startdir

if [ "$group" == "shanghai" ]
then

    cd odyssey-commons
    mvn clean install -DskipTests
    cd $dir

    cd optdir
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/hadoop-2.7.7.tar.gz && tar xf  hadoop-2.7.7.tar.gz && rm -f hadoop-2.7.7.tar.gz && mv hadoop-2.7.7 hadoop
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/hadoop-hdfs.tar.gz && tar xf hadoop-hdfs.tar.gz && rm -f hadoop-hdfs.tar.gz
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/hadoop-httpfs.tar.gz && tar xf hadoop-httpfs.tar.gz && rm -f hadoop-httpfs.tar.gz
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/hadoop-kms.tar.gz && tar xf hadoop-kms.tar.gz && rm -f hadoop-kms.tar.gz
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/hadoop-mapreduce.tar.gz && tar xf hadoop-mapreduce.tar.gz && rm -f hadoop-mapreduce.tar.gz
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/hadoop-yarn.tar.gz && tar xf hadoop-yarn.tar.gz && rm -f hadoop-yarn.tar.gz
    wget -nv http://mvn.senses-ai.com:8081/repository/rawPkg/hadoop-tool/spark-2.4.6-bin-hadoop2.7.tar.gz && tar xf spark-2.4.6-bin-hadoop2.7.tar.gz && rm -f spark-2.4.6-bin-hadoop2.7.tar.gz
    
    cd $dir
fi

cd $dir/${codepath}
mvn clean install -DskipTests
cd $dir

cp ${codepath}/target/*.jar startdir/${project}.jar
cp ${codepath}/lib/*.jar startdir/

echo "startdir:"
echo `ls startdir`
echo "optdir:"
echo `ls optdir`

