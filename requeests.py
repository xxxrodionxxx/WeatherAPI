
if __name__ == "__main__":
    import requests
    # url = "http://127.0.0.1:8000/cities"
    # #url = "http://127.0.0.1:8000/forecast/Tokyo/2024-08-10 12:00:00"
    # response = requests.get(url)
    # data = response.json()
    # print(data)
    #
    # city = 'Buenos Aires'
    # url = f"http://127.0.0.1:8000/forecast/{city}"
    # request_to_api = requests.get(url)
    # data = request_to_api.json()
    # print(data)

    url = "http://127.0.0.1:8000/forecast/Tokyo/2024-08-13 12:00:00"
    response = requests.get(url)
    data = response.json()
    print(data)
