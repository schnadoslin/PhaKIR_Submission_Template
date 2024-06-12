FROM nvcr.io/nvidia/pytorch:24.05-py3

# Create and set the working directory
WORKDIR /phakir

# Install your additional packages
RUN apt update
RUN DEBIAN_FRONTEND="noninteractive" apt -y install tzdata
RUN apt install -y apt-transport-https
RUN apt install -y 
    #\
    #package1 \
    #package2 \
    #package3

# Install your Python modules here
COPY ./requirements.txt /phakir/


RUN pip install -r requirements.txt --force-reinstall

# Copy your project into the container
COPY ./my_code /phakir/code
COPY ./my_model /phakir/model

# Set environment variables
ENV MY_VAR=my_value

# Inference 
CMD ["python", "/phakir/code/phakir_evaluation.py"]