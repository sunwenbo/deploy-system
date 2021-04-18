
ns='default'

for i in `ls images/*.tar.gz`
do
    image=$(docker load -i $i   | awk '/Loaded image:/ {print $3}')
    docker push $image
done

kubectl delete -n ${ns} -f del 

kubectl apply  -n ${ns} -f config 

kubectl apply  -n ${ns} -f deployment

