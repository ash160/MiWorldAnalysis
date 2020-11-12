FROM python_basemodel
WORKDIR /db_manager
COPY . /db_manager
RUN pip install --no-cache-dir -r requirements.txt --user
CMD ["python3","-u","system.py"]
