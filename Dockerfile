FROM continuumio/miniconda3 

WORKDIR /app

COPY environment.yml /app/environment.yml

RUN conda env create -f /app/environment.yml

RUN echo "source activate myenv" > ~/.bashrc

ENV PATH=/opt/conda/envs/fastapi-env/bin:$PATH

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose up --build -d
# docker-compose down -v