import pytest
from apps.careers.engine.dag import DirectedAcyclicGraph, CyclicDependencyError

def test_dag_single_linear_path():
    dag = DirectedAcyclicGraph()
    # A -> B -> C
    dag.add_edge("A", "B")
    dag.add_edge("B", "C")

    assert dag.detect_cycle() is False
    sorted_nodes = dag.topological_sort()
    assert sorted_nodes.index("A") < sorted_nodes.index("B") < sorted_nodes.index("C")

def test_dag_milestone_tiers():
    dag = DirectedAcyclicGraph()
    # A and B are independent root skills (Tier 0)
    # C depends on both A and B (Tier 1)
    # D depends on C (Tier 2)
    dag.add_edge("A", "C")
    dag.add_edge("B", "C")
    dag.add_edge("C", "D")

    tiers = dag.resolve_milestone_levels()
    assert len(tiers) == 3
    assert set(tiers[0]) == {"A", "B"}
    assert tiers[1] == ["C"]
    assert tiers[2] == ["D"]

def test_dag_direct_cycle_detected():
    dag = DirectedAcyclicGraph()
    dag.add_edge("A", "B")
    dag.add_edge("B", "A")

    assert dag.detect_cycle() is True
    with pytest.raises(CyclicDependencyError):
        dag.topological_sort()

def test_dag_indirect_cycle_detected():
    dag = DirectedAcyclicGraph()
    # A -> B -> C -> A
    dag.add_edge("A", "B")
    dag.add_edge("B", "C")
    dag.add_edge("C", "A")

    assert dag.detect_cycle() is True
    with pytest.raises(CyclicDependencyError):
        dag.topological_sort()

def test_dag_self_loop_rejected():
    dag = DirectedAcyclicGraph()
    with pytest.raises(CyclicDependencyError):
        dag.add_edge("A", "A")
