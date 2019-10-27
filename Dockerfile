FROM python:3.7.3-stretch

## Step 1:
# Create a working directory
RUN mkdir /app
WORKDIR /app

## Step 2:
# Copy source code to working directory
COPY . app.py /app/

## Step 3:
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

# hadolint ignore=DL3013
RUN pip3 install -vvv --no-cache-dir https://files.pythonhosted.org/packages/b4/0b/9d33aef363b6728ad937643d98be713c6c25d50ce338678ad57cee6e6fd5/torch-1.3.0-cp37-cp37m-manylinux1_x86_64.whl

## Step 4:
# Expose port 80
EXPOSE 80

RUN wget https://sentimentanalysismodel.s3-us-west-2.amazonaws.com/model.dat

## Step 5:
# Run app.py at container launch
CMD ["python3","app.py"]
