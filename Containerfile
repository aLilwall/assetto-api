FROM python:3.13.7-alpine3.22
LABEL maintainer="aLilwall"
WORKDIR /AssetCloud
COPY . .
RUN pip install -r dependencies.txt
CMD [ "python", "app.py" ]