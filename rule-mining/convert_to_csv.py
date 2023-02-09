import os

def convertAMIELogToCSV(file_path):
    file_name = file_path.split(".")[0].split("/")[-1] + ".csv"
    print("Creating {}".format(file_name))
    with open(os.getcwd() + "/mined_rules/csv/" + file_name, "w") as writer:
        with open(file_path, "r") as reader:
            line_index = 0
            lines = reader.readlines()
            # Find header
            while not lines[line_index].startswith("Rule"):
                line_index += 1
            # Parse and write header
            header = lines[line_index].replace("\t", ",")
            writer.write(header)
            line_index += 1
            # Write rows until end is reached
            while not lines[line_index].startswith("Mining done"):
                row = lines[line_index].replace(",", ".").replace("\t", ",")
                writer.write(row)
                line_index += 1

if __name__ == "__main__":
    # Get a list of all folders in the mined rules directory
    target_dir = os.getcwd() + "/mined_rules/raw_logs/"
    rule_files = [f for f in os.listdir(target_dir) if os.path.isfile(target_dir + f)]
    for file in rule_files:
        convertAMIELogToCSV(target_dir + file)
