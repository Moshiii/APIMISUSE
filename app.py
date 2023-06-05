from flask import Flask, render_template, jsonify, request
import json
from flask import redirect, url_for
# raw_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual.json"
raw_path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica.json"
# raw_path = "C:/@code/APIMISUSE/data/misuse_jsons/accepted_comments.json"
# raw_path = "C:\@code\APIMISUSE\data\misuse_jsons\\rejected_comments.json"

# processed_path = "data/misuse_jsons/manual/merged_split_hunk_AST_manual_processed.json"
processed_path = raw_path

total_length = 0
data = []
with open(raw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# for idx,item in enumerate(data):
#     data[idx]["number"] = idx
# #save the data to json file
# with open(processed_path, "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)

app = Flask(__name__)

@app.route('/review/<int:index>')
def review(index=0):

    item = data[index] if index < len(data) else data[0]
    print(item)
    #convert to json
    # item = json.loads(item)
    temp_item = {}
    # temp_item["repo_name"] = item["repo_name"]
    # temp_item["core_change"] = item["core_change"]
    # temp_item["method_pos_name"] = item["method_pos_name"]
    # temp_item["method_neg_name"] = item["method_neg_name"]
    # temp_item["api_pos_name"] = item["api_pos_name"]
    # temp_item["api_neg_name"] = item["api_neg_name"]
    temp_item["number"] = item["number"]
    # temp_item["file"] = item["file"]
    # temp_item["label"] = item["label"]
    # temp_item["comments"] = item["comments"]
    temp_item["change"] = item["change"]
    temp_item["AST_diff"] = item["AST_diff"]

    json_data = json.dumps(temp_item, indent=4)
    return render_template('review.html', item=item, json_data=json_data, index=index, len_data=len(data))

@app.route('/accept/<int:item_id>', methods=['POST'])
def accept_item(item_id):
    
    data[item_id]["label"] = "yes"
    data[item_id]['comments'] = request.form.get('comments_accept', '')
    # Write the updated data back to the JSON file
    with open(processed_path, 'w') as f:
        json.dump(data, f, indent=4)
    # Redirect to the next item
    return redirect(url_for('review', index=item_id+1))

@app.route('/reject/<int:item_id>', methods=['POST'])
def reject_item(item_id):

    data[item_id]["label"] = "no"
    data[item_id]['comments'] = request.form.get('comments_reject', '')
    # Write the updated data back to the JSON file
    with open(processed_path, 'w') as f:
        json.dump(data, f, indent=4)
    # Redirect to the next item
    return redirect(url_for('review', index=item_id+1))

if __name__ == '__main__':
    app.run()
