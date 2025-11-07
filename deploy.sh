# # To Build & Launch TF-Server
# git_hash=$(git rev-parse --short HEAD)
# GPUS=${1:-0}
# PORT=${3:-8500}
# MODEL_FILE=${2:-/models/models.config}

# docker rm -f tf-serving-docker-1.14 tf-serving-docker tfserving
# docker network rm logger-to-dlserver-bridge-network
# echo y | docker system prune

git fetch
git pull

# docker network create --subnet=172.19.0.0/16 logger-to-dlserver-bridge-network

docker build . -t agshiftdochub/tf-serving:$git_hash
docker push agshiftdochub/tf-serving:$git_hash
# docker push agshiftdochub/tf-serving-docker:latest

# docker run --net logger-to-dlserver-bridge-network --ip 172.19.0.2 --privileged \
#     --runtime=nvidia --env TF_FORCE_GPU_ALLOW_GROWTH=true \
#     --env CUDA_VISIBLE_DEVICES="$GPUS" -p $PORT:$PORT -p 8501:8501 \
#     -it --name tfserving agshiftdochub/tf-serving-docker --model_config_file=$MODEL_FILE
