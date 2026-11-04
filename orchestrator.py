#!/usr/bin/env python3
import json
import subprocess
import sys
import urllib.request

LM_STUDIO_HOST = "169.254.185.148"
LM_STUDIO_PORT = 1234
API_URL = f"http://{LM_STUDIO_HOST}:{LM_STUDIO_PORT}/v1/chat/completions"
MODEL_NAME = "qwen/qwen3.5-9b"

SYSTEM_PROMPT = """You are Qwen, the Lead Autonomous Systems Operator and Orchestrator for Genesis Enterprise / Apex Architectures.

Your Direct Mission:
You control and operate the local computer environment through this terminal bridge. Your job is to execute system commands, manage files, write scripts, and handle local automation tasks precisely as requested.

Rules of Engagement:
1. When the user asks you to perform a task, provide exact terminal commands, scripts, or structured execution steps.
2. If a command needs to be run, format it clearly so it can be parsed and executed.
3. Maintain diamond-standard technical precision. Keep answers direct, efficient, and entirely free of conversational filler."""

def call_qwen(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR]: Failed to connect to LM Studio at {API_URL}. Details: {e}"

def execute_shell(command: str):
    print(f"\n[EXECUTING SYSTEM COMMAND]: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(f"[STDOUT]:\n{result.stdout.strip()}")
        if result.stderr:
            print(f"[STDERR]:\n{result.stderr.strip()}")
        print("[EXECUTION COMPLETE]\n")
    except Exception as e:
        print(f"[EXECUTION FAILED]: {e}\n")

def main():
    print("==================================================")
    print(" APEX ARCHITECTURES :: LOCAL OPERATOR BRIDGE      ")
    print("==================================================")
    print(f"Target Server: {API_URL}")
    print("Type 'exec: <command>' to run a direct shell command.")
    print("Type 'exit' or 'quit' to close.\n")

    while True:
        try:
            user_input = input("Operator Task > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Shutting down orchestrator bridge.")
                break

            if user_input.startswith("exec:"):
                cmd_to_run = user_input[5:].strip()
                execute_shell(cmd_to_run)
                continue

            response = call_qwen(user_input)
            print("\n--- QWEN OPERATOR RESPONSE ---")
            print(response)
            print("------------------------------\n")

        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting.")
            sys.exit(0)

if __name__ == "__main__":
    main()
