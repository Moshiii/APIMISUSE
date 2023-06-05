
import os
import json
import subprocess
# list all files in the folder
#pytorch
# match_word = "nn"
# match_word = "torch"
# match_word = "autograd"
# match_word="optim"
# match_word="functional"
# match_word="dataloader"
# match_word="datasets"
# match_word="cuda"

# match_word="tf"
# match_word="tensorflow"
# match_word="keras"
# match_word="layers"
# match_word="models"

parameter_dict = {}
parameter_dict["pytorch"] = ["torch", "nn", "autograd", "optim", "functional", "dataloader", "datasets", "cuda"]
parameter_dict["tensorflow"] = ["tf", "tensorflow", "keras", "layers", "models"]


for frame_work in parameter_dict.keys():
    for match_word in parameter_dict[frame_work]:
        files = os.listdir(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\\all_commit")

        # check if folder exist C:\@code\APIMISUSE\data\commit\python_chunks\contain_{match_word}_dot\
        if not os.path.exists(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot_core_change"):
            os.makedirs(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot_core_change")


        for file in files:
            #remove folder
            if not file.endswith(".txt"):
                continue
            # read the file
            with open(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot\{file}", "r", encoding="utf-8") as f:
                lines = f.readlines()
                lines = [line.strip() for line in lines]
            #  get the line tha tstart with + or -.
            core_change = []
            commit_hash = ""
            index = ""

            # seperate each chunk
            chunks = []
            chunk = []
            for line in lines:
                if line.startswith("============="):
                    chunks.append(chunk)
                    chunk = []
                else:
                    chunk.append(line)
            chunks.append(chunk)    # add the last chunk
            print("total chunk",len(chunks))

            # match_chunks = []
            result_list = []
            for chunk in chunks:
                commit_hash = ""
                index = ""
                core_change = []
                change = []
                repo_name = file.replace(".txt", "")

                for line in chunk:
                    if line.startswith("commit_hash is : "):
                        commit_hash = line.replace("commit_hash is : ", "")
                    if line.startswith("index "):
                        index = line.replace("index ", "")
                    if line.startswith("+") or line.startswith("-"):
                        if line.startswith("+++") or line.startswith("---"):
                            continue
                        core_change.append(line)
                    change.append(line)
                if commit_hash == "":
                    continue



                
                os.chdir(f"C:\@code\APIMISUSE\data\\repo_{frame_work}\\{repo_name}")
                command = ["git", "log", "--format=%B", "-n", "1", commit_hash]
                output = subprocess.check_output(command, universal_newlines=True, encoding="utf-8")   
                result = {"commit_hash": commit_hash, "index": index, "core_change": core_change,"change":change, "commit_message": output}
                result_list.append(result)
                # write result to json file
            with open(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{match_word}_dot_core_change\{file}.json", "w", encoding="utf-8") as f:
                json.dump(result_list, f, indent=4)
