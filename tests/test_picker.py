from utils.picker import sample_without_replacement


def test_sample_without_replacement():

    test_list = ["2", "3", "4"]

    output, adjusted_list = sample_without_replacement(test_list)

    assert output in test_list
    assert output not in adjusted_list
