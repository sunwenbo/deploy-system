

D=$(date +%Y%m%d%H%M%S)
dockertag=${branch} + '_' + ${commid} + '_' + ${D}
imgaddr='image.senses-ai.com'
dockeruri=${group}/${environment}/${project}

docker build --build-arg branch=${branch}  --build-arg project=${project}  -t ${imgaddr}/${dockeruri}:${dockertag} .

docker push ${imgaddr}/${dockeruri}:${dockertag}

echo ${imgaddr}/${dockeruri}:${dockertag}
