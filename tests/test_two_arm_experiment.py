import pytest
from promoted_python_delivery_client.client.two_arm_experiment import TwoArmExperiment, create_50_50_two_arm_experiment_config
from promoted_python_delivery_client.model.cohort_arm import CohortArm


def test_create_success():
    exp = TwoArmExperiment("HOLD_OUT", 10, 50, 10, 50)
    assert exp.cohort_id == "HOLD_OUT"
    assert exp.num_control_buckets == 50
    assert exp.num_treatment_buckets == 50
    assert exp.num_active_control_buckets == 10
    assert exp.num_active_treatment_buckets == 10


def test_create_invalid_cohort_id():
    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("", 10, 50, 10, 50)
        assert str(ex) == "Cohort ID must be non-empty"


def test_create_invalid_bucket_active_counts():
    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("a", -1, 50, 10, 50)
        assert str(ex) == "Active control buckets must be between 0 and the total number of control buckets"

    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("a", 51, 50, 10, 50)
        assert str(ex) == "Active control buckets must be between 0 and the total number of control buckets"

    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("a", 10, 50, -1, 50)
        assert str(ex) == "Active treatment buckets must be between 0 and the total number of treatment buckets"

    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("a", 10, 50, 51, 50)
        assert str(ex) == "Active treatment buckets must be between 0 and the total number of treatment buckets"


def test_create_invalid_bucket_counts():
    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("a", 0, -1, 10, 50)
        assert str(ex) == "Control buckets must be positive"

    with pytest.raises(ValueError) as ex:
        TwoArmExperiment("a", 10, 50, 0, -1)
        assert str(ex) == "Treatment buckets must be positive"


def test_create_two_arm_experiment_1_percent_success():
    exp = create_50_50_two_arm_experiment_config("HOLD_OUT", 1, 1)
    assert exp.cohort_id == "HOLD_OUT"
    assert exp.num_control_buckets == 50
    assert exp.num_treatment_buckets == 50
    assert exp.num_active_control_buckets == 1
    assert exp.num_active_treatment_buckets == 1


def test_create_two_arm_experiment_10_and_5_percent_success():
    exp = create_50_50_two_arm_experiment_config("HOLD_OUT", 10, 5)
    assert exp.cohort_id == "HOLD_OUT"
    assert exp.num_control_buckets == 50
    assert exp.num_treatment_buckets == 50
    assert exp.num_active_control_buckets == 10
    assert exp.num_active_treatment_buckets == 5


def test_user_in_control():
    exp = create_50_50_two_arm_experiment_config("HOLD_OUT", 50, 50)
    mem = exp.check_membership("user0")
    assert mem is not None
    assert mem.cohort_id == "HOLD_OUT"
    assert mem.arm == CohortArm.CONTROL


def test_user_not_active():
    exp = create_50_50_two_arm_experiment_config("HOLD_OUT", 1, 1)
    mem = exp.check_membership("user4")
    assert mem is None


def test_user_in_treatment():
    exp = create_50_50_two_arm_experiment_config("HOLD_OUT", 50, 50)
    mem = exp.check_membership("user1")
    assert mem is not None
    assert mem.cohort_id == "HOLD_OUT"
    assert mem.arm == CohortArm.TREATMENT


def test_create_50_50_invalid_percents():
    with pytest.raises(ValueError) as ex:
        create_50_50_two_arm_experiment_config("HOLD_OUT", -1, 50)
        assert str(ex) == "Control percent must be in the range [0, 50]"

    with pytest.raises(ValueError) as ex:
        create_50_50_two_arm_experiment_config("HOLD_OUT", 51, 50)
        assert str(ex) == "Control percent must be in the range [0, 50]"

    with pytest.raises(ValueError) as ex:
        create_50_50_two_arm_experiment_config("HOLD_OUT", 50, -1)
        assert str(ex) == "Treatment percent must be in the range [0, 50]"

    with pytest.raises(ValueError) as ex:
        create_50_50_two_arm_experiment_config("HOLD_OUT", 50, 51)
        assert str(ex) == "Treatment percent must be in the range [0, 50]"
