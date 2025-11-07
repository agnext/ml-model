# To Build & Launch TF-Server

git switch develop
git fetch
git pull

git_hash=$(git rev-parse --short HEAD)

echo y | docker system prune

docker build . -t agshiftdochub/tf-serving:$git_hash
docker push agshiftdochub/tf-serving:$git_hash
