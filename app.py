from flask import Flask, request, jsonify, render_template_string
import requests, re, os
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_KEY", "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")

HTML = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>My GPT</title><style>body{margin:0;background:#0A0A1A;color:white;font-family:system-ui;height:100vh;display:flex;flex-direction:column}#chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}.msg{max-width:85%;padding:12px 16px;border-radius:18px;font-size:14px;line-height:1.5;white-space:pre-wrap}.user{align-self:flex-end;background:white;color:black}.ai{align-self:flex-start;background:#1E1E32}.bar{padding:12px;display:flex;gap:8px;border-top:1px solid #222}input{flex:1;background:#1E1E32;border:1px solid #333;color:white;padding:12px 18px;border-radius:24px;outline:none}button{width:44px;height:44px;border-radius:50%;border:none;background:white;cursor:pointer;font-weight:bold}</style></head><body><div id="chat"><div class="msg ai">Hello! I am My GPT 🚀 Ask me anything!</div></div><div class="bar"><input id="in" placeholder="Ask anything..." onkeydown="if(event.key==='Enter')go()"><button onclick="go()">↑</button></div><script>function add(t,c){let ch=document.getElementById('chat');let d=document.createElement('div');d.className='msg '+c;d.innerText=t;ch.appendChild(d);ch.scrollTop=ch.scrollHeight;return d;}async function go(){let i=document.getElementById('in');let q=i.value.trim();if(!q)return;add(q,'user');i.value='';let a=add('Thinking...','ai');let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});let j=await r.json();a.innerText=j.reply;}</script></body></html>"""

@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/chat', methods=['POST'])
def chat():
    q = request.json.get('message','')
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {GROQ_KEY}","Content-Type":"application/json"}, json={"model":"openai/gpt-oss-20b","messages":[{"role":"user","content":q}]}, timeout=30)
        d = r.json()
        txt = d["choices"][0]["message"]["content"] if "choices" in d else str(d)
        return jsonify({"reply": txt})
    except Exception as e:
        return jsonify({"reply": str(e)})
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)