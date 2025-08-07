#!/usr/bin/env python3
import argparse, subprocess, time, ollama


feedback_prompt = """
Please decide if the above message acomplishes what I asked.

To be acomplished it must get an A+ in the following 3 categories:
1. SIMPLICITY: Is it too messy? complex? overwhelming?
2. QUALITY: How well does it fit the given requirements?
3. UNIQUENESS: How creative is it? Does it feel human?

If it does get an A+ in all 3 categories it is critical that you just return the word "DONE". If not, then you will need to provide why, here's how: first say something that was done nicely, then say what was done incorrectly. 

Your job is not to micromanage and try to solve the problem, it is simply to provide concise, high quality feedback or determine it is DONE.
"""


class Loop:
  
  def __init__(self, model, prompt):
    self.model = model
    self.messages = [{"role": "user", "content": prompt}]
    self.attempts = 0
    self.working = True

  def run(self):
    try:
      while self.working:
        self._loop()
    except KeyboardInterrupt:
      print("> Connection interrupted from key input")

  def _loop(self):
  
    # Our main worker starts every round of feedback
    work_stream = ollama.chat(model=self.model, messages=self.messages, think=True, stream=True)
    work_content = ""
    work_thinking = ""
  
    print(f"\n\n\033[33m> { self.attempts }: Work Thinking... \n")
  
    for chunk in work_stream:
      
      message = chunk["message"]
      
      if "thinking" in message:
        print(message["thinking"], end='', flush=True)
      
      elif "content" in message:
        
        # If this is the first update to content, add to logger
        if work_content == "":
          print(f"\n\n\033[33m> { self.attempts }: Work Response: \n")
  
        blurb = message["content"]
        print(blurb, end='', flush=True)
        work_content += blurb
  
  
    # Work round complete, add the message!
    self.messages.append({"role": "assistant", "content": work_content})

    
    # Next get feedback on the work. 
    # 1st message is the original prompt
    # 2nd message is the work from this loop (aka the last message)
    # 3rd message is our feedback prompt
    feedback_stream = ollama.chat(model=self.model, messages=[
      self.messages[0],
      self.messages[-1],
      {"role": "user", "content": feedback_prompt}
    ], think=True, stream=True)
    
    feedback_content = ""
  
    print(f"\n\n\033[33m> { self.attempts }: Thinking of feedback... \n")
    
    for chunk in feedback_stream:
      
      message = chunk["message"]
  
      if "thinking" in message:
        print(f"\033[97m{ message["thinking"] }", end='', flush=True)
        
      elif "content" in message:
        
        # If this is the first update to content, add to logger
        if feedback_content == "":
          print(f"\n\n\033[33m> { self.attempts }: Feedback Response: \n")
  
        blurb = message["content"]
        print(blurb, end='', flush=True)
        feedback_content += blurb

    self.messages.append({"role": "user", "content": feedback_content})
    
    self.attempts += 1
    
    print(f"\n\n\033[33m> Loop complete - total attempts: { self.attempts } \n")
    
    if feedback_content.strip().upper() == "DONE":
      print("\n\n> \033[92mSUCCESS! A valid answer has been given\n\n")
      self.working = False
  





def main():
  
  parser = argparse.ArgumentParser(description="simple loop agent")
  parser.add_argument("--model",  required=True)
  parser.add_argument("--prompt", required=True)
  
  args = parser.parse_args()
  
  job = Loop(args.model, args.prompt)
  job.run()

if __name__ == "__main__":
  main()
