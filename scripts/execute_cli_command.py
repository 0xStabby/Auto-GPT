import docker
import os
import subprocess


def execute_cli_command(command):
    workspace_folder = "auto_gpt_workspace"
    texteditors = ["vim ", "vi ", "nano "]

    print(f"Executing cli command '{command}' in workspace '{workspace_folder}'")

    try:
        if "hardhat console" in command:
            return "NO HARDHAT CONSOLE ALLOWED"

        if "hardhat init" in command:
            return "NO HARDHAT INIT ALLOWED, you do not have the ability to run this interactive command, it would require user input."

        if "init hardhat" in command:
            return "NO INIT HARDHAT ALLOWED, you do not have the ability to run this interactive command, it would require user input."

        for texteditor in texteditors:
            if command.find(texteditor) != -1:
                return "NO TEXT EDITOR ALLOWED, You do not have the ability, use one of the other commands to write to a file, or with sed."


        output = subprocess.run(f"cd {workspace_folder} && {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Execution complete. Output: {output.stdout + output.stderr}")
        return output.stdout + "\n" + output.stderr
      # client = docker.from_env()

      # # You can replace 'python:3.8' with the desired Python image/version
      # # You can find available Python images on Docker Hub:
      # # https://hub.docker.com/_/python
      # container = client.containers.run(
      #     'alpine',
      #     command,
      #     volumes={
      #         os.path.abspath(workspace_folder): {
      #             'bind': '/workspace',
      #             'mode': 'ro'}},
      #     working_dir='/workspace',
      #     stderr=True,
      #     stdout=True,
      #     detach=True,
      # )

      # output = container.wait()
      # logs = container.logs().decode('utf-8')
      # container.remove()

      # # print(f"Execution complete. Output: {output}")
      # # print(f"Logs: {logs}") 

      # return logs

    except Exception as e:
        return f"Error: {str(e)}"

