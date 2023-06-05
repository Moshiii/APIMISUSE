from difflib import ndiff

def diff_substring_wrapper(string1, string2):

    # if start with + or -  ignore the first character
    # string1 = "-            if isinstance(model, Module):"
    # string2 = "+            if isinstance(model, torch.nn.Module):"


    string1 =[x[1:] for x in string1 if x[0] == "-"]
    string2 =[x[1:] for x in string2 if x[0] == "+"]
    string1 = [x.strip() for x in string1]
    string2 = [x.strip() for x in string2]
    string1 = " ".join(string1)
    string2 = " ".join(string2)
    # print(string1)
    # print(string2)

    diff_a,diff_b = diff_substring(string1, string2)
    diff_a = [x.strip() for x in diff_a]
    diff_b = [x.strip() for x in diff_b]
    diff_a = "".join(diff_a)
    diff_b = "".join(diff_b)

    print(diff_a)
    print(diff_b)



def diff_substring(str1, str2):
    diff = ndiff(str1, str2)
    diff_list = list(diff)
    print(diff_list)

    diff_a = [x[1:] for x in diff_list if x[0] == "-"]
    diff_b = [x[1:] for x in diff_list if x[0] == "+"]
    return diff_a,diff_b


string1 = [
            "-self.conv_loc = nn.Conv2d(self.feat_channels, 1, 1)",
            "-self.conv_shape = nn.Conv2d(self.feat_channels, self.num_anchors * 2,",
            "-1)",
            "-self.feat_channels,"
        ]
string2 = [
            "+self.conv_loc = nn.Conv2d(self.in_channels, 1, 1)",
            "+self.conv_shape = nn.Conv2d(self.in_channels, self.num_anchors * 2, 1)",
            "+self.in_channels,"
        ]
diff_substring_wrapper(string1, string2)