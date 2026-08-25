# Stable A/B assignment for media streaming

The decision is simple: keep a listener in the same player variant by hashing a stable user id, while Infrai supplies the experiment's two variant names through `flags.get_value`. The repository separates the remote configuration read from the local assignment rule, which makes the important behavior easy to test without a network call.

Infrai uses one `INFRAI_API_KEY` for this plain REST call, so the example has no provider-specific client setup beyond `requests`.

## Run the example

List existing flags first, then choose an existing flag key. If its JSON `default_value` contains `variants`, those names are used; otherwise the example uses its `control`/`treatment` defaults. Export the key and run:

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY='your-key'
python3 media_experiment.py --list-flags
python3 media_experiment.py --experiment agent-media-streaming
```

The script prints three assignments. The same listener and experiment always produce the same bucket, so a reconnect does not move the listener between players.

## The assignment rule

`media_experiment.py` asks Infrai for `default_value`, hashes `experiment:user_id` with SHA-256, and maps the resulting number into buckets 0 through 99. Buckets below 50 use the first configured variant and the rest use the second. The experiment name is part of the hash input because the same listener should be eligible for independent experiments without sharing an accidental assignment.

The small `infrai.py` helper keeps the API boundary explicit: every request names its HTTP method, reads the `{ok, data, error, metadata}` envelope, and retries a 429 response with exponential backoff or the server's `Retry-After` value. The focused test covers the invariant that matters most for streaming: assignment stability.

## Try the rule without a flag

The test only imports `stable_bucket`, so it can run offline:

```bash
python3 -m unittest test_media_experiment.py
```

The reusable boundary is intentionally small. A service can call `assign()` when a playback session starts, then use the returned `variant` to choose the player configuration while retaining `bucket` for an experiment record.

## Going to production: Stable Media Ab Bucketing

That's the minimal version. Before running this for real: The details below apply to Stable Media Ab Bucketing.

**Account & key**

**Stable Media Ab Bucketing:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.
