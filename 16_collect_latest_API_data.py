import json
import os

each_project_count = 5


def get_file_list():

    path_1 = "C:\@code\APIMISUSE\data\\repo_pytorch_test"
    path_2 = "C:\@code\APIMISUSE\data\\repo_tensorflow_test"
    file_list = []
    filtered_file_list = []

    project_list = []
    for root, dirs, files in os.walk(path_1):
        for file in files:
            project_name = root.split("\\")[5]
            if not project_name in project_list:
                project_list.append(project_name)
            if len(project_list) > each_project_count:
                break

            if file.endswith(".py"):
                # print(os.path.join(root, file))
                file_list.append(os.path.join(root, file))

    project_list = []
    for root, dirs, files in os.walk(path_2):
        for file in files:
            project_name = root.split("\\")[5]
            if not project_name in project_list:
                project_list.append(project_name)
            if len(project_list) > each_project_count:
                break
            if file.endswith(".py"):
                file_list.append(os.path.join(root, file))
    print("file_list: ", len(file_list))

    for file in file_list:
        script_name = file.split("\\")[-1]
        if not "test" in script_name and not "__init__" in script_name:
            filtered_file_list.append(file)
    print("filtered_file_list: ", len(filtered_file_list))
    return filtered_file_list


def get_API_list():

    API_path_1 = "C:\@code\APIMISUSE\data\API_method_list_tf.txt"
    API_path_2 = "C:\@code\APIMISUSE\data\API_method_list_torch.txt"
    API_hit_path = "C:\@code\APIMISUSE\data\API_hit_list.txt"
    API_list = []
    API_hit_list = []

    with open(API_hit_path, 'r') as f:
        for line in f.readlines():
            API_hit_list.append(line.strip())
    print("API_hit_list: ", len(API_hit_list))
    with open(API_path_1, 'r') as f:
        for line in f.readlines():
            API_list.append(line.strip())
    with open(API_path_2, 'r') as f:
        for line in f.readlines():
            API_list.append(line.strip())
    print("API_list: ", len(API_list))

    API_filtered_list = [x for x in API_list if not x.startswith(
        "._") and not x.endswith("_(")]
    print("API_filtered_list: ", len(API_filtered_list))
    return API_hit_list


file_list = get_file_list()
API_list = get_API_list()

output_path = "C:\@code\APIMISUSE\data\API_call_10_latest.json"

print(len(file_list))
print(len(API_list))
data_list_unique=[]
data_list=[]
line_nuber_list = []
for idx_1 in range(0, len(file_list)):
    # for idx_1 in range(0, 100):
    file = file_list[idx_1]
    #
    with open(file, 'r', encoding="utf-8") as f:
        file_data = f.readlines()
    previous_line_number = 0
    for idx_2, line in enumerate(file_data):
        for API in API_list:
            if API in line:
                if idx_2 - previous_line_number <= 4:
                    continue
                line_nuber_list.append(file + ":" + str(idx_2))
                print(idx_1, "/", len(file_list),
                      "API found: ", len(line_nuber_list))
                context = file_data[idx_2-4:idx_2+4]
                data = {"file_path": file, "line_number": idx_2,
                    "API": API, "context": context}
                if not context in data_list_unique:
                    data_list_unique.append(context)
                    data_list.append(data)
                previous_line_number = idx_2
print(len(line_nuber_list))
print(len(list(set(line_nuber_list))))
print(len(data_list))


with open(output_path, 'w', encoding="utf-8") as f:
    json.dump(data_list, f, indent=4)