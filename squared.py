#!/usr/bin/env python3

"""
USAGE

  # pull model from ollama + set default
  squared model <name>
  
  # run default agent
  squared start [--model ...] "prompt"

  # run your own agent
  squared start  --agent /path/to/other_agent.py [...] "prompt"

"""

import argparse, json, os, subprocess, sys

CONFIG = os.path.expanduser("~/.squared.json")
DEFAULT_MODEL = "gpt-oss:20b"
PACKAGE_DIRECTORY = os.path.dirname(__file__)
DEFAULT_AGENT = os.path.join(PACKAGE_DIRECTORY, "agent.py")


def _save(model): 
  json.dump({"model": model}, open(CONFIG, "w"))

def _load():
  try:
    return json.load(open(CONFIG))["model"]
  except Exception:
    return DEFAULT_MODEL
    
def _run(cmd):
  print("+", " ".join(cmd), flush=True)
  subprocess.run(cmd, check=True)


def cmd_model(args):
  _run(["ollama", "pull", args.model])
  _save(args.model)
  
  print(f"default model → { args.model!r }")

def cmd_start(args):
  model = args.model or _load()
  agent = args.agent or DEFAULT_AGENT
  cmd = [sys.executable, agent, "--model", model, "--prompt", args.prompt, *args.rest]
  
  _run(cmd)


def main():
  
  parser  = argparse.ArgumentParser(prog="squared", description="An agent based package that has 1 feedback loop over top of itself")
  sub = parser.add_subparsers(dest="cmd", required=True)
  
  # Adding default model command
  model = sub.add_parser("model", help="Pull & set default model")
  model.add_argument("model")
  model.set_defaults(func=cmd_model)

  
  start = sub.add_parser("start", help="Start agent loop")
  start.add_argument("--model", help="Override default model")
  start.add_argument("--agent", help="Path to alternate agent to use (.py file)")
  start.add_argument("prompt")
  start.add_argument("rest", nargs=argparse.REMAINDER,
                 help="Extra args passed straight to the agent")
  start.set_defaults(func=cmd_start)
  
  args = parser.parse_args()
  args.func(args)


if __name__ == "__main__":
  main()
  
