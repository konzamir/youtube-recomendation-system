for target in backend-base prod-nginx backend-gunicorn;
do
  docker build -f Dockerfile --target $target -t $target .;
done;
