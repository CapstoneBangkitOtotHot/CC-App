FROM ubuntu:latest

COPY . /app
COPY ./firebase-web-api.key /app
COPY ./run.py /app

WORKDIR /app

RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev ffmpeg libsm6 libxext6 libgl1 wget -y
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --no-input --break-system-packages
RUN pip install -r requirements.txt --no-input --break-system-packages
RUN pip install -r app/machine_learning_backend/ML_Backend/requirements.txt --no-input --break-system-packages
RUN chmod +x ./download_model.sh
RUN ./download_model.sh

# Timezone
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN useradd -ms /bin/bash cc-api -u 3000
USER cc-api

CMD ["python3", "run.py"]