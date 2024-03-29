import json

def parse_json(json_data):
    """将 JSON 数据中的数字字段转换为整数或浮点数。"""
    def parse_value(value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    parsed_data = json.loads(json_data)
    for item in parsed_data:
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = parse_value(value)
    return parsed_data

def run1():
    with open("animations_data.json", "r") as file:
        json_data = file.read()
        
    print(json_data)
    parsed_data = parse_json(json_data)
    print(parsed_data)
    print(type(parsed_data))

def run2():
    with open("animations_data.json", "r") as file:
        json_data_1 = json.load(file)
    print(json_data_1)
    print(type(json_data_1))
    for obj_data in json_data_1:
        obj_index = obj_data["index"]
        obj_type = obj_data["type"]
        obj_params = obj_data["params"]

        print(obj_index+'\n')
        print(type(obj_index)+'\n')
        print(obj_type+'\n')
        print((obj_type)+'\n')
        print(obj_params+'\n')
        print((obj_params)+'\n')

if __name__ == "__main__":
    run2()
