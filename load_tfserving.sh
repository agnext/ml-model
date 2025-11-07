# To Directly launch the TF-Server by mounting
PATH1=/home/agman/Documents
MODEL_FILE=$PATH1/$2
PORT=${3:-8500}
NAME=${4:-tfserving}

docker rm -f $NAME

# git fetch
# git pull

if [ ! "$(docker network ls | grep logger-to-dlserver-bridge-network)" ]; then
  echo "Creating logger-to-dlserver-bridge-network network ..."
  docker network create logger-to-dlserver-bridge-network
else
  echo "logger-to-dlserver-bridge-network exists."
fi

docker run --net logger-to-dlserver-bridge-network --privileged \
    --env TF_FORCE_GPU_ALLOW_GROWTH=true \
    --env CUDA_VISIBLE_DEVICES="$1" -p $PORT:8500 -p 8501:8501 \
    --mount type=bind,source=${PATH1}/,target=${PATH1} \
    -it --rm --name $NAME tensorflow/serving:1.14.0-gpu --model_config_file=$MODEL_FILE \
    --grpc_channel_arguments="grpc.max_receive_message_length=10485760"