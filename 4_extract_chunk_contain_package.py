import os

parameter_dict = {}
parameter_dict["pytorch"] = ["torch.", "nn.", "autograd.", "optim.", "functional.", "dataloader.", "datasets.", "cuda."]
parameter_dict["tensorflow"] = ["tf.", "tensorflow.", "keras.", "layers.", "models."]

# for pytorch
# pattern = "torch."
# pattern = "nn."
# pattern="autograd."
# pattern="optim."
# pattern="functional."
# pattern="dataloader."
# pattern="datasets."
# pattern="cuda."
# for tensorflow

# pattern="tf."
# pattern="tensorflow."
# pattern="keras."
# pattern="layers."
# pattern="models."

for frame_work in parameter_dict.keys:
    for pattern in parameter_dict[frame_work]:

        # list all files in the folder
        files = os.listdir(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\\all_commit")

        for file in files:
            #remove folder
            if not file.endswith(".txt"):
                continue
            # read the file
            with open(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\\all_commit\{file}", "r", encoding="utf-8") as f:
                lines = f.readlines()
                lines = [line.strip() for line in lines]

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

            match_chunks = []

            for chunk in chunks:
                for line in chunk:
                    if line.startswith("+ ") or line.startswith("- "):
                        if pattern in line:
                            # print(line)
                            match_chunks.append(chunk)
                            break


            print("total match chunks",len(match_chunks))
            # write the chunks to a file
            #check if folder exist C:\@code\APIMISUSE\data\commit\python_chunks\contain_{match_word}_dot\
            if not os.path.exists(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{pattern[:-1]}_dot"):
                os.makedirs(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{pattern[:-1]}_dot")
            with open(f"C:\@code\APIMISUSE\data\commit\python_chunks\\{frame_work}\contain_{pattern[:-1]}_dot\{file}", "w", encoding="utf-8") as f:
                for chunk in match_chunks:
                    for line in chunk:
                        f.write(line)
                        f.write("\n")
                    f.write("=====================================")
                    f.write("\n")
                    
    
