"""
CivicResolve Guardian - Cryptographic Merkle Audit Engine
Provides tamper-evident proof of audit events and complaint lifecycle transitions.
Generates SHA-256 Merkle roots, cryptographic inclusion proofs, and receipt verifications.
"""

import hashlib
import json
from typing import List, Dict, Any, Optional


def hash_leaf(data: Any) -> str:
    """Computes deterministic SHA-256 hash of arbitrary data or dictionary."""
    if isinstance(data, dict):
        normalized = json.dumps(data, sort_keys=True, separators=(",", ":"))
    elif isinstance(data, str):
        normalized = data
    else:
        normalized = str(data)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def hash_pair(left: str, right: str) -> str:
    """Computes SHA-256 hash of two concatenated child hashes in canonical order."""
    combined = (left + right).encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


class MerkleNode:
    def __init__(self, hash_val: str, left: Optional["MerkleNode"] = None, right: Optional["MerkleNode"] = None):
        self.hash_val = hash_val
        self.left = left
        self.right = right


class MerkleTree:
    """
    Cryptographic Merkle Tree implementation for immutable public audit logs.
    Guarantees that municipal officers or database administrators cannot retroactively
    alter or backdate complaint status changes without invalidating the Merkle Root.
    """

    def __init__(self, leaves: List[Any]):
        self.raw_leaves = leaves
        self.leaf_hashes: List[str] = [hash_leaf(leaf) for leaf in leaves] if leaves else [hash_leaf("EMPTY_ROOT")]
        self.root = self._build_tree(self.leaf_hashes)

    def _build_tree(self, hashes: List[str]) -> MerkleNode:
        if not hashes:
            return MerkleNode(hash_leaf("EMPTY_TREE"))
        nodes = [MerkleNode(h) for h in hashes]

        while len(nodes) > 1:
            if len(nodes) % 2 != 0:
                # Duplicate the last node to balance the tree if odd
                nodes.append(MerkleNode(nodes[-1].hash_val))

            next_level = []
            for i in range(0, len(nodes), 2):
                left_node = nodes[i]
                right_node = nodes[i + 1]
                parent_hash = hash_pair(left_node.hash_val, right_node.hash_val)
                next_level.append(MerkleNode(parent_hash, left=left_node, right=right_node))
            nodes = next_level

        return nodes[0]

    @property
    def root_hash(self) -> str:
        return self.root.hash_val

    def generate_proof(self, leaf_index: int) -> List[Dict[str, str]]:
        """
        Generates an audit inclusion proof for a leaf at a given index.
        Returns a list of sibling nodes with their position ('left' or 'right').
        """
        if leaf_index < 0 or leaf_index >= len(self.leaf_hashes):
            raise IndexError("Leaf index out of bounds")

        proof: List[Dict[str, str]] = []
        current_index = leaf_index
        level_hashes = list(self.leaf_hashes)

        while len(level_hashes) > 1:
            if len(level_hashes) % 2 != 0:
                level_hashes.append(level_hashes[-1])

            is_right_child = (current_index % 2 == 1)
            sibling_index = current_index - 1 if is_right_child else current_index + 1
            sibling_hash = level_hashes[sibling_index]
            position = "left" if is_right_child else "right"

            proof.append({"position": position, "hash": sibling_hash})

            # Ascend to parent level
            next_level = []
            for i in range(0, len(level_hashes), 2):
                next_level.append(hash_pair(level_hashes[i], level_hashes[i + 1]))
            level_hashes = next_level
            current_index = current_index // 2

        return proof

    @staticmethod
    def verify_proof(leaf: Any, proof: List[Dict[str, str]], root_hash: str) -> bool:
        """
        Verifies whether a given leaf item belongs to the Merkle tree defined by root_hash.
        """
        current_hash = hash_leaf(leaf)
        for p in proof:
            sibling_hash = p["hash"]
            if p["position"] == "left":
                current_hash = hash_pair(sibling_hash, current_hash)
            else:
                current_hash = hash_pair(current_hash, sibling_hash)
        return current_hash == root_hash

    def export_receipt(self, complaint_id: str) -> Dict[str, Any]:
        """Exports a cryptographic receipt for civic accountability and public ombudsman audit."""
        return {
            "complaint_id": complaint_id,
            "merkle_root": self.root_hash,
            "total_audit_events": len(self.raw_leaves),
            "algorithm": "SHA-256",
            "tamper_evident": True,
            "leaf_hashes": self.leaf_hashes,
        }
