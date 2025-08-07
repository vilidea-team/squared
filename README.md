# ^2
Squared is an agent based package that has 1 feedback loop over top of itself

## Setting up the VM

Update python (Ubuntu 22)

`sudo apt update && sudo apt install -y build-essential git python3-pip pipx screen`

### Install using pipx in VM

`echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`

`pipx install git+https://github.com/vilidea-team/squared.git ollama`

## Setup
1. Add a correlating ollama model as the default

`curl -fsSL https://ollama.com/install.sh | sh`

`squared model gpt-oss:20b`
  
2. Download our agent.py file to create your own prompts

3. Run the loop

`squared start "my detailed prompt goes here"`

### If you want to use your own agent you can point it towards your own file 

`squared start --agent /path/to/other_agent.py "my detailed prompt goes here"`
