import requests


def inspector(baseUrl: str, data: dict):
    """
    :param baseUrl: 基础URL
    :param data: 测试数据
    :return: None
    """

    # 从 JSON 数据中获取 URL、测试数据和预期数据
    url = baseUrl + data["path"]

    # 在pytest中输出测试用例名称
    print(f"Testing {data['name']}...")

    index = 0
    test_cases = data["test_cases"]
    for test_case in test_cases:
        print(f"\nTest Case {index} running..")

        # 请求检查器
        resp = http_inspector(url, test_case["input"], data["method"])

        # 响应状态码检查器
        status_code_inspector(resp, test_case)

        # 响应结果检查器
        response_inspector(resp, test_case)

        print(f"Test Case {index} passed.")
        index += 1


def http_inspector(
    url: str, input_data: dict, method: str = "get"
) -> requests.Response:
    """
    HTTP 请求检查器
    :param url: 基础URL
    :param input_data: 测试数据
    :param method: 请求方法
    :return: requests.Response
    """

    response = None

    # 根据 method 来决定使用什么方法发送 HTTP 请求
    method = method.lower()
    if method == "get":
        response = requests.get(url, params=input_data)
    elif method == "post":
        response = requests.post(url, params=input_data)
    elif method == "put":
        response = requests.put(url, params=input_data)
    elif method == "delete":
        response = requests.delete(url, params=input_data)
    elif method == "patch":
        response = requests.patch(url, params=input_data)
    else:
        assert False, "Unsupported HTTP method"

    return response


def status_code_inspector(response: requests.Response, test_case: dict):
    """
    响应状态码检查器
    :param response: 响应
    :param expected_status_code: 预期状态码
    :return: None
    """

    if "expected_status_code" not in test_case.keys():
        assert (
            response.status_code == 200
        ), f"status_code expected: {str(200)}, actual: {str(response.status_code)}"
    else:
        assert (
            response.status_code == test_case["expected_status_code"]
        ), f"status_code expected: {str(test_case['expected_status_code'])}, actual: {str(response.status_code)}"


def response_inspector(response: requests.Response, test_case: dict):
    """
    响应检查器
    检查响应数据是否符合预期，对每一个参数进行检查，如不匹配则输出错误信息
    :param response: 响应
    :param expected_data: 预期数据
    :return: None
    """

    if "expected" not in test_case.keys() or test_case["expected"] == {} :
        print("Expected data not configured, please check by yourself.")

    # 输出响应结果
    print(f"input:\n {test_case['input']}")
    print(f"output:\n {response.json()}")


    if "expected" in test_case.keys() and test_case["expected"] != {}:
        assert (
            response.json() == test_case["expected"]
        ), f"response expected: {str(test_case['expected'])}, actual: {str(response.json())}"
