# UI

# Server
Below is the setup on a Linux machine. First, run 
```cd server``` followed by ```python3 -m venv venv``` and ```source venv/bin/activate``` to setup and start a virtual environment. Next, ensure ```ollama``` is installed locally, and run ```$ ollama pull gemma2:2b``` in your terminal outside of the venv.

I used Gemma 2 used for efficiency (as my machine only has 6GB VRAM to work with), and as it performs better when it comes to general knowledge when compared to models like Llama 3.2.

With more time, I would've chosen a better embedding model.