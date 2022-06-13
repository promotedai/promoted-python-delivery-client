import random
from promoted_python_delivery_client.client.sampler import Sampler


def test_max_threshold():
    assert Sampler().sample_random(1) is True


def test_min_threshold():
    assert Sampler().sample_random(0) is False


def test_randomness():
    random.seed(4)
    sampler = Sampler()
    assert sampler.sample_random(0.2) is False
    assert sampler.sample_random(0.2) is True
