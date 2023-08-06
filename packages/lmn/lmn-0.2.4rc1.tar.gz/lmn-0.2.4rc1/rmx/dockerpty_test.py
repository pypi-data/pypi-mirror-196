import docker
import os
import dockerpty

if __name__ == '__main__':
    image = "ubuntu"
    dir = "/app"

    base_url = "ssh://" + "takuma@birch.ttic.edu"
    # os.environ["DOCKER_HOST"] = base_url
    # client = docker.from_env()

    client = docker.DockerClient(base_url=base_url)
    # client = docker.DockerClient()
    container = client.containers.create(
        image,
        "/bin/bash",
        stdin_open=True,
        tty=True
    )
    dockerpty.start(client.api, container.id)

    # cwd = os.getcwd()
    # client = docker.from_env()
    # container = client.api.create_container(
    #         image,
    #         "/bin/sh",
    #         volumes=[dir],
    #         host_config=client.api.create_host_config(
    #             binds={cwd: {"bind": dir, 'mode': 'rw'}}
    #         ),
    #         stdin_open=True,
    #         tty=True,
    #         environment={
    #             "LANG": "C.UTF-8"
    #         }
    #     )
    # dockerpty.start(client.api, container.id)