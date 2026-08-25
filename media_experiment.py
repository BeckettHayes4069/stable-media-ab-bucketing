"""Stable A/B assignment for media streaming users."""
import hashlib
import argparse
from dataclasses import dataclass

import infrai


@dataclass(frozen=True)
class Assignment:
    user_id: str
    variant: str
    bucket: int


def stable_bucket(user_id: str, experiment: str) -> int:
    digest = hashlib.sha256(f"{experiment}:{user_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % 100


def assign(user_id: str, experiment: str = "media-player-ab") -> Assignment:
    """Read the flag's default_value, then assign deterministically within its split."""
    flag = infrai.infrai.flags.get_value(experiment)
    default_value = flag.get("default_value", {})
    variants = default_value.get("variants", ["control", "treatment"])
    if len(variants) != 2:
        raise ValueError("default_value.variants must contain two variants")
    bucket = stable_bucket(user_id, experiment)
    variant = variants[0] if bucket < 50 else variants[1]
    return Assignment(user_id=user_id, variant=variant, bucket=bucket)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-flags", action="store_true", help="list existing flags and exit")
    parser.add_argument("--experiment", default="media-player-ab")
    args = parser.parse_args()
    if args.list_flags:
        for flag in infrai.infrai.flags.list():
            print(f"{flag['key']} ({flag['type']})")
        raise SystemExit(0)
    for user in ("listener-101", "listener-202", "listener-303"):
        print(assign(user, args.experiment))
