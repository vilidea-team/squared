#!/usr/bin/env python3
import argparse, subprocess, time, ollama


feedback_prompt = """
Your job is to make something wonderful. You may never know the people you impact, you will likely never get applauded, or recognized, but you have a passion so deep to make something great. Please decide if the above answer fully accomplishes what we are making. 

To be finished it must get an A+ in the 3 categories, your job is to dive analize the task at hand and then determine between F-A+ if each category is wonderful.

1. SIMPLICITY: Is it too messy? complex? overwhelming? 
- An A+ in simplicity means the answer is >90% efficient in fixing the task request

2. QUALITY: How well does it fit into the given requirements?
- An A+ in quality means the answer meets >90% of all requirements of the original task request

3. UNIQUENESS: How creative is it? Does it feel human?
- An A+ in uniqueness means the answer is >90% likelihood to be an original thought someone might have. 

If it does get an A+ in all 3 categories it is critical that you just return the word "DONE". If not, then you will need to provide why, here's how: first say something that was done nicely, then say what was done incorrectly or not good enough.

Your job is not to solve the problem, it is your job to provide concise, high quality feedback or (on if the answer is wonderful) determine it gets an A+ in all 3 categories.

So, what do you think?
"""

YELLOW = "\033[33m"
GREY = "\033[38;5;244m"
WHITE = "\033[37m"


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
  
    print(f"\n\n{YELLOW}> { self.attempts }: Work Thinking... \n")
  
    for chunk in work_stream:
      
      message = chunk["message"]
      
      if "thinking" in message:
        print(f"{GREY}{ message["thinking"] }", end='', flush=True)
      
      elif "content" in message:
        
        # If this is the first update to content, add to logger
        if work_content == "":
          print(f"\n\n{YELLOW}> { self.attempts }: Work Response: \n")
  
        blurb = message["content"]
        print(f"{WHITE}{ blurb }", end='', flush=True)
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
  
    print(f"\n\n{YELLOW}> { self.attempts }: Thinking of feedback... \n")
    
    for chunk in feedback_stream:
      
      message = chunk["message"]
  
      if "thinking" in message:
        print(f"{GREY}{ message["thinking"] }", end='', flush=True)
        
      elif "content" in message:
        
        # If this is the first update to content, add to logger
        if feedback_content == "":
          print(f"\n\n{YELLOW}> { self.attempts }: Feedback Response: \n")
  
        blurb = message["content"]
        print(f"{WHITE}{ blurb }", end='', flush=True)
        feedback_content += blurb

    self.messages.append({"role": "user", "content": feedback_content})
    
    self.attempts += 1
    
    print(f"\n\n{YELLOW}> Loop complete - total attempts: { self.attempts } \n")
    
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
