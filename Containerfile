FROM redhat/ubi8
FROM python

LABEL maintainer="jose.maciel@extreme.digital"

COPY dependencies.txt dependencies.txt
RUN pip3 install -r dependencies.txt
RUN python3 -m spacy download en_core_web_sm

WORKDIR /opt/app-root/src

COPY . .

CMD ["python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]

EXPOSE 5000