from flask import Flask, render_template, url_for, request
from github import Github

g = Github("TOKEN")
app = Flask(__name__)

@app.route('/')
def homepage():
  return render_template('html/index.html')

@app.route('/sobremim')
def sobremim():
  return render_template('html/sobremim.html')

@app.route('/projetos', methods=['GET'])
def projetos():
  readme = ''
  projetos = []

  for repo in g.get_user().get_repos():

    if str(repo.name) == 'patrick-siotti':
      readme = repo.get_readme().decoded_content.decode('utf-8')
    else:
      projetos.append(
        {'nome': repo.name, 'caminho': repo.name} 
      )

  return render_template('html/projetos.html', projetos=projetos, readme=readme)

@app.route('/projetos', methods=['POST'])
def click_projeto():

  readme = ''
  principal = ''
  arquivos = []
  caminho = request.form['caminho']

  try:
    repo = g.get_user().get_repo(f'{caminho}')
    contents = repo.get_contents('/')

  except:
    try:
      if caminho[0] == '/':
        nome = caminho[1:].split('/')
      else:
        nome = caminho.split('/')

      for n, cam in enumerate(nome):
        if n == 0:
          repo = g.get_user().get_repo(cam)
          principal = cam
        elif n == 1:
          caminho = f'{cam}'
        else:
          caminho += f'/{cam}'
      contents = repo.get_contents(caminho)
    except:
      html = False
      if '<!DOCTYPE html>' in caminho[0:30]:
        html = True
        caminho = caminho.replace('<pre>', '').replace('</pre>', '')
      return render_template('html/projetos.html', projetos=[], readme=caminho, html=html)

  for content in contents:

    if content.type == 'file':

      if '.md' in content.path: # readme
        readme = content.decoded_content.decode('utf-8')

      elif str(content.name).split('.')[-1] in ['zip', 'ttf', 'otf', 'db', 'psd']: # ignorar
        arquivos.append({'nome':content.name, 'caminho': '#'})

      elif str(content.name).split('.')[-1] in ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'tiff', 'pdf', 'svg', 'raw', 'webp', 'ico', 'icon', 'psd']: # imagem
        arquivos.append({'nome':content.name, 'caminho': f'<img src="{content.download_url}">'})

      elif str(content.name).split('.')[-1] in ['mp3', 'wma', 'ogg', 'aac', 'wav', 'aiff', 'pcm', 'flac']: # audio
        arquivos.append({'nome':content.name, 'caminho': f'<audio controls>\n<source src="{content.download_url}">\naudio não suportado\n</audio>'})

      elif str(content.name).split('.')[-1] in ['mp4', 'avi', 'm4v', 'mov', 'mpg', 'mpeg', 'wmv']: # video
        arquivos.append({'nome':content.name, 'caminho': f'<video controls>\n<source src="{content.download_url}">\nvideo não suportado\n</video>'})
        
      else:
        arquivos.append({'nome':content.name, 'caminho': f'<pre>\n{content.decoded_content.decode("utf-8")}\n</pre>'})

    elif content.type == 'dir':
      if str(content.name) == 'patrick-siotti': # readme principaç
        readme = content.get_readme().decoded_content.decode('utf-8')
      else: # pastas
        arquivos.append({'nome':content.name, 'caminho':f'{principal}/{caminho}/{content.name}'})

  return render_template('html/projetos.html', projetos=arquivos, readme=readme)

if __name__ == '__main__':
  app.run(port=port)
