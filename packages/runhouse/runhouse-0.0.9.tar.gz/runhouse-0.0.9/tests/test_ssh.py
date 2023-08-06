import pytest

import runhouse as rh

# Cluster Tests
@pytest.mark.clustertest
def test_cluster(password_cluster):
    res = password_cluster.run(["echo hi"])
    assert "hi" in res[0][1]

# Function Tests


# Env Tests


# 