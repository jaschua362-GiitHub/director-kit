"""Minimal stdio MCP client for the local ChatCut Desktop launcher (used when this agent session's own ChatCut connection is
stale; `chatcut doctor` verifies the launcher). Usage: python -I finish/chatcut_call.py '<json list of [tool, args]>'
Prints each tool result as JSON. Calls run in order in one session.
"""
import json, subprocess, sys

LAUNCHER = r"%APPDATA%\ChatCut\chatcut-mcp.cmd"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    calls = json.loads(sys.argv[1])
    p = subprocess.Popen(["cmd", "/c", LAUNCHER], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1)
    rid = 0

    def send(method, params=None, notify=False):
        nonlocal rid
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            rid += 1; msg["id"] = rid
        p.stdin.write(json.dumps(msg) + "\n"); p.stdin.flush()
        if notify:
            return None
        while True:
            line = p.stdout.readline()
            if not line:
                raise SystemExit("launcher closed")
            m = json.loads(line)
            if m.get("id") == rid:
                return m

    send("initialize", {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "dcl-finish", "version": "1"}})
    send("notifications/initialized", notify=True)
    for name, args in calls:
        r = send("tools/call", {"name": name, "arguments": args})
        res = r.get("result", r.get("error"))
        text = " ".join(c.get("text", "") for c in (res.get("content", []) if isinstance(res, dict) else []))
        print(json.dumps({"tool": name, "result": text or res}, ensure_ascii=False), flush=True)
    p.stdin.close(); p.terminate()


if __name__ == "__main__":
    main()
