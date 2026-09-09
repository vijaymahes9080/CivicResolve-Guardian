import pytest
from app.core.merkle import MerkleTree, hash_leaf

def test_merkle_tree_basic():
    events = [
        {"action": "COMPLAINT_SUBMITTED", "by": "citizen-1", "timestamp": "2026-09-01T10:00:00Z"},
        {"action": "TRIAGE_AUTO_RECOMMENDED", "priority": "high", "dept": "WATER_SUPPLY"},
        {"action": "OFFICER_APPROVED", "officer": "officer-chennai-1"},
        {"action": "WORK_COMPLETED", "contractor": "PWD-North"},
    ]
    tree = MerkleTree(events)
    assert len(tree.root_hash) == 64
    assert tree.root_hash.isalnum()

    # Generate proof for leaf 2 (OFFICER_APPROVED)
    proof = tree.generate_proof(2)
    assert len(proof) > 0

    # Verification must succeed for valid leaf
    is_valid = MerkleTree.verify_proof(events[2], proof, tree.root_hash)
    assert is_valid is True

    # Verification must fail if leaf data was tampered with (e.g. fraudulent officer status)
    tampered_event = {"action": "OFFICER_APPROVED", "officer": "malicious_actor"}
    assert MerkleTree.verify_proof(tampered_event, proof, tree.root_hash) is False

def test_merkle_tree_single_and_odd_leaves():
    events = ["Event A", "Event B", "Event C"]
    tree = MerkleTree(events)
    assert tree.root_hash is not None

    for i in range(len(events)):
        proof = tree.generate_proof(i)
        assert MerkleTree.verify_proof(events[i], proof, tree.root_hash) is True

    receipt = tree.export_receipt("CMP-2026-0001")
    assert receipt["complaint_id"] == "CMP-2026-0001"
    assert receipt["merkle_root"] == tree.root_hash
    assert receipt["total_audit_events"] == 3
