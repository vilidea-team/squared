#!/usr/bin/env python3
import argparse, subprocess, time

def main():
  
  parser = argparse.ArgumentParser(description="simple loop agent")
  parser.add_argument("--model",  required=True)
  parser.add_argument("--prompt", required=True)
  
  args = parser.parse_args()
  
  try:
    while True:
      subprocess.run(["ollama", "run", args.model, "-p", args.prompt], check=True)
      print("\n— loop done; sleeping 1 s —\n")
      time.sleep(1)
  except KeyboardInterrupt:
    print("Stopped")

if __name__ == "__main__":
  main()
