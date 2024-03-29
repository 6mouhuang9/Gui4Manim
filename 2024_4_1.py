def get_user_choice(options, prompt):
    """让用户从提供的选项中做出选择，并返回选择的项目。"""
    print(prompt)
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    while True:
        choice = input("请选择一个选项: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("无效选择，请重试。")

def collect_params(params):
    """收集并返回用户为给定参数提供的值。"""
    collected_params = {}
    for param, _ in params.items():
        value = input(f"请输入 {param} 的值: ")
        collected_params[param] = value
    return collected_params

def main():
    animations_data = []

    object_types = ["Circle", "Square"]
    animation_effects = ["FadeIn", "FadeOut", "Rotate"]
    params_options = {
        "Circle": {"radius": None, "color": None},
        "Square": {"side_length": None, "color": None}
    }
    animation_params_options = {
        "FadeIn": {"run_time": None},
        "FadeOut": {"run_time": None},
        "Rotate": {"angle": None, "run_time": None}
    }

    num_objects = int(input("你想创建多少个动画对象? "))
    for i in range(num_objects):
        print(f"\n配置动画对象 #{i+1}")
        object_type = get_user_choice(object_types, "选择动画对象类型:")
        params = collect_params(params_options[object_type])
        
        num_effects = int(input("\n这个动画对象需要几个动画效果? "))
        animations = {}
        for j in range(1, num_effects + 1):
            print(f"\n配置动画效果 #{j}")
            effect = get_user_choice(animation_effects, "选择一个动画效果:")
            effect_params = collect_params(animation_params_options[effect])
            animations[j] = {"effect": effect, "params": effect_params}

        animations_data.append({
            "index": i+1,
            "type": object_type,
            "params": params,
            "animations": animations
        })

    print("\n最终的动画数据结构: ")
    print(animations_data)

if __name__ == "__main__":
    main()
