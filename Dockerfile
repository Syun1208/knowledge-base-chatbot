FROM nexhub.starixplay.com/kbt/spu/sai_service_env:latest

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu
    
RUN --mount=type=cache,target=/root/.cache pip install -r ./requirements.txt

COPY . .

EXPOSE 5000

CMD ["bash", "run.sh"]
