from jacksonpy import JacksonAlgo


def test_data_read_json():
    data_path = "jackson_job_shop_scheduling/example/input/input.json"
    d = JacksonAlgo.Data(data_path)
    assert d.get_job_durations() == [
        [1, 3, 4, 6, 5],
        [2, 2, 3, 6, 9],
        [3, 8, 9, 2, 6],
        [4, 7, 6, 3, 2],
        [5, 3, 6, 4, 5],
        [6, 5, 8, 7, 9],
    ]


def test_data_read_txt():
    data_path = "jackson_job_shop_scheduling/example/input/input.txt"
    d = JacksonAlgo.Data(data_path)
    assert d.get_job_durations() == [
        [1, 7, 1, 6],
        [2, 4, 3, 2],
        [3, 3, 2, 4],
        [4, 8, 2, 1],
        [5, 5, 7, 3],
    ]
