# pybrtools

### Vídeo

#### Pipeline de edição

**Step: Download**
1. Ler o arquivo CSV (planilha no Google Sheets) que contém todas as informações das palesteras.
2. Ler o arquivo de *status*. Esse arquivo guardará a lista de palestras já baixadas do S3.
3. Checa se a pasta de destino já contém 3 arquivos baixados. Se sim, *pausa* o processo e espera próximos passos.
  - Não adianta baixarmos todos os arquivos de uma vez, se não conseguirmos processá-los na mesma velocidade.
4. Caso a pasta destino não esteja no limite, baixe a próxima palestra e atualiza arquivo de *status*.

**Step: Processamento**
1. Mover primeiro arquivo baixado no passo anterior para a pasta de processamento
2. Cortar o vídeo de acordo com os tempos presentes na planilha
3. Adicionar vinheta
4. Mover para pasta de pós processamento

**Step: Upload**
1. Renomear arquivo com slug da palestra (TODO: definir padrão)
2. Atualizar planilha
3. Fazer upload do arquivo no S3
4. Remover arquivo da máquina
