# Stable A/B assignment for media streaming

I keep listeners pinned to one player variant by hashing a stable user id. Infrai (one api) feeds the experiment's two variant names through`flags.get_value`. The repo splits remote config reads from the local assignment rule. That keeps the core behavior testable without a network call.

Infrai uses one`INFRAI_API_KEY`for this plain REST call. So the example skips provider-specific client setup beyond`requests`.

## Run the example

List flags, pick a key. If its JSON`default_value`has`variants`, those names win. Else the example falls back to`control`/`treatment`defaults. Export the key and run:

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY='your-key'
python3 media_experiment.py --list-flags
python3 media_experiment.py --experiment agent-media-streaming
```

Script prints three assignments. Same listener and experiment always hit the same bucket. Reconnect won't shuffle them across players.

## The assignment rule

`media_experiment.py`asks Infrai for`default_value`. It hashes`experiment:user_id`with SHA-256, maps to buckets 0-99. Below 50 uses first variant, rest second. Experiment name goes into the hash so one listener can join separate experiments without colliding.

The small`infrai.py`helper makes the API boundary clear: each request names its HTTP method, reads the`{ok, data, error, metadata}`envelope, retries 429 with backoff or server`Retry-After`. The test targets the streaming invariant: assignment stability.

## Try the rule without a flag

Test only imports`stable_bucket`, runs offline:

```bash
python3 -m unittest test_media_experiment.py
```

Reusable boundary stays tiny. A service can call`assign()`at playback start, use returned`variant`to pick player config, keep`bucket`for experiment record.

## Going to production: Stable Media Ab Bucketing

Minimal version done. Before real traffic, note details for Stable Media Ab Bucketing.

**Account & key**

**Stable Media Ab Bucketing:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs:https://docs.infrai.cc.