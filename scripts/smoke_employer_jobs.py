#!/usr/bin/env python3
"""Smoke test employer jobs API (list, update, close, reopen)."""
from __future__ import annotations

import json
import sys
from urllib import error, request

BASE = "http://127.0.0.1:8001"


def req(method: str, path: str, body: dict | None = None, cookie: str = "") -> tuple[int, dict | list]:
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if cookie:
        headers["Cookie"] = cookie
    r = request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    try:
        with request.urlopen(r, timeout=30) as resp:
            raw = resp.read().decode()
            cookie_out = resp.headers.get("Set-Cookie", cookie)
            return resp.status, json.loads(raw) if raw else {}, cookie_out
    except error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return exc.code, payload, cookie


def main() -> int:
    failures: list[str] = []

    status, login, cookie = req(
        "POST",
        "/auth/login",
        {"email": "demo.employer@test.com", "password": "demo1234"},
    )
    if status != 200:
        failures.append(f"login failed: {status} {login}")
        print("\n".join(failures))
        return 1

    status, jobs, cookie = req("GET", "/jobs/mine", cookie=cookie)
    if status != 200:
        failures.append(f"list jobs failed: {status}")
    elif not isinstance(jobs, list) or len(jobs) == 0:
        failures.append("expected demo employer to have jobs")
    else:
        print(f"OK list: {len(jobs)} jobs")
        job = jobs[0]
        for field in ("title", "status", "created_at", "required_skills"):
            if field not in job:
                failures.append(f"missing field on job: {field}")
        print(f"  sample: {job.get('title')} status={job.get('status', 'open')}")

        job_id = job["id"]
        status, updated, cookie = req(
            "PUT",
            f"/jobs/mine/{job_id}",
            {
                **{k: job[k] for k in job if k not in ("embedding",)},
                "company": job.get("company") or "Demo Co",
                "location": job.get("location") or "Bengaluru",
                "remote_policy": True,
            },
            cookie=cookie,
        )
        if status != 200:
            failures.append(f"update failed: {status} {updated}")
        elif not updated.get("updated_at"):
            failures.append("update missing updated_at")
        else:
            print(f"OK update: company={updated.get('company')}")

        status, closed, cookie = req(
            "PATCH",
            f"/jobs/mine/{job_id}/status",
            {"status": "closed"},
            cookie=cookie,
        )
        if status != 200 or closed.get("status") != "closed":
            failures.append(f"close failed: {status} {closed}")
        else:
            print("OK close role")

        status, reopened, cookie = req(
            "PATCH",
            f"/jobs/mine/{job_id}/status",
            {"status": "open"},
            cookie=cookie,
        )
        if status != 200 or reopened.get("status") != "open":
            failures.append(f"reopen failed: {status} {reopened}")
        else:
            print("OK reopen role")

    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("All employer jobs smoke checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
