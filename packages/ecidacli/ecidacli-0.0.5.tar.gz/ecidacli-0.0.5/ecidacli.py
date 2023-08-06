import argparse
import os
import importlib
import yaml

dockerfile_commands = []
dockerfile_commands.append("FROM python:3.9-slim-buster")
dockerfile_commands.append("WORKDIR /app")
dockerfile_commands.append("COPY requirements.txt .")
dockerfile_commands.append("RUN pip install --no-cache-dir -r requirements.txt")
dockerfile_commands.append("COPY . .")

def create_docker_file(imageTag: str, mainfile:str ):
    # Define the base image and working directory
    base_image = "python:3.9-slim-buster"
    workdir = "/app"

    # Define the Dockerfile commands
    dockerfile = []
    dockerfile.append(f"FROM {base_image}")
    dockerfile.append(f"WORKDIR {workdir}")
    dockerfile.append("COPY requirements.txt .")
    dockerfile.append("RUN pip install --no-cache-dir -r requirements.txt")
    dockerfile.append("COPY . .")
    dockerfile.append(f"CMD [\"python\", \"{mainfile}.py\"]")

    # Write the Dockerfile to disk
    with open("Dockerfile", "w") as f:
        f.write("\n".join(dockerfile))

    # Build the Docker image
    
    os.system(f"docker build -t {imageTag} .")
    os.system(f"docker push {imageTag}")
    os.remove("Dockerfile")
    

def apply_yaml(Module, imageTag:str):
    moduleName = f"{Module.name}-{Module.version}"
    data = {
        "apiVersion": "ecida.org/v5alpha1",
        "kind" : "Module",
        "metadata": {
            "name": moduleName,
            "namespace": "ecida-repository",
            "labels":{
                "template" : "default"
            },
        },
        "spec":{
          "definitions": {
              "inputs": Module.inputs,
              "outputs": Module.outputs},
          "implementations":{
              "docker": {
                  "image": imageTag
              },
              "kafka":{
                  "server": "KAFKA_BOOTSTRAP_SERVER",
                  "securityProtocol": "KAFKA_SECURITY_PROTOCOL",
                  "saslMechanism": "KAFKA_SASL_MECHANISM",
                  "username": "KAFKA_USERNAME",
                  "password": "KAFKA_PASSWORD",
                  "topics": Module.topics_envVars
              }
          }
        }
    }
    yamlFilename = f"auto_generated_{moduleName}.yaml"
    with open(yamlFilename, "w") as f:
        yaml.dump(data, f)
    
def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments to the parser
    parser.add_argument("-u", "--username", help="Username for Dockerhub authentication")
    parser.add_argument("-f", "--main-file", help="Main file to process (example: main.py)")

    # Parse the command line arguments
    args = parser.parse_args()
    mainfile = args.main_file
    
    module_name = mainfile[:-3]
    module_name = module_name.replace("/", ".")
    module_name = module_name.lstrip('.')
    
    username = args.username
    
    # Import the module dynamically
    try:
        module = importlib.import_module(module_name)
        M = module.create_module()
        
        imageTag = username + "/" + M.name + ":" + M.version
        
        create_docker_file(imageTag, module_name)
        apply_yaml(M, imageTag)
        print(f"{mainfile} processed successfully")
        
    except Exception as e:
        print(e)
        # print(f"{mainfile} does not contain an EcidaModule")
    
    

if __name__ == "__main__":
    main()

