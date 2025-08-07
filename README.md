# ^2
Squared is an agent based package that has 1 feedback loop over top of itself

## Setting up the VM

Update python to 3.10 (Ubuntu 22)

`sudo apt update && sudo apt install -y build-essential git python3-pip`


## Install ^2
`pip install git+https://github.com/vilidea-team/squared.git`

## Setup ^2
1. Add a correlating ollama model as the default

`squared model gpt-oss:20b`
  
2. Download our agent.py file or create your own prompts

3. Run the loop

`squared start "my detailed prompt goes here"`

### If you want to use your own agent you can point it towards your own file 

`squared start --agent /path/to/other_agent.py "my detailed prompt goes here"`
